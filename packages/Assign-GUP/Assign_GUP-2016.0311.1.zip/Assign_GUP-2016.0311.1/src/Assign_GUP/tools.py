
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
common tools used in various places
'''

XML_CODEPOINT = 'ISO-8859-1'
CODEPOINT_LIST = ('cp1251', 'cp1252', 'utf8', 'iso-8859-1')


def text_decode(source):
    '''try decoding ``source`` with various known codepoints to unicode'''
    for encoding in CODEPOINT_LIST:  # walk through a list of codepoints
        try:
            return source.decode(encoding, 'replace')
        except (ValueError, UnicodeError), _exc:
            continue
        except Exception, _exc:
            continue
    return source


def text_encode(source):
    '''encode ``source`` using the default codepoint'''
    return source.encode(encoding=XML_CODEPOINT, errors='ignore')
