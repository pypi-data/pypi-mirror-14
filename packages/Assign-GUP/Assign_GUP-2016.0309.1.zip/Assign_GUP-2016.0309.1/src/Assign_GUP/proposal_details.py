
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
QtGui widget to edit one Proposal instance

.. rubric:: :class:`AGUP_ProposalDetails`

adds one row of widgets for possible Reviewer of Proposal

====================================================  ============================================================
Method                                                Description
====================================================  ============================================================
:meth:`~AGUP_ProposalDetails.addReviewer`             add a Reviewer to the panel
====================================================  ============================================================
'''


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtGui
else:
    from PyQt4 import QtGui

import history
import prop_revu_grid
import resources
import signals
import topic_slider
import topics


UI_FILE = 'proposal_details.ui'


#         self.reviewers_gb.layout().setReviewersValues(self.agup.reviewers)


class AGUP_ProposalDetails(QtGui.QWidget):
    '''
    QtGui widget to edit one Proposal instance
    '''

    def __init__(self, parent=None, settings=None, agup=None):
        '''
        '''
        self.parent = parent
        self.settings = settings
        self.agup = agup

        QtGui.QWidget.__init__(self, parent)
        resources.loadUi(UI_FILE, self)
        self.restoreSplitterDetails()

        self.modified = False
        self.topic_list = []
        self.topic_widgets = {}
        self.reviewer_list = []
        # self.reviewer_widgets = {}    # not used

        layout = prop_revu_grid.ReviewerAssignmentGridLayout(None, self.agup)
        self.reviewers_gb.setLayout(layout)
        layout.custom_signals.checkBoxGridChanged.connect(self.onAssignmentsChanged)

        self.custom_signals = signals.CustomSignals()
    
    def addReviewers(self, reviewers):
        '''
        Add the list of Reviewers to the details panel
        '''
        self.reviewers_gb.layout().addReviewers(reviewers)
    
    def onAssignmentsChanged(self):
        '''
        called when a reviewer assignment checkbox has been changed
        '''
        self.custom_signals.checkBoxGridChanged.emit()
    
    def onTopicValueChanged(self, topic):
        ''' '''
        value = self.topic_widgets[topic].getValue()
        history.addLog("topic (" + topic + ") value changed: " + str(value))
        self.modified = True
        prop_id = str(self.getProposalId())
        self.custom_signals.topicValueChanged.emit(prop_id, str(topic), value)
    
    def addTopic(self, topic, value):
        '''
        '''
        if topic not in self.topic_list:
            self.topic_list.append(topic)
        row = self.topic_list.index(topic)
        topicslider = topic_slider.AGUP_TopicSlider(self.topic_layout, row, topic, value)
        self.topic_widgets[topic] = topicslider
        topicslider.slider.valueChanged.connect(lambda: self.onTopicValueChanged(topic))
    
    def addTopics(self, topic_list):
        '''
        '''
        for topic in topic_list:
            self.addTopic(topic, topics.DEFAULT_TOPIC_VALUE)

    def setTopic(self, key, value):
        '''
        '''
        if key not in self.topic_list:
            raise KeyError, 'unknown Topic: ' + key
        if value < 0 or value > 1:
            raise ValueError, 'Topic value must be between 0 and 1, given' + str(value)
        self.topic_widgets[key].setValue(value)
        self.topic_widgets[key].onValueChange(value)    # sets the slider
        self.modified = True
    
    def clear(self):
        '''
        '''
        self.setProposalId('')
        self.setProposalTitle('')
        self.setReviewPeriod('')
        self.setSpkName('')
        self.setFirstChoiceBl('')
        self.setSubjects('')
    
    def setAll(self, prop_id, title, period, speaker, choice, subjects):
        '''
        '''
        self.setProposalId(prop_id)
        self.setProposalTitle(title)
        self.setReviewPeriod(period)
        self.setSpkName(speaker)
        self.setFirstChoiceBl(choice)
        self.setSubjects(subjects)
    
    def setupProposal(self, proposal):
        '''
        install proposal data in the editor's widgets
        '''
        kv = dict(
            proposal_id = self.setProposalId,
            proposal_title = self.setProposalTitle,
            review_period = self.setReviewPeriod,
            spk_name = self.setSpkName,
            first_choice_bl = self.setFirstChoiceBl,
            subjects = self.setSubjects,
        )

        layout = self.reviewers_gb.layout()
        layout.proposal = proposal

        # set all the text entry widget fields
        for k, v in kv.items():
            v(proposal.getKey(str(k)))
        # set all the topic values
        for topic in proposal.getTopicList():
            v = proposal.getTopic(topic)
            self.topic_widgets[topic].setValue(v)
            self.topic_widgets[topic].onValueChange(v)

        layout.setProposal(proposal)

    def getProposalId(self):
        ''' '''
        return self.proposal_id.text()

    def setProposalId(self, value):
        ''' '''
        self.proposal_id.setText(value)
        self.modified = True
    
    def setProposalTitle(self, value):
        ''' '''
        self.proposal_title.setPlainText(value)
        self.modified = True

    def setReviewPeriod(self, value):
        ''' '''
        self.review_period.setText(value)
        self.modified = True

    def setSpkName(self, value):
        ''' '''
        self.spk_name.setText(value)
        self.modified = True

    def setFirstChoiceBl(self, value):
        ''' '''
        self.first_choice_bl.setText(value)
        self.modified = True

    def setSubjects(self, value):
        ''' '''
        self.subjects.setPlainText(value)
        self.modified = True

    def saveSplitterDetails(self):
        ''' '''
        if self.settings is not None:
            self.settings.saveSplitterDetails(self)

    def restoreSplitterDetails(self):
        ''' '''
        if self.settings is not None:
            self.settings.restoreSplitterDetails(self)
    
    def update(self):
        ''' '''
        history.addLog(self.__class__.__name__ + '.update()', False)
        grid = self.reviewers_gb.layout()
#         grid.update()


def project_main():
    import sys
    import os
    import agup_data

    app = QtGui.QApplication(sys.argv)

    testfile = os.path.abspath('project/agup_project.xml')
    test_gup_id = str(941*9*5)

    agup = agup_data.AGUP_Data()    
    agup.openPrpFile(testfile)
    proposal = agup.proposals.proposals[test_gup_id]

    mw = AGUP_ProposalDetails(agup=agup)
    mw.addTopics(agup.topics.getTopicList())
    mw.addReviewers(agup.reviewers)
    mw.setupProposal(proposal)
  
    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    # AGUP_main()
    project_main()
