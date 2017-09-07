"""
Basic Python client for AMR.
http://ipscience-help.thomsonreuters.com/LAMRService/WebServicesOverviewGroup/overview.html
"""

from itertools import izip_longest
import os
import xml.etree.ElementTree as ET
import urllib2

try:
    USER = os.environ['WOS_USER']
    PASSWORD = os.environ['WOS_PASSWORD']
except KeyError:
    raise Exception("Unable to read WOS_USER and WOS_PASSWORD environment variables.")

AMR_URL = "https://ws.isiknowledge.com/cps/xrpc"
BATCH_SIZE = 50


def grouper(iterable, n, fillvalue=None):
    """
    Group iterable into n sized chunks.
    See: http://stackoverflow.com/a/312644/758157
    """
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)


def read(raw):
    ns = {'isi': 'http://www.isinet.com/xrpc41'}
    raw = ET.fromstring(raw)
    out = {}
    for cite in raw.findall('isi:fn/isi:map/isi:map', ns):
        cite_key = cite.attrib['name']
        meta = {}
        for val in cite.findall('isi:map/isi:val', ns):
            meta[val.attrib['name']] = val.text
        out[cite_key] = meta
    return out


def get(request_xml):
    req = urllib2.Request(AMR_URL)
    req.add_header('Content-Type', 'application/xml')
    response = urllib2.urlopen(req, request_xml)
    text = response.read()
    # parse into xml
    xml = read(text)
    return xml


