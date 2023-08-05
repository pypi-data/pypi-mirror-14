"""OSSOS VOSpace storage convenience package"""
import cStringIO
import errno
import fnmatch
from glob import glob
import os
import re
from string import upper
import tempfile
import logging
import warnings

from astropy.coordinates import SkyCoord
from astropy.io import ascii
from astropy import units
from astropy.units import Quantity
from astropy.utils.exceptions import AstropyUserWarning
from vos import vos
from astropy.io import fits
import requests

requests.packages.urllib3.disable_warnings()
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)


from .downloads.cutouts.calculator import CoordinateConverter

import coding
import util
from .gui import logger
from .wcs import WCS

MAXCOUNT = 30000
_TARGET = "TARGET"

CERTFILE = os.path.join(os.getenv('HOME'),
                        '.ssl',
                        'cadcproxy.pem')

DBIMAGES = 'vos:OSSOS/dbimages'
MEASURE3 = 'vos:OSSOS/measure3'
POSTAGE_STAMPS = 'vos:OSSOS/postage_stamps'
TRIPLETS = 'vos:OSSOS/triplets'
ASTROM_RELEASES = 'vos:OSSOS/0_OSSOSreleases'

DATA_WEB_SERVICE = 'https://www.canfar.phys.uvic.ca/data/pub/'
VOSPACE_WEB_SERVICE = 'https://www.canfar.phys.uvic.ca/vospace/nodes/'
TAP_WEB_SERVICE = 'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/tap/sync'

OSSOS_TAG_URI_BASE = 'ivo://canfar.uvic.ca/ossos'
OBJECT_COUNT = "object_count"


