
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
event filters for certain MVC widgets such as QListView
'''

import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore

NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)


class ArrowKeysEventFilter(QtCore.QObject):
    '''
    watches for ArrowUp and ArrowDown (navigator keys) to change selection in QtCore.QAbstractListModel
    '''

    def eventFilter(self, listView, event):
        '''
        custom event filter
        '''
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                prev = listView.currentIndex()
                listView.keyPressEvent(event)
                curr = listView.currentIndex()
                parent = listView.parent().parent()     # FIXME: fragile!
                parent.selectModelByIndex(curr, prev)
                return True
        return False
