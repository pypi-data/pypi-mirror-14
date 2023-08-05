
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Helper routines for Qt
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtGui
else:
    from PyQt4 import QtGui


BACKGROUND_DEFAULT = '#efefef'

#             QPushButton { 
#                    background-color: red;
#                    color: black;
#                    text-align: center;
#                    }


def setButtonBackground(widget, color = BACKGROUND_DEFAULT):
    '''
    '''
    css = 'background-color: %s;' % color
    widget.setStyleSheet(css)


def setWidgetBackground(widget, color = BACKGROUND_DEFAULT):
    '''
    change the background color of a Qt widget
    
    :param str color: specified as name (mintcream), hex RGB (#dea)
    '''
    if widget is not None:
        palette = QtGui.QPalette()
        palette.setColor(widget.backgroundRole(), QtGui.QColor(color))
        widget.setPalette(palette)
