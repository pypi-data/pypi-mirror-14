
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
widgets of one Reviewer of one Proposal instance

.. rubric:: :class:`ProposalReviewerRow`

adds one row of widgets for possible Reviewer of Proposal

====================================================  ============================================================
Method                                                Description
====================================================  ============================================================
:meth:`~ProposalReviewerRow.getAssignment`            return which type of reviewer this is (0, 1, 2)
:meth:`~ProposalReviewerRow.setAssignment`            define which type of reviewer this is (0, 1, 2)
:meth:`~ProposalReviewerRow.setValue`                 set dotProduct value as percentage
:meth:`~ProposalReviewerRow.setEnabled`               enable/disable the checkboxes based on Reviewer eligibility
:meth:`~ProposalReviewerRow.setNumberAssigned`        show the number of assigned proposals with given role (1 | 2)
:meth:`~ProposalReviewerRow.dotProduct`               compute and set widget with dot product of reviewer & proposal topics
====================================================  ============================================================

.. rubric:: :class:`ReviewerAssignmentGridLayout`

QGridLayout of possible Reviewers of Proposal

====================================================  ============================================================
Method                                                Description
====================================================  ============================================================
:meth:`~ReviewerAssignmentGridLayout.addReviewer`     add controls for one Reviewer to the grid
:meth:`~ReviewerAssignmentGridLayout.addReviewers`    add list of Reviewers to the grid
:meth:`~ReviewerAssignmentGridLayout.setEnabled`      enable/disable one Reviewer
:meth:`~ReviewerAssignmentGridLayout.setProposal`     specify the Proposal associated with this grid
:meth:`~ReviewerAssignmentGridLayout.setAssignment`   define the type for a named Reviewer 
:meth:`~ReviewerAssignmentGridLayout.onCheck`         ensure only one reviewer is either primary or secondary
:meth:`~ReviewerAssignmentGridLayout.setValue`        set dotProduct value of a named Reviewer as percentage
====================================================  ============================================================

