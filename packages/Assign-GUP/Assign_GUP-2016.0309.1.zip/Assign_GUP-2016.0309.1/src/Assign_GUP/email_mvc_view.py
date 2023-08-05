
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
MVC View for emails

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys, time
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import email_template
import event_filters
import general_mvc_model
import history
import proposal
import qt_utils
import resources
import signals

UI_FILE = 'emailview.ui'
REVIEWERS_TEST_FILE = os.path.join('project', 'agup_project.xml')


class Email(object):
    '''data structure for sending email'''
    
    to = None
    cc = None
    subject = None
    body = None
    
    def send(self):
        '''send the email content to the default email tool'''
        # FIXME: no email when len(msg)>~750
        # FIXME: body text loses its formatting
        if self.to is None:
            raise RuntimeError('Must specify email recipient')
        msg = 'mailto:' + self.to
        more = []
        if self.cc is not None:
            more.append('cc=' + self.cc)
        if self.subject is not None:
            more.append('subject=' + self.subject)
        if self.body is not None:
            more.append('body=' + self.body)
        if len(more) > 0:
            args = '&'.join([_ for _ in more])
            msg += '?' + args
        url = QtCore.QUrl(msg)
        service = QtGui.QDesktopServices()
        service.openUrl(url)


class AGUP_Emails_View(QtGui.QWidget):
    '''
    Show the email to be sent to each Reviewer
    
    :param obj parent: instance of main_window.AGUP_MainWindow or None
    :param obj agup: instance of agup_data.AGUP_Data
    :param obj settings: instance of settings.ApplicationQSettings
    '''
    
    def __init__(self, parent=None, agup=None, settings=None, hide_email_button=True):
        self.parent = parent
        self.agup = agup
        self.settings = settings

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        
        self.setWindowTitle('Assign_GUP - Email Letters')
        self.listview_gb.setTitle('Reviewers')
        self.details_gb.setTitle('Email Letter')
        
        self.email = Email()

        self.details_panel = QtGui.QPlainTextEdit(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)
        
        self.sort_name = None

        if self.agup.reviewers is not None:
            self.setModel(self.agup.reviewers)
            if len(self.agup.reviewers) > 0:
                self.sort_name = self.agup.reviewers.keyOrder()[0]
                self.showReviewerEmail()
                self.selectFirstListItem()

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)

        self.arrowKeysEventFilter = event_filters.ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)

        self.custom_signals = signals.CustomSignals()
        self.openButton.released.connect(self.doOpenEmail)
        # FIXME: Until the email part is fixed, do not show the button in the UI
        if hide_email_button:
            self.openButton.hide()

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

    def selectModelByIndex(self, curr, prev):
        '''
        select Reviewer for email display as referenced by QListView index
        
        :param index curr: sort_name string of current selected reviewer
        :param index prev: QListView index of previously selected reviewer
        '''
        self.sort_name = self.index_to_ID(curr)
        if self.sort_name is None:
            return
        self.showReviewerEmail()
    
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

    def closeEvent(self, event):
        '''
        '''
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

    def showReviewerEmail(self):
        '''
        select Reviewer for email display as referenced by self.sort_name
        '''
        def getAssignments(full_name, role):
            assignments = []
            for prop in self.agup.proposals:
                if role ==  prop.eligible_reviewers.get(full_name, None):
                    assignments.append(prop.getKey('proposal_id'))
            return assignments

        if self.sort_name is None:
            return
        panelist = self.reviewers.getReviewer(str(self.sort_name))
        
        text = self.sort_name
        text += '\n'
        text += str(panelist)
        # TODO: show email letter instead
        et = email_template.EmailTemplate()
        keyword_dict = self._getEmailKeywords_(et)
        full_name = panelist.getFullName()
        primaries = getAssignments(full_name, proposal.PRIMARY_REVIEWER_ROLE)
        secondaries = getAssignments(full_name, proposal.SECONDARY_REVIEWER_ROLE)
        fields = dict(     # to be filled with data from an instance of Reviewer
            FULL_NAME = full_name,
            EMAIL = panelist.getKey('email'),
            ASSIGNED_PRIMARY_PROPOSALS = ' '.join(primaries),
            ASSIGNED_SECONDARY_PROPOSALS = ' '.join(secondaries),
        )
        fields.update(keyword_dict)
        title = 'email: ' + full_name
        self.email.body = et.mail_merge(**fields)
        self.details_panel.setPlainText(self.email.body)

        fmt = 'APS General User Proposal Review Assignments for %s Cycle'
        self.email.subject = fmt % fields['REVIEW_CYCLE']
        if 'CC' not in fields:
            fields['CC'] = email_template.DEFAULT_TEMPLATE_FIELDS['CC']
        self.email.cc = fields['CC']
        self.email.to = '%s <%s>' % (full_name, fields['EMAIL'])

        # set reviewers
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected reviewer: ' + str(self.sort_name))

    def _getEmailKeywords_(self, et):
        '''
        internal: get the dictionary of keywords for the mail merge
        '''
        keyword_dict = {}
        if self.settings is not None:
            keyword_dict = self.settings.getEmailKeywords()
        if len(keyword_dict) == 0:
            keyword_dict = et.keyword_dict
            # self.settings.saveEmailKeywords(keyword_dict)
        return keyword_dict
    
    def doOpenEmail(self):
        '''
        open the email letter in the email tool (does not work too good now)
        '''
        self.email.send()
    
    def update(self):
        history.addLog(self.__class__.__name__ + '.update()', False)
        self.showReviewerEmail()


def main():
    '''simple starter program to develop this code'''
    import sys
    import os
    import agup_data

    agup = agup_data.AGUP_Data()
    agup.openPrpFile('project/agup_project.xml')

    app = QtGui.QApplication(sys.argv)
    # TODO: developer use only: hide_email_button=False
    mw = AGUP_Emails_View(None, agup, hide_email_button=False)
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
