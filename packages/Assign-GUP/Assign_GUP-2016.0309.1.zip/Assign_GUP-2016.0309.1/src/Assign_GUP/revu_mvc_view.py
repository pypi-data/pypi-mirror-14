
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
MVC View for reviewers

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import event_filters
import general_mvc_model
import history
import qt_utils
import resources
import reviewer_details
import signals
import topics

UI_FILE = 'listview.ui'
REVIEWERS_TEST_FILE = os.path.join('project', 'agup_project.xml')


class AGUP_Reviewers_View(QtGui.QWidget):
    '''
    Manage the list of Reviewers, including assignments of topic weights
    
    :param obj parent: instance of main_window.AGUP_MainWindow or None
    :param obj agup: instance of agup_data.AGUP_Data
    :param obj settings: instance of settings.ApplicationQSettings
    '''
    
    def __init__(self, parent=None, agup=None, settings=None):
        self.parent = parent
        self.topics = agup.topics
        self.settings = settings

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        
        self.setWindowTitle('Assign_GUP - Reviewers')
        self.listview_gb.setTitle('Reviewers')
        self.details_gb.setTitle('Reviewer Details')

        self.details_panel = reviewer_details.AGUP_ReviewerDetails(self, self.settings)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        self._init_topic_widgets(self.topics)

        if agup.reviewers is not None:
            self.setModel(agup.reviewers)
            if len(agup.reviewers) > 0:
                sort_name = agup.reviewers.keyOrder()[0]
                self.editReviewer(sort_name, None)
                self.selectFirstListItem()

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.details_panel.custom_signals.topicValueChanged.connect(self.onTopicValueChanged)
        self.details_panel.full_name.textEdited.connect(self.onDetailsModified)
        self.details_panel.sort_name.textEdited.connect(self.onDetailsModified)
        self.details_panel.phone.textEdited.connect(self.onDetailsModified)
        self.details_panel.email.textEdited.connect(self.onDetailsModified)
        self.details_panel.joined.textEdited.connect(self.onDetailsModified)
        self.details_panel.url.textEdited.connect(self.onDetailsModified)
        self.details_panel.notes.textChanged.connect(self.onDetailsModified)

        self.arrowKeysEventFilter = event_filters.ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)
        
        self.custom_signals = signals.CustomSignals()
    
    def _init_topic_widgets(self, topics_obj):
        '''
        '''
        self.details_panel.addTopics(topics_obj.getTopicList())

    def on_item_clicked(self, index):
        '''
        called when changing the selected Reviewer in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectModelByIndex(index, self.prior_selection_index)

    def onTopicValueChanged(self, sort_name, topic, value):
        '''
        called when user changed a topic value in the details panel
        '''
        self.reviewers.setTopicValue(str(sort_name), str(topic), value)
        self.custom_signals.recalc.emit()
        self.custom_signals.topicValueChanged.emit(sort_name, topic, value)
        self.details_panel.modified = True
    
    def onDetailsModified(self, *args):
        '''
        '''
        self.details_panel.modified = True
    
    def details_modified(self):
        '''OK to select a different reviewer now?'''
        return self.details_panel.modified

    def editReviewer(self, sort_name, prev_index):
        '''
        select Reviewer for editing as referenced by sort_name
        '''
        if self.details_modified():
            self.saveReviewerDetails()
            
        if sort_name is None:
            return
        panelist = self.reviewers.getReviewer(str(sort_name))

        self.details_panel.setFullName(panelist.getKey('full_name'))
        self.details_panel.setSortName(panelist.getKey('name'))
        self.details_panel.setPhone(panelist.getKey('phone'))
        self.details_panel.setEmail(panelist.getKey('email'))
        self.details_panel.setNotes(panelist.getKey('notes'))
        self.details_panel.setJoined(panelist.getKey('joined'))
        self.details_panel.setUrl(panelist.getKey('URL'))

        topics_list = panelist.getTopicList()
        if len(self.details_panel.topic_list) == 0:
            self._init_topic_widgets(panelist.topics)            # need to create topic widgets first
        for topic in topics_list:
            value = panelist.getTopic(topic)
            self.details_panel.setTopic(topic, value)
        # set reviewers
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected reviewer: ' + str(sort_name))
    
    def saveReviewerDetails(self):
        '''
        copied Reviewer details from editor panel to main data structure
        '''
        sort_name = str(self.details_panel.getSortName())
        if len(sort_name) == 0:
            return
        panelist = self.reviewers.getReviewer(sort_name)    # raises IndexError if not found

        kv = dict(
            full_name=self.details_panel.getFullName,
            name=self.details_panel.getSortName,
            phone=self.details_panel.getPhone,
            email=self.details_panel.getEmail,
            notes=self.details_panel.getNotes,
            joined=self.details_panel.getJoined,
            URL=self.details_panel.getUrl,
        )
        for k, v in kv.items():
            panelist.setKey(k, v())
        history.addLog('saved reviewer details: ' + sort_name)
        self.details_panel.modified = False

    def selectModelByIndex(self, curr, prev):
        '''
        select Reviewer for editing as referenced by QListView index
        
        :param index curr: sort_name string of current selected reviewer
        :param index prev: QListView index of previously selected reviewer
        '''
        sort_name = self.index_to_ID(curr)
        if sort_name is None:
            return
        self.editReviewer(sort_name, prev)
    
    def selectFirstListItem(self):
        '''
        '''
        idx = self.listView.indexAt(QtCore.QPoint(0,0))
        self.listView.setCurrentIndex(idx)
        return idx
    
    def index_to_ID(self, index):
        '''convert QListView index to sort_name string'''
        obj = index.data().toPyObject()
        if obj is None:
            return obj
        return str(obj)
        
    def setModel(self, model):
        '''
        '''
        self.reviewers = model
        self.reviewers_model = general_mvc_model.AGUP_MVC_Model(self.reviewers, parent=self)
        self.listView.setModel(self.reviewers_model)
    
    def isReviewerListModified(self):
        '''
        '''
        return self.details_panel.modified

    def closeEvent(self, event):
        '''
        '''
        self.saveReviewerDetails()
        self.details_panel.saveSplitterDetails()
        self.saveWindowGeometry()
        event.accept()
    
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
    
    def update(self):
        # not called
        history.addLog(self.__class__.__name__ + '.update()', False)


def main():
    '''simple starter program to develop this code'''
    import sys
    import os
    import agup_data

    agup = agup_data.AGUP_Data()
    agup.openPrpFile('project/agup_project.xml')

    app = QtGui.QApplication(sys.argv)
    mw = AGUP_Reviewers_View(None, agup)
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
