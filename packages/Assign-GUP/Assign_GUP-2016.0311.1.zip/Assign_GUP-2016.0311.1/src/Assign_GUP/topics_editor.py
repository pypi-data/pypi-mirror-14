
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
GUI to edit the list of topics
'''


import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui
import history
import qt_utils
import resources
import signals
import topics


UI_FILE = 'topics_editor.ui'


class AGUP_TopicsEditor(QtGui.QDialog):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent=None, topics_list=None, settings=None):
        self.parent = parent
        self.topics = topics.Topics()
        self.topics.addTopics(topics_list)
        self.settings = settings

        QtGui.QDialog.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()

        self.setWindowTitle('AGUP List of Topics')
        self.listWidget.addItems(self.topics.getTopicList())

        self.add_pb.clicked.connect(self.onAdd)
        self.delete_pb.clicked.connect(self.onDelete)
        
        # select the first item in the list
        idx = self.listWidget.indexAt(QtCore.QPoint(0,0))
        self.listWidget.setCurrentIndex(idx)

        self.custom_signals = signals.CustomSignals()
    
    def getTopicList(self):
        '''
        when all editing is complete, call this method to get the final list
        '''
        return self.topics.getTopicList()

    def onAdd(self, *args, **kw):
        '''
        add the text in the entry box to the list of topics
        '''
        topic, ok = QtGui.QInputDialog.getText(self, 
                                             'new topic', 
                                             'type a new topic')
        topic = str(topic).strip()
        if ok and  topic and not self.topics.exists(topic):
            self.listWidget.addItem(topic)
            self.topics.add(topic)
            self.listWidget.sortItems()

    def onDelete(self, *args):
        '''
        remove the selected item from the list of topics
        '''
        curr = self.listWidget.currentItem()
        if curr is not None:
            box = QtGui.QMessageBox()
            box.setText('Delete topic: ' + str(curr.text()))
            box.setInformativeText('Delete this topic?')
            box.setStandardButtons(QtGui.QMessageBox.Ok 
                                   | QtGui.QMessageBox.Cancel)
            box.setDefaultButton(QtGui.QMessageBox.Ok)
            ret = box.exec_()
    
            if ret != QtGui.QMessageBox.Ok: return

            row = self.listWidget.row(curr)
            self.listWidget.takeItem(row)
            self.topics.remove(str(curr.text()))
    
    def onCloseButton(self, event):
        ''' '''
        self.close()
    
    def closeEvent(self, event):
        ''' '''
        self.custom_signals.closed.emit()   # this window is closing - needed?
        self.saveWindowGeometry()
        event.accept()
        self.close()
    
    def saveWindowGeometry(self):
        '''
        remember where the window was
        '''
        if self.settings is not None:
            self.settings.saveWindowGeometry(self)

    def restoreWindowGeometry(self):
        '''
        put the window back where it was
        '''
        if self.settings is not None:
            self.settings.restoreWindowGeometry(self)
