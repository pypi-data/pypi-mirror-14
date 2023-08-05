
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

r'''
Custom Qt4 signals

====================  ===============  =====================
signal                args             comments
====================  ===============  =====================
changed                                template editor
checkBoxGridChanged                    reviewer assignment
closed                                 topics_editor
recalc                                 dotProduct
topicValueChanged     str, str, float  reviewer or proposal
====================  ===============  =====================

'''


import datetime
import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore


class CustomSignals(QtCore.QObject):
    '''custom signals'''

    changed = QtCore.pyqtSignal()
    checkBoxGridChanged = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal()                # topics_editor
    recalc = QtCore.pyqtSignal()
    topicValueChanged = QtCore.pyqtSignal(str, str, float)
