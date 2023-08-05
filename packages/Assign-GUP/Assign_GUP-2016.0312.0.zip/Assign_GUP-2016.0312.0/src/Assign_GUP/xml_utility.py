
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
XML utility methods
'''

from lxml import etree
import os
import traceback


class IncorrectXmlRootTag(etree.DocumentInvalid):
    '''the root tag of the XML file is incorrect'''
    pass


class InvalidWithXmlSchema(etree.DocumentInvalid):
    '''error while validating against the XML Schema'''
    pass

class XmlSyntaxError(etree.XMLSyntaxError):
    '''Xml Syntax error'''
    pass


def getXmlText(parent, tag, default=None):
    '''
    Read the text content of an XML node
    
    :param reviewer: lxml node node
    :param default: default value is no node text
    :return: node text or None
    '''
    node = parent.find(tag)
    if node is None:
        return None
    if node.text is None:
        text = default
    else:
        text = node.text.strip()
    return text


def readValidXmlDoc(filename, expected_root_tag, XML_Schema_file, alt_root_tag='', alt_schema=None):
    '''
    Common code to read an XML file, validate it with an XML Schema, and return the XML doc object

    :param str XML_Schema_file: name of XML Schema file (local to package directory)
    '''
    if not os.path.exists(filename):
        raise IOError, 'file not found: ' + filename

    try:
        doc = etree.parse(filename)
    except (etree.XMLSyntaxError, etree.ParseError), exc:
        raise XmlSyntaxError, str(exc)

    try:
        root = doc.getroot()
        if root.tag not in (expected_root_tag, alt_root_tag):
            msg = 'expected=' + expected_root_tag
            msg += ' (or=' + alt_root_tag + ')'
            msg += ', received=' + root.tag
            raise IncorrectXmlRootTag(msg)
        try:
            if root.tag == expected_root_tag or alt_schema is None:
                validate(doc, XML_Schema_file)
            else:
                validate(doc, alt_schema)
        except etree.DocumentInvalid, exc:
            raise InvalidWithXmlSchema, str(exc)
    except Exception, exc:
        msg = 'In ' + filename + ': ' + traceback.format_exc()
        raise Exception, msg
    
    return doc


def validate(xml_tree, XSD_Schema_file):
    '''
    validate an XML document tree against an XML Schema file

    :param obj xml_tree: instance of etree._ElementTree
    :param str XSD_Schema_file: name of XSD Schema file (local to package directory)
    '''
    path = os.path.abspath(os.path.dirname(__file__))
    xsd_full_file_name = os.path.join(path, XSD_Schema_file)
    if not os.path.exists(xsd_full_file_name):
        raise IOError('Could not find XML Schema file: ' + XSD_Schema_file)
    
    xsd_doc = etree.parse(xsd_full_file_name)
    xsd = etree.XMLSchema(xsd_doc)

    return xsd.assertValid(xml_tree)
