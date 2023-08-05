
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
MVC View for proposals

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
import history
import general_mvc_model
import proposal_details
import qt_utils
import signals
import resources
import topics

UI_FILE = 'listview.ui'
PROPOSALS_TEST_FILE = os.path.join('project', '2015-2', 'proposals.xml')


class AGUP_Proposals_View(QtGui.QWidget):
    '''
    Manage the list of proposals, including assignments of topic weights and reviewers
    
    :param obj parent: instance of main_window.AGUP_MainWindow or None
    :param obj agup: instance of agup_data.AGUP_Data
    :param obj settings: instance of settings.ApplicationQSettings
    '''
    
    def __init__(self, parent=None, agup=None, settings=None):
        self.parent = parent
        self.reviewers = agup.reviewers
        self.topics = agup.topics
        self.settings = settings

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        
        self.setWindowTitle('Assign_GUP - Proposals')
        self.listview_gb.setTitle('Proposals')
        self.details_gb.setTitle('Proposal Details')

        self.details_panel = proposal_details.AGUP_ProposalDetails(parent=self, 
                                                                   settings=self.settings, 
                                                                   agup=agup)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        self._init_topic_widgets(self.topics)
        self.details_panel.addReviewers(self.reviewers)

        if agup.proposals is not None:
            self.setModel(agup.proposals)
            if len(agup.proposals) > 0:
                prop_id = agup.proposals.keyOrder()[0]
                self.editProposal(prop_id, None)
                self.selectFirstListItem()

        self.custom_signals = signals.CustomSignals()

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.details_panel.custom_signals.topicValueChanged.connect(self.onTopicValueChanged)
        self.details_panel.custom_signals.checkBoxGridChanged.connect(self.onAssignmentsChanged)

        self.arrowKeysEventFilter = event_filters.ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)
    
    def _init_topic_widgets(self, topics_obj):
        self.details_panel.addTopics(topics_obj.getTopicList())

    def on_item_clicked(self, index):
        '''
        called when changing the selected Proposal in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectModelByIndex(index, self.prior_selection_index)

    def onTopicValueChanged(self, prop_id, topic, value):
        '''
        called when user changed a topic value in the details panel
        '''
        self.proposals.setTopicValue(str(prop_id), str(topic), value)
        rvwr_grid = self.details_panel.reviewers_gb.layout()
        rvwr_grid.calcDotProducts()
        self.details_panel.modified = True
        self.custom_signals.topicValueChanged.emit(prop_id, topic, value)

    def onAssignmentsChanged(self):
        '''
        called when a reviewer assignment checkbox has been changed
        '''
        self.custom_signals.checkBoxGridChanged.emit()
    
    def details_modified(self):
        '''OK to select a different proposal now?'''
        return self.details_panel.modified

    def editProposal(self, prop_id, prev_prop_index):
        '''
        select Proposal for editing as referenced by ID number
        '''
        if prop_id is None:
            return
        proposal = self.proposals.getProposal(str(prop_id))
        self.details_panel.setupProposal(proposal)
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected proposal: ' + str(prop_id))
    
    def selectFirstListItem(self):
        ''' '''
        idx = self.listView.indexAt(QtCore.QPoint(0,0))
        self.listView.setCurrentIndex(idx)
        return idx
    
    def index_to_ID(self, index):
        '''convert QListView index to GUP ID string'''
        obj = index.data().toPyObject()
        if obj is None:
            return obj
        return str(obj)

    def selectModelByIndex(self, curr, prev):
        '''
        select Proposal for editing as referenced by QListView index
        
        :param index curr: GUP ID string of current selected proposal
        :param index prev: QListView index of previously selected proposal
        '''
        prop_id = self.index_to_ID(curr)
        if prop_id is None:
            return
        self.editProposal(prop_id, prev)
        
    def setModel(self, model):
        ''' '''
        self.proposals = model
        self.proposals_model = general_mvc_model.AGUP_MVC_Model(self.proposals, parent=self)
        self.listView.setModel(self.proposals_model)

        # select the first item in the list
        idx = self.selectFirstListItem()
        self.prior_selection_index = idx
        self.selectModelByIndex(idx, None)
    
    def isProposalListModified(self):
        ''' '''
        return self.details_panel.modified

    def recalc(self):
        '''
        recalculate dot products
        '''
        rvwr_grid = self.details_panel.reviewers_gb.layout()
        rvwr_grid.calcDotProducts()

    def closeEvent(self, event):
        '''in response to user requesting the window be closed'''
        self.saveWindowGeometry()
        self.details_panel.saveSplitterDetails()
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
    
    def update(self):
        ''' '''
        history.addLog(self.__class__.__name__ + '.update()', False)
#         self.details_panel.update()
