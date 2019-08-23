import os
import zipfile
from xml.etree.ElementTree import Element, SubElement
from xml.etree import ElementTree
from xml.dom import minidom
from datetime import datetime
from . import log

def createMef(uuid, metadataFilename, mefFilename):
    z = zipfile.ZipFile(mefFilename, "w")    
    z.write(metadataFilename, os.path.join(uuid, "metadata", os.path.basename(metadataFilename)))
    info = getInfoXmlContent(uuid)
    z.writestr(os.path.join(uuid, "info.xml"), info)
    z.close()
    log.logInfo("MEF file written to %s" % mefFilename)

def _addSubElement(parent, tag, value=None):
    sub = SubElement(parent, tag)
    if value is not None:
        sub.text = value
    return sub

def getInfoXmlContent(uuid):
    root = Element("info", {"version": "1.1"})
    general = _addSubElement(root, "general")
    d = datetime.now().isoformat()
    _addSubElement(general, "changeDate", d)
    _addSubElement(general, "createDate", d)
    _addSubElement(general, "schema", "iso19139")
    _addSubElement(general, "format", "full")
    _addSubElement(general, "uuid", uuid)
    _addSubElement(general, "siteName", "GeoCatBridge")
    _addSubElement(general, "isTemplate", "n")
    _addSubElement(root, "categories")
    _addSubElement(root, "privileges")
    _addSubElement(root, "public")
    _addSubElement(root, "private")    
    xmlstring = ElementTree.tostring(root, encoding='UTF-8', method='xml').decode()
    dom = minidom.parseString(xmlstring)    
    return dom.toprettyxml(indent="  ")