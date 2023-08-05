
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
edit the template to send emails, include editor for keyword substitutions

Provide tools to:

* manage list of substitution keywords
* manage values of substitution keywords
* display as read-only those substitution keywords defined for each reviewer
* provide editor for email template letter
* show example email with subsitutions applied

The email template is stored in the project file.

The substitution keyword dictionary is (at present) 
stored in the settings file.
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui
import re

import email_template
import history
import resources
import signals


UI_FILE = 'editor_email_template.ui'
DISABLED_STYLE = 'background: #eee'
MINIMUM_KEY_LENGTH = 3


class Editor(QtGui.QWidget):
    '''
    '''
    
    def __init__(self, parent, agup, settings=None):
        self.parent = parent
        self.agup = agup
        self.settings = settings
        self.keyword_dict = self.agup.email.keyword_dict
        self.current_key = None
        self.signals = signals.CustomSignals()

        QtGui.QWidget.__init__(self, parent)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        self.restoreSplitterDetails()

        self.listWidget.addItems(sorted(self.keyword_dict.keys()))
        self.listWidget.addItems(sorted(email_template.REVIEWER_FIELDS.keys()))
        self.template.setPlainText(self.agup.email.email_template)

        self.selectFirstKeyword()

        self.pb_add.clicked.connect(self.onAdd)
        self.pb_delete.clicked.connect(self.onDelete)

        self.listWidget.currentItemChanged.connect(self.doCurrentItemChanged)
        self.template.textChanged.connect(self.doTemplateTextChanged)
        self.plainTextEdit.textChanged.connect(self.doKeywordTextChanged)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.disabled_style = DISABLED_STYLE
        self.enabled_style = self.plainTextEdit.styleSheet()
        
        self.doMerge()
        self.show()
    
    def onAdd(self, *args, **kw):
        '''
        add keyword substitution
        
        Keywords are allowed to start with a letter or "_", 
        then can have numbers also.  All letters must be uppercase.
        
        Substitutions may be any text, including any white space.
        
        Strings must have a minimum length of MINIMUM_KEY_LENGTH (3) characters.
        '''
        key, ok = QtGui.QInputDialog.getText(self, 
                                             'new keyword', 
                                             'type a new keyword substitution')
        key = str(key).strip()
        if ok and len(key) > MINIMUM_KEY_LENGTH:
            match_pattern = '^[_A-Z]+[_A-Z0-9]*$'
            pattern = re.compile(match_pattern)
            if pattern.match(key) is not None and key not in self.keyword_dict.keys():
                if key not in email_template.REVIEWER_FIELDS.keys():
                    self.keyword_dict[key] = ''
                    self.listWidget.addItem(key)

    def onDelete(self, *args, **kw):
        '''
        delete the selected key
        
        check that self.current_key is not None
        then delete that one and reset to next in list
        '''
        key = self.current_key
        if key is None: return
        if key not in self.keyword_dict.keys(): return

        box = QtGui.QMessageBox()
        box.setText('Delete: ' + key)
        box.setInformativeText('Delete this substitution key?')
        box.setStandardButtons(QtGui.QMessageBox.Ok 
                               | QtGui.QMessageBox.Cancel)
        box.setDefaultButton(QtGui.QMessageBox.Ok)
        ret = box.exec_()

        if ret != QtGui.QMessageBox.Ok: return

        del self.keyword_dict[key]
        curr = self.listWidget.currentItem()
        if curr is not None:
            row = self.listWidget.row(curr)
            self.listWidget.takeItem(row)
        self.current_key = None
        self.selectFirstKeyword()

    def doCurrentItemChanged(self, widget_item):
        '''
        '''
        self.current_key = key = str(widget_item.text())
        if key in self.keyword_dict.keys():
            value = self.keyword_dict[key]
        else:
            value = email_template.REVIEWER_FIELDS[key]
        self.plainTextEdit.setPlainText(value)
        # check if keyword is to be filled in from reviewer (or proposal) data
        if key in email_template.REVIEWER_FIELDS.keys():
            self.plainTextEdit.setReadOnly(True)
            self.plainTextEdit.setStyleSheet(self.disabled_style)
            self.plainTextEdit.setToolTip('this value is set for each reviewer')
        else:
            self.plainTextEdit.setReadOnly(False)
            self.plainTextEdit.setStyleSheet(self.enabled_style)
            self.plainTextEdit.setToolTip('you may edit this value')
    
    def doKeywordTextChanged(self, *args, **kw):
        '''
        '''
        if self.current_key is not None and self.current_key in self.keyword_dict.keys():
            s = str(self.plainTextEdit.toPlainText())
            if s != self.keyword_dict[self.current_key]:
                self.keyword_dict[self.current_key] = s
                self.signals.changed.emit()
                self.doMerge()
    
    def doTemplateTextChanged(self, *args, **kw):
        '''
        '''
        s = str(self.template.toPlainText())
        if s != self.agup.email.email_template:
            self.agup.email.email_template = s
            self.signals.changed.emit()
            self.doMerge()
    
    def doMerge(self):
        '''
        '''
        text = self.agup.email.mail_merge(**email_template.REVIEWER_FIELDS)
        self.mail_merge.setPlainText(text)

    def saveWindowGeometry(self):
        '''
        remember where the window was
        '''
        if self.settings is not None:
            self.settings.saveWindowGeometry(self, 'TemplateEditor_geometry')

    def restoreWindowGeometry(self):
        '''
        put the window back where it was
        '''
        if self.settings is not None:
            self.settings.restoreWindowGeometry(self, 'TemplateEditor_geometry')

    def saveSplitterDetails(self):
        '''
        remember where the splitters were
        '''
        def handler(group, splitter):
            sizes = map(int, splitter.sizes())
            self.settings.setKey(group + '/widths', ' '.join(map(str, sizes)))

        if self.settings is not None:
            handler('TemplateEditor_v_splitter', self.v_splitter)
            handler('TemplateEditor_h_splitter', self.h_splitter)
            handler('TemplateEditor_splitter3', self.splitter3)

    def restoreSplitterDetails(self):
        '''
        put the splitters back where they were
        '''
        def handler(group, splitter):
            sizes = self.settings.getKey(group + '/widths')
            if sizes is not None:
                splitter.setSizes(map(int, str(sizes).split()))

        if self.settings is not None:
            handler('TemplateEditor_v_splitter', self.v_splitter)
            handler('TemplateEditor_h_splitter', self.h_splitter)
            handler('TemplateEditor_splitter3', self.splitter3)

    def closeEvent(self, event):
        '''
        '''
        self.saveWindowGeometry()
        self.saveSplitterDetails()
        event.accept()
        self.close()

    def selectFirstKeyword(self):
        '''
        '''
        idx = self.listWidget.indexAt(QtCore.QPoint(0,0))
        self.listWidget.setCurrentIndex(idx)

        if len(self.keyword_dict):
            self.current_key = sorted(self.keyword_dict.keys())[0]
            value = self.keyword_dict[self.current_key]
        else:
            self.current_key = sorted(email_template.REVIEWER_FIELDS.keys())[0]
            value = email_template.REVIEWER_FIELDS[self.current_key]
        self.plainTextEdit.setPlainText(value)

        return idx
    

# if __name__ == '__main__':
#     import os
#     import sys
#     import pprint
#     import agup_data
# 
#     agup = agup_data.AGUP_Data()
#     agup.openPrpFile('project/agup_project.xml')
# 
#     app = QtGui.QApplication(sys.argv)
#     mw = Editor(None, agup)
#     _r = app.exec_()
#     pprint.pprint(agup.email.keyword_dict)
#     print agup.email.email_template
#     sys.exit(_r)