class Wrapper(object):

    def __init__(self, wrapped_class, *args, **kargs):
        self.wrapped_class = wrapped_class(*args, **kargs)

    def __getattr__(self, attr):
        orig_attr = self.wrapped_class.__getattribute__(attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                print "-->", orig_attr, args, kwargs
                result = orig_attr(*args, **kwargs)
                print "<--", type(result)
                return result
            return hooked
        else:
            return orig_attr


# vospace = Wrapper(vos.Client)
vospace = vos.Client()

SUCCESS = 'success'

# ## some cache holders.
mopheaders = {}
astheaders = {}
fwhm = {}
zmag = {}

APCOR_EXT = "apcor"
ZEROPOINT_USED_EXT = "zeropoint.used"
PSF_EXT = "psf.fits"


def get_detections(release='current'):
    """

    @param release: the release to retrieve from VOSpace
    @return: astropy.table.Table
    """
    detection_path = "{}/{}/OSSOS*.detections".format(ASTROM_RELEASES,release)
    filenames = vospace.glob(detection_path)
    if not len(filenames) > 0:
        raise IOError("No detection file found using: {}".format(detection_path))

    return ascii.read(open_vos_or_local(filenames[0]).read(), header_start=-1)


def cone_search(ra, dec, dra=0.01, ddec=0.01, mjdate=None, calibration_level=2):
    """Do a QUERY on the TAP service for all observations that are part of OSSOS (*P05/*P016)
    where taken after mjd and have calibration 'observable'.

    :param ra: RA center of search cont
    :type ra: Quantity
    :param dec: float degrees
    :type dec: Quantity
    :param dra: float degrees
    :type dra: Quantity
    :param ddec: float degrees
    :type ddec: Quantity
    """

    data = dict(QUERY=(" SELECT Observation.observationID as collectionID, "
                       " Plane.time_bounds_cval1 AS mjdate "
                       " FROM caom2.Observation AS Observation "
                       " JOIN caom2.Plane AS Plane "
                       " ON Observation.obsID = Plane.obsID "
                       " WHERE  ( Observation.collection = 'CFHT' ) "
                       " AND Plane.calibrationLevel={} "
                       " AND Plane.energy_bandpassName LIKE 'r.%' "
                       " AND ( Observation.proposal_id LIKE '%P05' or Observation.proposal_id LIKE '%P06' )"
                       " AND Observation.target_name NOT LIKE 'WP%'"),
                REQUEST="doQuery",
                LANG="ADQL",
                FORMAT="tsv")

    data["QUERY"] = data["QUERY"].format(calibration_level)
    data["QUERY"] += (" AND  "
                      " CONTAINS( BOX('ICRS', {}, {}, {}, {}), "
                      " Plane.position_bounds ) = 1 ").format(ra.to(units.degree).value, dec.to(units.degree).value,
                                                              dra.to(units.degree).value, ddec.to(units.degree).value)
    if mjdate is not None:
        data["QUERY"] += " AND Plane.time_bounds_cval1 < {} AND Plane.time_bounds_cval2 > {} ".format(
            mjdate + 1.0 / 24.0,
            mjdate - 1 / 24.0)

    result = requests.get(TAP_WEB_SERVICE, params=data, verify=False)
    assert isinstance(result, requests.Response)
    logger.debug("Doing TAP Query using url: %s" % (str(result.url)))

    table_reader = ascii.get_reader(Reader=ascii.Basic)
    table_reader.header.splitter.delimiter = '\t'
    table_reader.data.splitter.delimiter = '\t'
    table = table_reader.read(result.text)

    logger.debug(str(table))
    return table


def populate(dataset_name,
             data_web_service_url=DATA_WEB_SERVICE + "CFHT"):
    """Given a dataset_name created the desired dbimages directories
    and links to the raw data files stored at CADC."""

    data_dest = get_uri(dataset_name, version='o', ext='fits.fz')
    data_source = "%s/%so.fits.fz" % (data_web_service_url, dataset_name)

    mkdir(os.path.dirname(data_dest))

    try:
        vospace.link(data_source, data_dest)
    except IOError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise e

    header_dest = get_uri(dataset_name, version='o', ext='head')
    header_source = "%s/%so.fits.fz?cutout=[0]" % (
        data_web_service_url, dataset_name)
    try:
        vospace.link(header_source, header_dest)
    except IOError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise e

    header_dest = get_uri(dataset_name, version='p', ext='head')
    header_source = "%s/%s/%sp.head" % (
        'http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/pub', 'CFHTSG', dataset_name)
    try:
        vospace.link(header_source, header_dest)
    except IOError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise e

    return True


def get_cands_uri(field, ccd, version='p', ext='measure3.cands.astrom', prefix=None,
                  block=None):
    """
    return the nominal URI for a candidate file.
    """

    if prefix is None:
        prefix = ""
    if len(prefix) > 0:
        prefix += "_"
    if len(field) > 0:
        field += "_"

    if ext is None:
        ext = ""
    if len(ext) > 0 and ext[0] != ".":
        ext = ".{}".format(ext)

    measure3_dir = MEASURE3
    if block is not None:
        measure3_dir + "/{}".format(block)
    mkdir(measure3_dir)
    return "{}/{}{}{}{}{}".format(measure3_dir, prefix, field, version, ccd, ext)


def get_uri(expnum, ccd=None,
            version='p', ext='fits',
            subdir=None, prefix=None):
    """
    Build the uri for an OSSOS image stored in the dbimages
    containerNode.

    :rtype : basestring
    expnum: CFHT exposure number
    ccd: CCD in the mosaic [0-35]
    version: one of p,s,o etc.
    dbimages: dbimages containerNode.
    @type subdir: str
    @param expnum: int
    @param ccd:
    @param version:
    @param ext:
    @param subdir:
    @param prefix:
    """
    if subdir is None:
        subdir = str(expnum)
    if prefix is None:
        prefix = ''
    uri = os.path.join(DBIMAGES, subdir)

    if ext is None:
        ext = ''
    elif len(ext) > 0 and ext[0] != '.':
        ext = '.' + ext

    if version is None:
        version = ''

    if ccd is None:
        uri = os.path.join(uri,
                           '%s%s%s%s' % (prefix, str(expnum),
                                         version,
                                         ext))
    else:
        ccd = str(ccd).zfill(2)
        uri = os.path.join(uri,
                           'ccd{}'.format(ccd),
                           '%s%s%s%s%s' % (prefix, str(expnum),
                                           version,
                                           ccd,
                                           ext))

    return uri


dbimages_uri = get_uri


def set_tags_on_uri(uri, keys, values=None):
    node = vospace.get_node(uri)
    if values is None:
        values = []
        for idx in range(len(keys)):
            values.append(None)
    assert (len(values) == len(keys))
    for idx in range(len(keys)):
        key = keys[idx]
        value = values[idx]
        tag = tag_uri(key)
        node.props[tag] = value
    return vospace.add_props(node)


def _set_tags(expnum, keys, values=None):
    uri = os.path.join(DBIMAGES, str(expnum))
    node = vospace.get_node(uri, force=True)
    if values is None:
        values = []
        for idx in range(len(keys)):
            values.append(None)
    assert (len(values) == len(keys))
    for idx in range(len(keys)):
        key = keys[idx]
        tag = tag_uri(key)
        value = values[idx]
        node.props[tag] = value
    return vospace.add_props(node)


def set_tags(expnum, props):
    """Assign the key/value pairs in props as tags on on the given expnum.

    @param expnum: str
    @param props: dict
    @return: success
    """
    # now set all the props
    return _set_tags(expnum, props.keys(), props.values())


def set_tag(expnum, key, value):
    """Assign a key/value pair tag to the given expnum containerNode.

    @param expnum:  str
    @param key: str
    @param value: str
    @return: success
    """

    return set_tags(expnum, {key: value})


def tag_uri(key):
    """Build the uri for a given tag key. 

    key: (str) eg 'mkpsf_00'

    """
    if OSSOS_TAG_URI_BASE in key:
        return key
    return OSSOS_TAG_URI_BASE + "#" + key.strip()


def get_tag(expnum, key):
    """given a key, return the vospace tag value.

    @return: value of the tag requested.
    """

    if tag_uri(key) not in get_tags(expnum):
        get_tags(expnum, force=True)
    logger.debug("%s # %s -> %s" % (expnum, tag_uri(key), get_tags(expnum).get(tag_uri(key), None)))
    return get_tags(expnum).get(tag_uri(key), None)


def get_process_tag(program, ccd, version='p'):
    """make a process tag have a suffix indicating which ccd its for.

    """
    return "%s_%s%s" % (program, str(version), str(ccd).zfill(2))


def get_tags(expnum, force=False):
    """

    @param expnum:
    @param force:
    @return: a dictionary of tags.
    @rtype: dict
    """
    uri = os.path.join(DBIMAGES, str(expnum))
    return vospace.get_node(uri, force=force).props


class Task(object):
    """
    A task within the OSSOS pipeline work-flow.
    """

    def __init__(self, executable, dependency=None):
        self.executable = executable
        self.name = os.path.splitext(self.executable)[0]
        self._target = None
        self._status = None
        self._dependency = None
        self.dependency = dependency

    def __str__(self):
        return self.name

    @property
    def tag(self):
        """
        Get the string representation of the tag used to annotate the status in VOSpace.
        @return: str
        """
        return "{}{}_{}{}{:02d}".format(self.target.prefix,
                                        self,
                                        self.target.version,
                                        self.target.ccd)

    @property
    def target(self):
        """

        @return: The target that this task is set to run on.
        @rtype: Target
        """
        return self._target

    @target.setter
    def target(self, target):
        assert isinstance(Target, target)
        self._target = target

    @property
    def dependency(self):
        """
        @rtype: Task
        """
        raise NotImplementedError()

    @dependency.setter
    def dependency(self, dependency):
        if dependency is None:
            self._dependency = dependency
        else:
            assert isinstance(Task, dependency)

    @property
    def status(self):
        """

        @return: The status of running this task on the given target.
        @rtype: str
        """
        return get_tag(self.target.expnum, self.tag)

    @status.setter
    def status(self, status):
        status += util.Time.now().iso
        set_tag(self.target.expnum, self.tag, status)

    @property
    def finished(self):
        """
        @rtype: bool
        """
        return self.status.startswith(SUCCESS)

    @property
    def ready(self):
        if self.dependency is None:
            return True
        else:
            return self.dependency.finished


class Target(object):
    """
    The target that a task will act on.
    """

    def __init__(self, prefix, expnum, version, ccd):
        """

        @param prefix: that is prefixed to the base exposure
        @type prefix: str
        @param expnum: the number of the CFHT exposure that is the target
        @type expnum: str
        @param version: Which version of the exposure (o, p, s) is the target.
        @type version: str
        @param ccd: which CCD of the exposure is the target.
        @type ccd: int
        """

        self.prefix = prefix
        self.expnum = expnum
        self.version = version
        self.ccd = ccd

    @property
    def name(self):
        return "{}{}{}{:02d}".format(self.prefix, self.expnum, self.version, self.ccd)

    @property
    def tags(self):
        """

        @rtype: list [str]
        """
        return get_tags(self.expnum)


def get_status(task, prefix, expnum, version, ccd, return_message=False):
    """Report back status of the given program.

    @param prefix:
    """
    key = get_process_tag(prefix+task, ccd, version)
    status = get_tag(expnum, key)
    logger.debug('%s: %s' % (key, status))
    if return_message:
        return status
    else:
        return status == SUCCESS


def set_status(task, prefix, expnum, version, ccd, status):
    """set the processing status of the given program.

    @param prefix:
    """

    return set_tag(expnum, get_process_tag(prefix+task, ccd, version), status)


def get_file(expnum, ccd=None, version='p', ext='fits', subdir=None, prefix=None):
    uri = get_uri(expnum=expnum, ccd=ccd, version=version, ext=ext, subdir=subdir, prefix=prefix)
    filename = os.path.basename(uri)

    if not os.access(filename, os.F_OK):
        copy(uri, filename)

    return filename


def decompose_content_decomposition(content_decomposition):
    """

    :param content_decomposition:
    :return:
    """
    # check for '-*' in the cutout string and replace is naxis:1

    content_decomposition = re.findall('(\d+)__(\d+)_(\d+)_(\d+)_(\d+)', content_decomposition)
    if len(content_decomposition) == 0:
        content_decomposition = [(0, 1, -1, 1, -1)]
    return content_decomposition


def ra_dec_cutout(uri, sky_coord, radius):
    """

    :param uri: The vospace location of the image to make a cutout from
    :type uri: str
    :param sky_coord: The central coordinate of the cutout
    :type sky_coord: SkyCoord
    :param radius: The radius of the cutout
    :type radius: Quantity
    :return: An HDUList with the cutout
    :rtype: fits.HDUList
    """

    # These two lines enable debugging at httplib level (requests->urllib3->http.client)
    # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
    # The only thing missing will be the response.body which is not logged.
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client

    # Get the 'uncut' images CRPIX1/CRPIX2 values

    coo_sys = upper(sky_coord.frame.name)
    this_cutout = "CIRCLE {} {} {} {}".format(coo_sys, sky_coord.ra.to(units.degree).value,
                                              sky_coord.dec.to(units.degree).value,
                                              radius.to(units.degree).value)

    view = "cutout"

    fobj = vospace.open(uri, view=view, cutout=this_cutout)
    hdulist = fits.open(cStringIO.StringIO(fobj.read()))
    hdulist.verify('silentfix+ignore')
    cutouts = decompose_content_decomposition(fobj.resp.headers.get('content-disposition', '0___'))
    logger.debug("Got cutout boundaries of: {}".format(cutouts))
    logger.debug("Initial Length of HDUList: {}".format(len(hdulist)))

    # Make sure here is a primaryHDU
    if len(hdulist) == 1:
        phdu = fits.PrimaryHDU()
        phdu.header['ORIGIN'] = "OSSOS"
        hdulist.insert(0, phdu)

    logger.debug("Final Length of HDUList: {}".format(len(hdulist)))

    if len(cutouts) != len(hdulist) - 1:
        raise ValueError("Wrong number of cutout structures found in Content-Disposition response.")

    for hdu in hdulist[1:]:
        cutout = cutouts.pop(0)
        if 'ASTLEVEL' not in hdu.header:
            print "******* NO ASTLEVEL ********* ASTROMETRY NOT POSSIBLE ********* IGNORE {0} ********".format(uri)
        hdu.header['EXTNO'] = cutout[0]
        hdu.header['DATASEC'] = reset_datasec("[{}:{},{}:{}]".format(cutout[1],
                                                                     cutout[2],
                                                                     cutout[3],
                                                                     cutout[4]),
                                              hdu.header.get('DATASEC', None),
                                              hdu.header['NAXIS1'],
                                              hdu.header['NAXIS2'])
        hdu.header['XOFFSET'] = int(cutout[1]) - 1
        hdu.header['YOFFSET'] = int(cutout[3]) - 1

        hdu.converter = CoordinateConverter(hdu.header['XOFFSET'], hdu.header['YOFFSET'])
        try:
                hdu.wcs = WCS(hdu.header)
        except Exception as ex:
            logger.error("Failed trying to initialize the WCS for {}".format(uri))
            raise ex
    logger.debug("Sending back {}".format(hdulist))
    return hdulist


def get_image(expnum, ccd=None, version='p', ext='fits',
              subdir=None, prefix=None, cutout=None, return_file=True, flip_image=True):
    """Get a FITS file for this expnum/ccd  from VOSpace.


    @param cutout: (str)
    @param return_file: return an filename (True) or HDUList (False)
    @param expnum: CFHT exposure number (int)
    @param ccd:     @param ccd:
    @param version: [p, s, o]  (char)
    @param ext:
    @param subdir:
    @param prefix:
    @return: astropy.io.fits.PrimaryHDU
    """

    filename = os.path.basename(get_uri(expnum, ccd, version, ext=ext, subdir=subdir, prefix=prefix))
    if os.access(filename, os.F_OK) and return_file and cutout is None:
        return filename

    cutout_string = cutout
    try:
        if os.access(filename, os.F_OK) and cutout:
            cutout = datasec_to_list(cutout)
            hdulist = fits.open(filename)
            if len(hdulist) > 1:
                raise ValueError("Local cutout access not designed to work on MEFs yet.")
            header = hdulist[0].header
            cutout[0] = cutout[0] < 0 and header['NAXIS1'] - cutout[0] + 1 or cutout[0]
            cutout[1] = cutout[1] < 0 and header['NAXIS1'] - cutout[1] + 1 or cutout[1]
            cutout[2] = cutout[2] < 0 and header['NAXIS2'] - cutout[2] + 1 or cutout[2]
            cutout[3] = cutout[3] < 0 and header['NAXIS2'] - cutout[3] + 1 or cutout[3]
            logger.debug("DATA array shape: {}".format(hdulist[0].data.shape))
            logger.debug("CUTOUT array: {} {} {} {}".format(cutout[0],
                                                            cutout[1],
                                                            cutout[2],
                                                            cutout[3]))
            flip = cutout[0] < cutout[1] and 1 or -1
            flop = cutout[2] < cutout[3] and 1 or -1
            header['CRPIX1'] = (header.get("CRPIX1", 1) - cutout[0]) * flip + 1
            header['CRPIX2'] = (header.get("CRPIX2", 1) - cutout[2]) * flop + 1
            header['CD1_1'] = header.get("CD1_1", 1) * flip
            header['CD2_1'] = header.get("CD2_1", 1) * flip
            header['CD2_2'] = header.get("CD2_2", 1) * flop
            header['CD1_2'] = header.get("CD1_2", 1) * flop

            data = hdulist[0].data[cutout[2]-1:cutout[3], cutout[0]-1:cutout[1]]
            hdulist[0].data = data
            header['DATASEC'] = reset_datasec(cutout_string,
                                              header['DATASEC'],
                                              header['NAXIS1'],
                                              header['NAXIS2'])
            if return_file:
                cutout_filename = os.path.splitext(filename)[0]+"_{}_{}_{}_{}.fits".format(cutout[0],
                                                                                           cutout[1],
                                                                                           cutout[2],
                                                                                           cutout[3])
                hdulist.writeto(cutout_filename)
                return cutout_filename
            else:
                return hdulist
    except Exception as e:
        logger.debug(str(e))
        logger.debug("Failed trying to access local copy: {} with cutout [{}:{}, {}:{}], using VOSpace".format(
            filename, cutout[2]-1, cutout[3], cutout[0]-1, cutout[1]))

    cutout = cutout_string

    if not subdir:
        subdir = str(expnum)

    logger.debug("Building list of possible uri locations")
    # # here is the list of places we will look, in order
    if version != 'p':
        locations = [(get_uri(expnum, ccd, version, ext=ext, subdir=subdir, prefix=prefix),
                      cutout)]
    else:
        locations = []
    logger.debug(str(locations))
    if ccd is not None:
        try:
            for this_ext in [ext, ext + ".fz"]:
                ext_no = int(ccd) + 1
                # extension 1 -> 18 +  37,36 should be flipped.
                flip_these_extensions = range(1,19)
                flip_these_extensions.append(37)
                flip_these_extensions.append(38)
                flip = (cutout is None and "fits" in ext and (
                    (ext_no in flip_these_extensions and flip_image) and "[-*,-*]" or "[*,*]")) or cutout
                locations.append((get_uri(expnum, version=version, ext=this_ext, subdir=subdir),
                                  "[{}]{}".format(ext_no, flip)))
        except Exception as e:
            logger.error(str(e))
            pass
    else:
        uri = get_uri(expnum, ccd, version, ext=ext, subdir=subdir, prefix=prefix)
        locations.append((uri, cutout))
        uri = get_uri(expnum, ccd, version, ext=ext + ".fz", subdir=subdir, prefix=prefix)
        locations.append((uri, cutout))
    while len(locations) > 0:
        (uri, cutout) = locations.pop(0)
        try:
            hdu_list = get_hdu(uri, cutout)
            if return_file:
                hdu_list.writeto(filename)
                del hdu_list
                return filename
            else:
                return hdu_list
        except Exception as e:
            logger.debug("{}".format(type(e)))
            logger.debug("Failed to open {} cutout:{}".format(uri, cutout))
            logger.debug("vos sent back error: {} code: {}".format(str(e), getattr(e, 'errno', 0)))

    raise IOError(errno.ENOENT, "Failed to get image using {} {} {} {}.".format(expnum, version, ccd, cutout))


def datasec_to_list(datasec):
    """
    convert an IRAF style PIXEL DATA section as to a list of integers.
    @param datasec: str
    @return: list
    """

    return [int(x) for x in re.findall(r"([-+]?[\*\d]+?)[:,\]]+", datasec)]


def reset_datasec(cutout, datasec, naxis1, naxis2):
    """
    reset the datasec to account for a possible cutout.

    @param cutout:
    @param datasec:
    @return:
    """

    if cutout is None or cutout == "[*,*]":
        return datasec

    try:
        datasec = datasec_to_list(datasec)
    except:
        return datasec

    # check for '-*' in the cutout string and replace is naxis:1
    cutout = cutout.replace(" ", "")
    cutout = cutout.replace("[-*,", "{}:1,".format(naxis1))
    cutout = cutout.replace(",-*]", ",{}:1]".format(naxis2))
    cutout = cutout.replace("[*,", "[1:{},".format(naxis1))
    cutout = cutout.replace(",*]", ",1:{}]".format(naxis1))

    try:
        cutout = [int(x) for x in re.findall(r"([-+]?[\*\d]+?)[:,\]]+", cutout)]
    except:
        logger.debug("Failed to processes the cutout pattern: {}".format(cutout))
        return datasec

    if len(cutout) == 5:
        # cutout likely starts with extension, remove
        cutout = cutout[1:]

    # -ve integer offsets indicate offset from the end of array.
    for idx in [0, 1]:
        if cutout[idx] < 0:
            cutout[idx] = naxis1 - cutout[idx] + 1
    for idx in [2, 3]:
        if cutout[idx] < 0:
            cutout[idx] = naxis2 - cutout[idx] + 1

    flip = cutout[0] > cutout[1]
    flop = cutout[2] > cutout[3]

    logger.debug("Working with cutout: {}".format(cutout))

    if flip:
        cutout = [naxis1 - cutout[0] + 1, naxis1 - cutout[1] + 1, cutout[2], cutout[3]]
        datasec = [naxis1 - datasec[1] + 1, naxis1 - datasec[0] + 1, datasec[2], datasec[3]]

    if flop:
        cutout = [cutout[0], cutout[1], naxis2 - cutout[2] + 1, naxis2 - cutout[3] + 1]
        datasec = [datasec[0], datasec[1], naxis2 - datasec[3] + 1, naxis2 - datasec[2] + 1]

    datasec = [max(datasec[0] - cutout[0] + 1, 1),
               min(datasec[1] - cutout[0] + 1, naxis1),
               max(datasec[2] - cutout[2] + 1, 1),
               min(datasec[3] - cutout[2] + 1, naxis2)]

    return "[{}:{},{}:{}]".format(datasec[0], datasec[1], datasec[2], datasec[3])


def get_hdu(uri, cutout=None):
    """Get a at the given uri from VOSpace, possibly doing a cutout.

    If the cutout is flips the image then we also must flip the datasec keywords.  Also, we must offset the
    datasec to reflect the cutout area being used.

    @return: fits.HDU
    """

    # the filename is based on the Simple FITS images file.
    filename = os.path.basename(uri)
    if os.access(filename, os.F_OK) and cutout is None:
        logger.debug("File already on disk: {}".format(filename))
        hdu_list = fits.open(filename, scale_back=True)
        hdu_list.verify('silentfix+ignore')

    else:
        logger.debug("Pulling: {}{} from VOSpace".format(uri, cutout))
        fpt = tempfile.NamedTemporaryFile(suffix='.fits')
        cutout = cutout is not None and cutout or ""
        vospace.copy(uri+cutout, fpt.name)
        fpt.seek(0, 2)
        fpt.seek(0)
        logger.debug("Read from vospace completed. Building fits object.")
        hdu_list = fits.open(fpt, scale_back=False)
        hdu_list.verify('silentfix+ignore')

        logger.debug("Got image from vospace")
        try:
            hdu_list[0].header['DATASEC'] = reset_datasec(cutout, hdu_list[0].header['DATASEC'],
                                                          hdu_list[0].header['NAXIS1'],
                                                          hdu_list[0].header['NAXIS2'])
        except Exception as e:
            logging.debug("error converting datasec: {}".format(str(e)))

    for hdu in hdu_list:
        logging.debug("Adding converter to {}".format(hdu))
        hdu.converter = CoordinateConverter(0, 0)
        try:
            hdu.wcs = WCS(hdu.header)
        except Exception as ex:
            logger.error("Failed trying to initialize the WCS: {}".format(ex))

    return hdu_list


def get_trans(expnum, ccd, prefix=None, version='p'):
    uri = get_uri(expnum, ccd, version, ext='trans.jmp', prefix=prefix)
    logging.info("get_trans: {}".format(uri))
    fobj = open_vos_or_local(uri)
    line = fobj.read()
    fobj.close()
    vs = line.split()
    trans = {'dx': float(vs[0]),
             'cd11': float(vs[1]),
             'cd12': float(vs[2]),
             'dy': float(vs[3]),
             'cd21': float(vs[4]),
             'cd22': float(vs[5])}
    return trans


def get_fwhm(expnum, ccd, prefix=None, version='p'):
    """Get the FWHM computed for the given expnum/ccd combo.

    @param expnum:
    @param ccd:
    @param prefix:
    @param version:
    @return:
    """

    uri = get_uri(expnum, ccd, version, ext='fwhm', prefix=prefix)
    filename = os.path.basename(uri)

    try:
        return fwhm[uri]
    except:
        pass

    try:
        fwhm[uri]=float(open(filename, 'r').read())
        return fwhm[uri]
    except:
        pass

    try:
        fwhm[uri] = float(open_vos_or_local(uri).read())
        return fwhm[uri]
    except Exception as e:
        fwhm[uri] = 4.0
        return fwhm[uri]



def get_zeropoint(expnum, ccd, prefix=None, version='p'):
    """Get the zeropoint for this exposure.

    This command expects that there is a file called #######p##.zeropoint.used which contains the zeropoint.

    @param expnum: exposure to get zeropoint of
    @param ccd: which ccd (extension - 1) to get zp
    @param prefix: possible string prefixed to expsoure number.
    @param version:  one of [spo] as in #######p##
    @return:
    """
    uri = get_uri(expnum, ccd, version, ext='zeropoint.used', prefix=prefix)
    try:
        return zmag[uri]
    except:
        pass

    try:
        zmag[uri] = float(open_vos_or_local(uri).read())
        return zmag[uri]
    except:
        pass

    zmag[uri] = 0.0
    return zmag[uri]


def mkdir(dirname):
    """make directory tree in vospace.

    @param dirname: name of the directory to make
    """
    dir_list = []

    while not vospace.isdir(dirname):
        dir_list.append(dirname)
        dirname = os.path.dirname(dirname)
    while len(dir_list) > 0:
        logging.info("Creating directory: %s" % (dir_list[-1]))
        try:
            vospace.mkdir(dir_list.pop())
        except IOError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise e


def vofile(filename, **kwargs):
    """Open and return a handle on a VOSpace data connection"""
    basename = os.path.basename(filename)
    if os.access(basename, os.R_OK):
        return open(basename, 'r')
    kwargs['view'] = kwargs.get('view', 'data')
    return vospace.open(filename, **kwargs)


def open_vos_or_local(path, mode="rb"):
    """
    Opens a file which can either be in VOSpace or the local filesystem.
    """
    if path.startswith("vos:"):
        primary_mode = mode[0]
        if primary_mode == "r":
            vofile_mode = os.O_RDONLY
        elif primary_mode == "w":
            vofile_mode = os.O_WRONLY
        elif primary_mode == "a":
            vofile_mode = os.O_APPEND
        else:
            raise ValueError("Can't open with mode %s" % mode)

        return vofile(path, mode=vofile_mode)
    else:
        return open(path, mode)


def copy(source, dest):
    """use the vospace service to get a file. """

    #logger.debug("deleting {} ".format(dest))
    #try:
    #    vospace.delete(dest)
    #except Exception as e:
    #    logger.debug(str(e))
    #    pass
    logger.info("copying {} -> {}".format(source, dest))

    return vospace.copy(source, dest)


def vlink(s_expnum, s_ccd, s_version, s_ext,
          l_expnum, l_ccd, l_version, l_ext, s_prefix=None, l_prefix=None):
    """make a link between two version of a file.

    @param s_expnum:
    @param s_ccd:
    @param s_version:
    @param s_ext:
    @param l_expnum:
    @param l_ccd:
    @param l_version:
    @param l_ext:
    @param s_prefix:
    @param l_prefix:
    @return:
    """
    source_uri = get_uri(s_expnum, ccd=s_ccd, version=s_version, ext=s_ext, prefix=s_prefix)
    link_uri = get_uri(l_expnum, ccd=l_ccd, version=l_version, ext=l_ext, prefix=l_prefix)

    return vospace.link(source_uri, link_uri)


def remove(uri):
    try:
        vospace.delete(uri)
    except Exception as e:
        logger.debug(str(e))


def delete(expnum, ccd, version, ext, prefix=None):
    """delete a file, no error on does not exist."""
    uri = get_uri(expnum, ccd=ccd, version=version, ext=ext, prefix=prefix)
    remove(uri)


def my_glob(pattern):
    """get a listing matching pattern"""
    result = []
    if pattern[0:4] == 'vos:':
        dirname = os.path.dirname(pattern)
        flist = listdir(dirname)
        for fname in flist:
            fname = '/'.join([dirname, fname])
            if fnmatch.fnmatch(fname, pattern):
                result.append(fname)
    else:
        result = glob(pattern)
    return result


def listdir(directory, force=False):
    return vospace.listdir(directory, force=force)


def list_dbimages():
    return listdir(DBIMAGES)


def exists(uri, force=False):
    try:
        return vospace.get_node(uri, force=force) is not None
    except EnvironmentError as e:
        logger.error(str(e))  # not critical enough to raise
        # Sometimes the error code returned is the OS version, sometimes the HTTP version
        if e.errno in [404, os.errno.ENOENT]:
            return False


def move(old_uri, new_uri):
    vospace.move(old_uri, new_uri)


def delete_uri(uri):
    vospace.delete(uri)


def has_property(node_uri, property_name, ossos_base=True):
    """
    Checks if a node in VOSpace has the specified property.
    """
    if get_property(node_uri, property_name, ossos_base) is None:
        return False
    else:
        return True


def get_property(node_uri, property_name, ossos_base=True):
    """
    Retrieves the value associated with a property on a node in VOSpace.
    """
    # Must use force or we could have a cached copy of the node from before
    # properties of interest were set/updated.
    node = vospace.get_node(node_uri, force=True)
    property_uri = tag_uri(property_name) if ossos_base else property_name

    if property_uri not in node.props:
        return None

    return node.props[property_uri]


def set_property(node_uri, property_name, property_value, ossos_base=True):
    """
    Sets the value of a property on a node in VOSpace.  If the property
    already has a value then it is first cleared and then set.
    """
    node = vospace.get_node(node_uri)
    property_uri = tag_uri(property_name) if ossos_base else property_name

    # If there is an existing value, clear it first
    if property_uri in node.props:
        node.props[property_uri] = None
        vospace.add_props(node)

    node.props[property_uri] = property_value
    vospace.add_props(node)


def build_counter_tag(epoch_field, dry_run=False):
    """
    Builds the tag for the counter of a given epoch/field,
    without the OSSOS base.
    """
    logger.info("Epoch Field: {}, OBJECT_COUNT {}".format(str(epoch_field), str(OBJECT_COUNT)))
    tag = epoch_field[1] + "-" + OBJECT_COUNT

    if dry_run:
        tag += "-DRYRUN"

    return tag


def read_object_counter(node_uri, epoch_field, dry_run=False):
    """
    Reads the object counter for the given epoch/field on the specified
    node.

    Returns:
      count: str
        The current object count.
    """
    return get_property(node_uri, build_counter_tag(epoch_field, dry_run),
                        ossos_base=True)


def increment_object_counter(node_uri, epoch_field, dry_run=False):
    """
    Increments the object counter for the given epoch/field on the specified
    node.

    Returns:
      new_count: str
        The object count AFTER incrementing.
    """
    current_count = read_object_counter(node_uri, epoch_field, dry_run=dry_run)

    if current_count is None:
        new_count = "01"
    else:
        new_count = coding.base36encode(coding.base36decode(current_count) + 1,
                                        pad_length=2)

    set_property(node_uri,
                 build_counter_tag(epoch_field, dry_run=dry_run),
                 new_count,
                 ossos_base=True)

    return new_count


def get_mopheader(expnum, ccd, version='p', prefix=None):
    """
    Retrieve the mopheader, either from cache or from vospace
    :rtype : fits.Header
    """
    prefix = prefix is None and "" or prefix
    mopheader_uri = dbimages_uri(expnum=expnum,
                                 ccd=ccd,
                                 version=version,
                                 prefix=prefix,
                                 ext='.mopheader')
    if mopheader_uri in mopheaders:
        return mopheaders[mopheader_uri]

    filename = os.path.basename(mopheader_uri)

    if os.access(filename, os.F_OK):
        logger.debug("File already on disk: {}".format(filename))
        mopheader_fpt = cStringIO.StringIO(open(filename, 'r').read())
    else:
        mopheader_fpt = cStringIO.StringIO(open_vos_or_local(mopheader_uri).read())

    with warnings.catch_warnings():
        warnings.simplefilter('ignore', AstropyUserWarning)
        mopheader = fits.open(mopheader_fpt)

        # add some values to the mopheader so it can be an astrom header too.
        header = mopheader[0].header
        try:
            header['FWHM'] = get_fwhm(expnum, ccd)
        except IOError:
            header['FWHM'] = 10
        header['SCALE'] = mopheader[0].header['PIXSCALE']
        header['NAX1'] = header['NAXIS1']
        header['NAX2'] = header['NAXIS2']
        header['MOPversion'] = header['MOP_VER']
        header['MJD_OBS_CENTER'] = str(util.Time(header['MJD-OBSC'],
                                                 format='mjd',
                                                 scale='utc', precision=5).replicate(format='mpc'))
        header['MAXCOUNT'] = MAXCOUNT
        mopheaders[mopheader_uri] = header
        mopheader.close()
    return mopheaders[mopheader_uri]


def _get_sghead(expnum, version):
    """
    Use the data web service to retrieve the stephen's astrometric header.

    :param expnum: CFHT exposure number you want the header for
    :param version: Which version of the header? ('p', 's', 'o')
    :rtype : list of astropy.io.fits.Header objects.
    """

    logger.warning("_get_sghead is depricated, use get_astheader instead.")

    url = "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/pub/CFHTSG/{}{}.head".format(expnum, version)
    logging.getLogger("requests").setLevel(logging.ERROR)
    resp = requests.get(url)
    if resp.status_code != 200:
        raise IOError(errno.ENOENT, "Could not get {}".format(url))

    header_str_list = re.split('END      \n', resp.content)

    # # make the first entry in the list a Null
    headers = [None]
    for header_str in header_str_list:
        headers.append(fits.Header.fromstring(header_str, sep='\n'))

    return headers


def get_header(uri):
    """
    Pull a FITS header from observation at the given URI
    """
    if uri not in astheaders:
        astheaders[uri] = get_hdu(uri, cutout="[1:1,1:1]")[0].header
    return astheaders[uri]


def get_astheader(expnum, ccd, version='p', prefix=None, ext=None):
    """
    Retrieve the header for a given dbimages file.

    @param expnum:  CFHT odometer number
    @param ccd: which ccd based extension (0..35)
    @param version: 'o','p', or 's'
    @return:
    """
    logger.debug("Getting ast header for {}".format(expnum))
    ast_uri = dbimages_uri(expnum, ccd, version=version, ext='.fits')
    if ast_uri not in astheaders:
        hdulist = get_image(expnum, ccd=ccd, version=version, prefix=prefix,
                            cutout="[1:1,1:1]", return_file=False)
        assert isinstance(hdulist, fits.HDUList)
        astheaders[ast_uri] = hdulist[0].header
    return astheaders[ast_uri]


def log_filename(prefix, task, version, ccd):
    return "{}{}_{}{}.txt".format(prefix, task, version, ccd)


def log_location(expnum, ccd):
    return os.path.dirname(get_uri(expnum, ccd=ccd))


def set_logger(task, prefix, expnum, ccd, version, dry_run):
    this_logger = logging.getLogger()
    log_format = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s %(lineno)d: %(message)s')

    filename = log_filename(prefix, task, ccd=ccd, version=version)
    location = log_location(expnum, ccd)
    if not dry_run:
        vo_handler = util.VOFileHandler("/".join([location, filename]))
        vo_handler.setFormatter(log_format)
        this_logger.addHandler(vo_handler)

    file_handler = logging.FileHandler(filename=filename)
    file_handler.setFormatter(log_format)
    this_logger.addHandler(file_handler)