-----
'''


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import history
import proposal
import signals


class ProposalReviewerRow(QtCore.QObject):
    '''
    Adds a row of widgets to an existing grid layout for one Reviewer of one Proposal instance
    '''

    def __init__(self, parent, layout, reviewer, proposal):
        '''
        :param obj parent: owner (a QWidget subclass)
        :param obj layout: layout in which to place these widgets
        :param obj reviewer: instance of reviewer.AGUP_Reviewer_Data
        :param obj proposal: instance of proposal.AGUP_Proposal_Data
        '''
        self.parent = parent
        self.layout = layout
        self.reviewer = reviewer
        self.proposal = proposal
        self.enabled = False

        QtCore.QObject.__init__(self, parent)
        QtCore.qInstallMsgHandler(self._handler_)

        self.comfort = ""
        self.custom_signals = signals.CustomSignals()
        self._init_controls_()
        self.dotProduct()
    
    def _handler_(self, msg_type, msg_string):
        if msg_type == QtCore.QtDebugMsg:
            adjective = 'Debug'
        elif msg_type == QtCore.QtWarningMsg:
            adjective = 'Warning'
        elif msg_type == QtCore.QtCriticalMsg:
            adjective = 'Critical'
        elif msg_type == QtCore.QtFatalMsg:
            adjective = 'Fatal'
        history.addLog('QtCore.qInstallMsgHandler-' + adjective + ': ' + msg_string)

    def _init_controls_(self):
        '''
        Build one row of the GUI panel with a reviewer for this proposal::

            [ ] 5    [ ] 0      1%        I. M. A. Reviewer
        
        '''
        # FIXME: on LinuxMint, checkboxes generate this error
        # Gtk-CRITICAL **: IA__gtk_widget_get_direction: assertion 'GTK_IS_WIDGET (widget)' failed
        #
        # see: https://github.com/prjemian/assign_gup/issues/15
        self.primary = QtGui.QCheckBox()
        self.num_primary = QtGui.QLabel()
        self.secondary = QtGui.QCheckBox()
        self.num_secondary = QtGui.QLabel()
        self.percentage = QtGui.QLabel()
        self.full_name = QtGui.QLabel(self.reviewer.getFullName())
        self.setValue(-1)

        w = self.layout.addWidget(self.primary)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignCenter)
        w = self.layout.addWidget(self.num_primary)
        # self.num_primary.setStyleSheet('text-align: center;')
        w = self.layout.addWidget(self.secondary)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignCenter)
        w = self.layout.addWidget(self.num_secondary)
        w = self.layout.addWidget(self.percentage)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignRight)
        w = self.layout.addWidget(self.full_name)

        self.primary.setEnabled(self.enabled)
        self.secondary.setEnabled(self.enabled)

        self.primary.setToolTip("check to select as primary reviewer (#1)")
        self.num_primary.setToolTip("number of proposals assigned as primary reviewer (#1)")
        self.secondary.setToolTip("check to select as secondary reviewer (#2)")
        self.num_secondary.setToolTip("number of proposals assigned as secondary reviewer (#2)")
        self.percentage.setToolTip("computed comfort factor of this reviewer with this proposal")

        self.primary.released.connect(lambda: self.onCheckBoxClick(self.primary))
        self.secondary.released.connect(lambda: self.onCheckBoxClick(self.secondary))
    
    def onCheckBoxClick(self, widget):
        '''
        either check box was clicked
        '''
        self.rowCheck(widget)
        self.custom_signals.checkBoxGridChanged.emit()
    
    def rowCheck(self, checkbox):
        '''
        ensure at most one checkbox (primary or secondary) is checked for this reviewer
        
        :param obj checkbox: instance of QCheckBox
        '''
        if checkbox == self.primary:
            if self.isPrimaryChecked():
                self.setSecondaryState(False)
        else:   # MUST be secondary, then
            if self.isSecondaryChecked():
                self.setPrimaryState(False)
    
    def setProposal(self, proposal):
        '''
        define the proposal to be used with this row
        '''
        self.proposal = proposal
    
    def getAssignment(self):
        '''
        report which type of reviewer this is
        
        =======   =======================
        returns   description
        =======   =======================
        0         unassigned
        1         primary reviewer (#1)
        2         secondary reviewer (#2)
        =======   =======================
        '''
        if self.isPrimaryChecked():
            return 1
        elif self.isSecondaryChecked():
            return 2
        return 0

    def setAssignment(self, code):
        '''
        define which type of reviewer this is
        
        ====   =======================
        code   description
        ====   =======================
        0      unassigned
        1      primary reviewer (#1)
        2      secondary reviewer (#2)
        ====   =======================
        
        :param int code: integer code (0 | 1 | 2)
        '''
        if code == 0:           # unassigned
            self.setPrimaryState(False)
            self.setSecondaryState(False)
        elif code == 1:
            self.setPrimaryState(True)
        elif code == 2:
            self.setSecondaryState(True)
        self.onCheckBoxClick(self.primary)
        self.onCheckBoxClick(self.secondary)

    def setNumberAssigned(self, number, role):
        '''show the number of assigned proposals with given role'''
        valid_roles = (1, 2)
        if role not in valid_roles:
            raise ValueError, 'unknown role: ' + str(role)
        (self.num_primary, self.num_secondary)[role-1].setText(str(number))

    def setValue(self, percentage):
        '''
        set the percentage value
        
        :param int percentage: dot product of reviewer and proposal topic strengths
        '''
        self.percentage.setText(str(percentage) + ' %')
    
    def isPrimaryChecked(self):
        return self.primary.checkState() != 0
    
    def setPrimaryState(self, state):
        if self.primary.isChecked() != state:
            self.primary.setChecked(state)
            if state:
                self.secondary.setChecked(False)
    
    def isSecondaryChecked(self):
        return self.secondary.checkState() != 0
    
    def setSecondaryState(self, state):
        if self.secondary.isChecked() != state:
            self.secondary.setChecked(state)
            if state:
                self.primary.setChecked(False)
    
    def setEnabled(self, state=True):
        if state != self.enabled:
            self.primary.setEnabled(state)
            self.secondary.setEnabled(state)
            self.enabled = state

    def dotProduct(self):
        r'''
        dot product of Proposal and Reviewer topic strengths, :math:`\vec{p} \cdot \vec{r}`
        
        Computes :math:`\vec{p} \cdot \vec{r}` where:
        
        * :math:`\vec{p}` is array of topic value strengths for Proposal
        * :math:`\vec{r}` is array of topic value strengths for Reviewer
        
        '''
        if self.enabled and self.proposal and self.reviewer:
            dot = self.proposal.topics.dotProduct(self.reviewer.topics)
        else:
            dot = 0.0
        self.setValue(int(100*dot+0.5))
    
    def update(self):
        ''' '''
        # TODO: update the checkboxes
        history.addLog(self.__class__.__name__ + '.update()', False)


class ReviewerAssignmentGridLayout(QtGui.QGridLayout):
    '''
    display and manage the assignment checkboxes and reported percentages for each reviewer on this proposal
    '''
    
    def __init__(self, parent, agup):
        self.parent = parent
        self.agup = agup
        self.proposal = None
        self.reviewers = None

        QtGui.QGridLayout.__init__(self, parent)
        self.custom_signals = signals.CustomSignals()

        self._init_basics()
    
    def _init_basics(self):
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 1)
        self.setColumnStretch(2, 1)
        self.setColumnStretch(3, 1)
        self.setColumnStretch(4, 1)
        self.setColumnStretch(5, 3)
        style = 'background: #888; color: white;' #  margin: auto; width: 50%; text-align: center;
        self.addWidget(QtGui.QLabel('R1', styleSheet=style))
        self.addWidget(QtGui.QLabel('#1', styleSheet=style))
        self.addWidget(QtGui.QLabel('R2', styleSheet=style))
        self.addWidget(QtGui.QLabel('#2', styleSheet=style))
        self.addWidget(QtGui.QLabel('%', styleSheet=style))
        self.addWidget(QtGui.QLabel('Reviewer Name', styleSheet=style))
        self.rvwr_widgets = {}
    
    def addReviewer(self, rvwr):
        '''
        add this reviewer object for display
        '''
        row_widget = ProposalReviewerRow(self.parent, self, rvwr, self.proposal)
        row_widget.custom_signals.checkBoxGridChanged.connect(lambda: self.onCheck(row_widget))
        row_widget.setNumberAssigned(0, 1)
        row_widget.setNumberAssigned(0, 2)
        return row_widget

    def addReviewers(self, reviewers):
        '''
        add a list of reviewers
        '''
        self.rvwr_widgets = {}
        self.reviewers = reviewers
        for rvwr in reviewers:
            if rvwr is not None:
                self.rvwr_widgets[rvwr.getSortName()] = self.addReviewer(rvwr)

    def setReviewersValues(self, reviewers):
        '''
        set the widget values for all Reviewers
        '''
        for rvwr in reviewers:
            if self.proposal is None or rvwr is None:
                if rvwr is not None:
                    sort_name = rvwr.getSortName()
                    row_widget = self.rvwr_widgets[sort_name]
                    row_widget.setEnabled(False)
                    row_widget.setAssignment(0)
            else:
                sort_name = rvwr.getSortName()
                full_name = rvwr.getFullName()
                row_widget = self.rvwr_widgets[sort_name]
                row_widget.setProposal(self.proposal)
                eligible = full_name in self.proposal.eligible_reviewers
                row_widget.setEnabled(eligible)
                assignment = None
                if eligible:
                    assignment = self.proposal.eligible_reviewers[full_name]
                row_widget.setAssignment(assignment or 0)
                row_widget.dotProduct()
                dot = self.proposal.topics.dotProduct(rvwr.topics)
            
            self.updateNumbersOfAssignedProposals()

    def updateNumbersOfAssignedProposals(self):
        '''
        update the numbers of assigned proposals shown for each reviewer and each role
        '''
        if self.agup is not None and self.agup.proposals is not None:
            for row_widget in self.rvwr_widgets.values():
                rvwr = row_widget.reviewer
                n1 = rvwr.getAssignments(self.agup.proposals, proposal.PRIMARY_REVIEWER_ROLE)
                n2 = rvwr.getAssignments(self.agup.proposals, proposal.SECONDARY_REVIEWER_ROLE)
                row_widget.setNumberAssigned(len(n1), proposal.PRIMARY_REVIEWER_ROLE)
                row_widget.setNumberAssigned(len(n2), proposal.SECONDARY_REVIEWER_ROLE)

    def setProposal(self, proposal):
        '''
        declare which proposal is associated with this grid
        '''
        self.proposal = proposal
        self.setReviewersValues(self.reviewers)
    
    def setAssignment(self, sort_name, code):
        '''
        define which type of reviewer this is
        
        :param str sort_name: reviewer's identifying key
        :param int code: integer code (0 | 1 | 2)
        '''
        self.rvwr_widgets[sort_name].setAssignment(code)
    
    def setValue(self, sort_name, percentage):
        '''
        set the percentage value
        '''
        widget = self.rvwr_widgets[sort_name]
        widget.setValue(percentage)

    def onCheck(self, row_widget):
        '''
        ensure only one reviewer is either primary or secondary
        '''
        assignment = row_widget.getAssignment()
        if assignment > 0:
            for row in self.rvwr_widgets.values():
                if row != row_widget:
                    {1: row.setPrimaryState, 
                     2: row.setSecondaryState}[assignment](False)

        if self.proposal is not None:
            full_name = row_widget.reviewer.getFullName()
            role = row_widget.getAssignment()
            if role == 0:  role = None
            # check that reviewer is not excluded
            if full_name not in self.proposal.getExcludedReviewers(self.agup.reviewers):
                self.proposal.setAssignedReviewer(row_widget.reviewer, role)

        self.updateNumbersOfAssignedProposals()

        # pass the signal up the chain
        self.custom_signals.checkBoxGridChanged.emit()
    
    def setEnabled(self, sort_name, state=True):
        '''
        enable (True) or disable (False) a Reviewer identified by sort_name
        
        All eligible Reviewers are enabled.
        Reviewers become ineligible when they are named as part of the Proposal team.
        '''
        widget = self.rvwr_widgets[sort_name]
        widget.setEnabled(state)
        widget.dotProduct()
    
    def calcDotProducts(self):
        for widget in self.rvwr_widgets.values():
            widget.dotProduct()
    
    def update(self):
        ''' '''
        history.addLog(self.__class__.__name__ + '.update()', False)
#         self.setReviewersValues(self.reviewers)


def developer_main():
    '''
        create QGroupBox + QGridLayout and run the panel

        ===    ===   ===   ===   ====   =========================
        R1     #1    R2    #2    %      Reviewer Name
        ===    ===   ===   ===   ====   =========================
        [x]    1     [ ]   0     100%   Joe User
        [ ]    0     [x]   1     80%    Second Reviewer
        [ ]    0     [ ]   0     22%    Some Panel Member
        [ ]    0     [ ]   0     1%     Another Panel Member
        ===    ===   ===   ===   ====   =========================
    '''
    import sys
    import os
    import agup_data
    global layout, agup

    testfile = os.path.abspath('project/agup_project.xml')

    agup = agup_data.AGUP_Data()    
    agup.openPrpFile(testfile)

    app = QtGui.QApplication(sys.argv)
    grid = QtGui.QGroupBox('prop_revu_grid demo')

    layout = ReviewerAssignmentGridLayout(grid, agup)
    layout.addReviewers(agup.reviewers)
    layout.setReviewersValues(agup.reviewers)
    
    timer = QtCore.QTimer()
    timer.singleShot(2000, _onDelay1)
    timer.singleShot(5000, _onDelay2)
    timer.singleShot(7500, _onDelay3)

    grid.show()
    sys.exit(app.exec_())


def _onDelay1():
    global layout, agup
    test_gup_id = str(941*9*5)
    proposal = agup.proposals.proposals[test_gup_id]
    layout.setProposal(proposal)
    layout.setEnabled('0-Myers', False)
    layout.setEnabled('Jemian', True)


def _onDelay2():
    global layout, agup
    layout.setEnabled('0-Myers', True)
    layout.setEnabled('Jemian', False)


def _onDelay3():
    global layout, agup
    test_gup_id = str(pow(207,2) + 271)
    proposal = agup.proposals.proposals[test_gup_id]
    layout.setProposal(proposal)
    layout.setEnabled('Jemian', True)


if __name__ == '__main__':
    developer_main()
