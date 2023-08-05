
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
show the About box
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import __init__
import history
import plainTextEdit
import resources

UI_FILE = 'about.ui'
DOCS_URL = 'http://Assign_GUP.readthedocs.org'
ISSUES_URL = 'https://github.com/prjemian/assign_gup/issues'
LICENSE_FILE = 'LICENSE'


class InfoBox(QtGui.QDialog):
    '''
    a Qt GUI for the About box
    '''

    def __init__(self, parent=None, settings=None):
        self.settings = settings
        QtGui.QDialog.__init__(self, parent)
        resources.loadUi(UI_FILE, baseinstance=self)
        
        self.license_box = None
        
        self.version.setText('software version: ' + str(__init__.__version__))

        self.docs_pb.clicked.connect(self.doDocsUrl)
        self.issues_pb.clicked.connect(self.doIssuesUrl)
        self.license_pb.clicked.connect(self.doLicense)
        self.setModal(False)

    def closeEvent(self, event):
        '''
        called when user clicks the big [X] to quit
        '''
        if self.license_box is not None:
            self.license_box.close()
        event.accept() # let the window close

    def doUrl(self, url):
        '''opening URL in default browser'''
        url = QtCore.QUrl(url)
        service = QtGui.QDesktopServices()
        service.openUrl(url)

    def doDocsUrl(self):
        '''opening documentation URL in default browser'''
        history.addLog('opening documentation URL in default browser')
        self.doUrl(DOCS_URL)

    def doIssuesUrl(self):
        '''opening issues URL in default browser'''
        history.addLog('opening issues URL in default browser')
        self.doUrl(ISSUES_URL)

    def doLicense(self):
        '''show the license'''
        if self.license_box is None:
            history.addLog('opening License in new window')
            #history.addLog('DEBUG: ' + LICENSE_FILE)
            lfile = resources.resource_file(LICENSE_FILE, '.')
            #history.addLog('DEBUG: ' + lfile)
            license_text = open(lfile, 'r').read()
            #history.addLog('DEBUG: ' + license_text)
            ui = plainTextEdit.TextWindow(None, 
                                          'LICENSE', 
                                          license_text, 
                                          self.settings)
            ui.setMinimumSize(700, 500)
            self.license_box = ui
            #ui.setWindowModality(QtCore.Qt.ApplicationModal)
            #history.addLog('DEBUG: ' + str(ui))
        self.license_box.show()
        #history.addLog('DEBUG: ui.show() done')
