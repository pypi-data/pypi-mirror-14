#!/usr/bin/env python

# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
:mod:`Main` code runs the GUI.
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui
import traceback

import about
import agup_data
import auto_assignment
import history
import prop_mvc_view
import proposal
import resources
import revu_mvc_view
import settings
import signals
import topics
import topics_editor

AGUP_filters = ';;'.join( ('AGUP PRP Project (*.agup)', 
                           'PRP Project (*.prp)', 
                           'XML File (*.xml)') )
AGUP_OPEN_FILTER = 'AGUP PRP Project (*.agup *.prp *.xml)'

UI_FILE = 'main_window.ui'
LOG_MINOR_DETAILS = False
# LOG_MINOR_DETAILS = True        # developer use


class AGUP_MainWindow(QtGui.QMainWindow):
    '''
    Creates a Qt GUI for the main window
    '''

    def __init__(self):
        self.settings = settings.ApplicationQSettings()
        self.agup = agup_data.AGUP_Data(self.settings)

        QtGui.QMainWindow.__init__(self)
        resources.loadUi(UI_FILE, baseinstance=self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_window_title = self.windowTitle()
        self.restoreWindowGeometry()

        self.modified = False
        self.forced_exit = False

        # keep these objects in a dictionary to simplify admin
        self.windows = dict(
            analysisGrid_report = None,
            assignment_report = None,
            email_report = None,
            email_template_editor = None,
            proposal_view = None,
            reviewer_view = None,
            summary_report = None,
        )

        self._init_history_()
        history.addLog('loaded "' + UI_FILE + '"', False)

        self.custom_signals = signals.CustomSignals()

        self._init_mainwindow_widget_values_()
        self._init_connections_()
        
        filename = self.settings.getPrpFile()
        if os.path.exists(filename):
            self.openPrpFile(filename)

        self.modified = False
        self.adjustMainWindowTitle()

    def _init_history_(self):
        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.statusbar, 
                                             history_widget=self.history,
                                             minor_details=LOG_MINOR_DETAILS)
        history.addMessageToHistory = self.history_logger.add

    def _init_mainwindow_widget_values_(self):
        self.setPrpFileText(self.settings.getPrpFile())
        self.setRcFileText(self.settings.fileName())
        self.setReviewCycleText(self.settings.getReviewCycle())
 
        for key in sorted(self.settings.allKeys()):
            value = self.settings.getKey(key)
            history.addLog('Configuration option: %s = %s' % (key, str(value)), False)

    def _init_connections_(self):
        self.actionNew_PRP_Project.triggered.connect(self.doNewPrpFile)
        self.actionOpen.triggered.connect(self.doOpenPrpFile)
        # self.actionUndo.triggered.connect()
        # self.actionCut.triggered.connect()
        # self.actionCopy.triggered.connect()
        # self.actionPaste.triggered.connect()
        # self.actionSelect_All.triggered.connect()
        self.actionImport_Topics.triggered.connect(self.doImportTopics)
        self.actionImport_Reviewers.triggered.connect(self.doImportReviewers)
        self.actionImport_Proposals.triggered.connect(self.doImportProposals)
        self.actionEdit_proposals.triggered.connect(self.doEditProposals)
        self.actionEdit_Reviewers.triggered.connect(self.doEditReviewers)
        self.actionEdit_Topics.triggered.connect(self.doEditTopics)
        self.actionEdit_Email_Template.triggered.connect(self.doEditEmailTemplate)
        self.actionSave.triggered.connect(self.doSave)
        self.actionSaveAs.triggered.connect(self.doSaveAs)
        self.actionReset_settings.triggered.connect(self.doResetDefaultSettings)
        self.actionExit.triggered.connect(self.doClose)
        self.actionAgupInfo.triggered.connect(self.doAgupInfo)
        self.actionSummary.triggered.connect(self.doSummaryReport)
        self.actionLetters.triggered.connect(self.doLettersReport)
        self.actionAssignments.triggered.connect(self.doAssignmentsReport)
        self.actionAnalysis_grid.triggered.connect(self.doAnalysis_gridReport)
        self.actionAutomated_assignment.triggered.connect(self.doAutomatedAssignment)
        self.actionUnassign_all_proposals.triggered.connect(self.doUnassignProposals)

    def doAgupInfo(self, *args, **kw):
        '''
        describe this application and where to get more info
        '''
        history.addLog('Info... box requested', False)
        # bless the Mac that it handles "about" differently
        ui = about.InfoBox(self, self.settings)    
        ui.show()
    
    def adjustMainWindowTitle(self):
        '''
        mark if main window is dirty
        
        indicate in main window title when there are unsaved modifications 
        (i.e., when self.cannotExit() is True)
        '''
        title = self.main_window_title
        if self.cannotExit():
            title += ' (*)'
        self.setWindowTitle(title)

    def cannotExit(self):
        '''
        advise if the application has unsaved changes
        '''
        if self.forced_exit:
            return False
        decision = self.modified
        if self.windows['proposal_view'] is not None:
            decision |= self.windows['proposal_view'].isProposalListModified()
        if self.windows['reviewer_view'] is not None:
            decision |= self.windows['reviewer_view'].isReviewerListModified()
        return decision

    def closeEvent(self, event):
        '''
        called when user clicks the big [X] to quit
        '''
        history.addLog('application forced quit requested', False)
        if self.cannotExit():
            if self.doNotQuitNow():
                event.ignore()
            else:
                self.doClose()
                event.accept()
        else:
            self.doClose()
            event.accept() # let the window close

    def closeSubwindows(self):
        '''
        close all other windows created by this code
        '''
        for window_name, window in self.windows.items():
            if window is not None:
                window.close()
                window.destroy()
                self.windows[window_name] = None

    def doClose(self, *args, **kw):
        '''
        called when user chooses exit (or quit), or from closeEvent()
        '''
        history.addLog('application exit requested', False)
        if self.cannotExit():
            if self.doNotQuitNow():
                return

        self.saveWindowGeometry()
        self.closeSubwindows()
        self.close()
    
    def doNotQuitNow(self):
        '''
        Ask user to save changes before exit.
        
        Return True if application should *NOT* exit.
        '''
        ret = self.requestConfirmation('The session data has changed.', 
                                    'Save the changes?', 
                                    QtGui.QMessageBox.Save 
                                   | QtGui.QMessageBox.Discard
                                   | QtGui.QMessageBox.Cancel, 
                                    QtGui.QMessageBox.Save)

        if ret == QtGui.QMessageBox.Save:
            history.addLog('Save before Exit was selected')
            self.doSave()
        elif ret == QtGui.QMessageBox.Cancel:
            history.addLog('Application Exit was canceled')
            return True     # application should NOT exit
        elif ret == QtGui.QMessageBox.Discard:
            self.forced_exit = True
            history.addLog('Discard Changes was chosen')
        else:
            msg = 'wrong button value from confirm close dialog: ' + str(ret)
            history.addLog('ValueError: ' + msg)
            raise ValueError, msg
        return False    # application should exit

    def doResetDefaultSettings(self):
        '''
        user requested to reset the settings to their default values
        
        Note: does not write to the rcfile
        '''
        history.addLog('Reset to Default Settings requested', False)
        self.settings.resetDefaults()
        self.adjustMainWindowTitle()

    def doNewPrpFile(self):
        '''
        clear the data in self.agup
        '''
        history.addLog('New PRP File requested', False)

        if self.cannotExit():
            ret = self.requestConfirmation('There are unsaved changes.', 
                                        'Forget about them?', 
                                        QtGui.QMessageBox.Ok
                                        | QtGui.QMessageBox.Cancel, 
                                        QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Cancel:
                return

        self.closeSubwindows()
        #self.agup.clearAllData()        # TODO: Why not make a new self.agup object?
        self.agup = agup_data.AGUP_Data(self.settings)
        self.modified = False
        self.setPrpFileText('')
        self.setIndicators()
        history.addLog('New PRP File')
        self.adjustMainWindowTitle()

    def doOpenPrpFile(self):
        '''
        open an existing PRP file
        '''
        history.addLog('Open PRP File requested', False)

        flags = QtGui.QFileDialog.DontResolveSymlinks
        title = 'Open PRP file'

        prp_file = self.settings.getPrpFile()
        if len(prp_file) == 0:
            prp_path = ''
        else:
            prp_path = os.path.dirname(prp_file)

        filename = QtGui.QFileDialog.getOpenFileName(None, 
                                                     title, 
                                                     prp_path, 
                                                     AGUP_OPEN_FILTER)
        filename = str(filename)

        if os.path.exists(filename):
            self.openPrpFile(filename)
            history.addLog('selected PRP file: ' + filename)
    
    def openPrpFile(self, filename):
        '''
        choose the XML file with data for this PRP review
        '''
        history.addLog('Opening PRP file: ' + filename)
        self.closeSubwindows()
        self.agup = agup_data.AGUP_Data(self.settings)
        
        try:
            self.agup.openPrpFile(filename)
        except Exception:
            history.addLog(traceback.format_exc())
            self.requestConfirmation(
                filename + ' was not an AGUP Project file',
                'Import AGUP Project file failed'
            )
            return

        self.setPrpFileText(filename)
        self.setIndicators()
        history.addLog('Open PRP file: ' + filename)

    def doEditProposals(self):
        '''
        edit the list of Proposals
        '''
        window_key = 'proposal_view'
        win = self.windows[window_key]
        if win is None:
            win = prop_mvc_view.AGUP_Proposals_View(self, self.agup, self.settings)
            win.custom_signals.checkBoxGridChanged.connect(self.onAssignmentsChanged)
            win.custom_signals.topicValueChanged.connect(self.onTopicValuesChanged)
            self.windows[window_key] = win
        win.show()

    def doEditReviewers(self):
        '''
        edit the list of Reviewers
        '''
        window_key = 'reviewer_view'
        win = self.windows['reviewer_view']
        if win is None:
            win = revu_mvc_view.AGUP_Reviewers_View(self, self.agup, self.settings)
            win.custom_signals.recalc.connect(self.doRecalc)
            win.custom_signals.topicValueChanged.connect(self.onTopicValuesChanged)
            self.windows[window_key] = win
        win.show()

    def doEditTopics(self):
        '''
        Create Window to edit list of Topics
        '''
        # post the editor GUI
        history.addLog('Edit Topics ... requested', False)
        self.closeSubwindows()
        
        known_topics = self.agup.topics.getTopicList()
        edit_topics_ui = topics_editor.AGUP_TopicsEditor(self, 
                                                         known_topics, 
                                                         self.settings)
        edit_topics_ui.exec_()   # Modal Dialog
        # closing the dialog produces this benign warning on Mac OSX:
        # modalSession has been exited prematurely - check for a reentrant call to endModalSession:
        # no real fix yet, see: https://bugreports.qt.io/browse/QTBUG-37699
        
        # learn what changed
        topics_list = edit_topics_ui.getTopicList()
        added, removed = topics.diffLists(topics_list, known_topics)
        if len(added) + len(removed) == 0:
            history.addLog('list of topics unchanged')
            self.adjustMainWindowTitle()
            return

        if False:       # skip this confirmation check now
            if not self.confirmEditTopics():
                history.addLog('revised list of topics not accepted')
                self.adjustMainWindowTitle()
                return False

        self.agup.topics.addTopics(added)
        self.agup.proposals.addTopics(added)
        self.agup.reviewers.addTopics(added)
        history.addLog('added topics: ' + ' '.join(added))

        self.agup.topics.removeTopics(removed)
        self.agup.proposals.removeTopics(removed)
        self.agup.reviewers.removeTopics(removed)
        history.addLog('deleted topics: ' + ' '.join(removed))
        history.addLog('Note: Be sure to review Topics for all Proposals and Reviewers.')

        self.modified = True
        self.adjustMainWindowTitle()
    
    def confirmEditTopics(self):
        '''
        confirm before proceeding
        '''
        ret = self.requestConfirmation('The list of topics has changed.', 
                                    'Save the changes?', 
                                    QtGui.QMessageBox.Save
                                    | QtGui.QMessageBox.Discard, 
                                    QtGui.QMessageBox.Save)
        return ret == QtGui.QMessageBox.Save

    def doImportProposals(self):
        '''
        import the proposal file as downloaded from the APS web site
        '''
        history.addLog('Import Proposals requested', False)
        title = 'Choose XML file with proposals'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        path = QtGui.QFileDialog.getOpenFileName(None, 
                                                 title, 
                                                 prp_path, 
                                                 "Proposals (*.xml)")
        path = str(path)
        if os.path.exists(path):
            history.addLog('selected file: ' + path, False)
            self.importProposals(path)
            history.addLog('imported proposals file: ' + path)

    def importProposals(self, filename):
        '''read a proposals XML file and set the model accordingly'''
        try:
            self.agup.importProposals(filename)
        except:
            history.addLog(traceback.format_exc())
            self.requestConfirmation(
                filename + ' was not an APS Proposals file',
                'Import Proposals failed'
            )
            return

        # ensure each imported proposal has the correct Topics
        for prop in self.agup.proposals:
            added, removed = self.agup.topics.diff(prop.topics)
            prop.addTopics(added)
            prop.removeTopics(removed)
        
        self.setIndicators()
        history.addLog('imported Proposals from: ' + filename)

        if self.getReviewCycleText() == '':
            self.setReviewCycleText(self.agup.proposals.cycle)

    def doImportReviewers(self):
        '''
        copy the list of Reviewers into this project from another PRP Project file
        '''
        history.addLog('Import Reviewers requested', False)
        title = 'Choose a PRP Project file to copy its Reviewers'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        path = QtGui.QFileDialog.getOpenFileName(None, 
                                                 title, 
                                                 prp_path, 
                                                 AGUP_OPEN_FILTER)
        path = str(path)
        if os.path.exists(path):
            self.importReviewers(path)
    
    def importReviewers(self, filename):
        '''read Reviewers from a PRP Project file and set the model accordingly'''
        try:
            self.agup.importReviewers(filename)
        except Exception:
            history.addLog(traceback.format_exc())
            self.requestConfirmation(
                filename + ' was not an AGUP Project file',
                'Import Reviewers failed'
            )
            return

        self.setNumTopicsWidget(len(self.agup.topics))
        self.setNumReviewersWidget(len(self.agup.reviewers))
        self.onAssignmentsChanged()
        history.addLog('imported Reviewers from: ' + filename)

    def doImportTopics(self):
        '''
        copy the list of Topics from another PRP file into this project
        '''
        history.addLog('Import Topics requested', False)
        title = 'Choose a PRP Project file to copy its Topics'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        filename = QtGui.QFileDialog.getOpenFileName(None, 
                                                     title, 
                                                     prp_path, 
                                                     AGUP_OPEN_FILTER)
        filename = str(filename)
        if os.path.exists(filename):
            self.importTopics(filename)
            history.addLog('imported Topics from: ' + filename)
    
    def importTopics(self, filename):
        '''read Topics from an AGUP PRP Project file and set the model accordingly'''
        try:
            self.agup.importTopics(filename)
        except Exception:
            history.addLog(traceback.format_exc())
            self.requestConfirmation(
                filename + ' was not an AGUP Project file',
                'Import Topics failed'
            )
            return

        self.setNumTopicsWidget(len(self.agup.topics))
        self.onTopicValuesChanged('', '', 0.0)
        history.addLog('imported topics from: ' + filename)

    def doRecalc(self):
        ''' '''
        if self.windows['proposal_view'] is not None:
            self.windows['proposal_view'].recalc()

    def doSave(self):
        '''
        save the self.agup data to the known project file name
        '''
        history.addLog('Save requested', False)
        filename = self.settings.getPrpFile()
        if len(filename) == 0:
            self.doSaveAs()
        else:
            self.agup.write(filename)
            self.modified = False
            for w in (self.windows['proposal_view'], self.windows['reviewer_view']):
                if w is not None:
                    w.details_panel.modified = False
            self.adjustMainWindowTitle()
            history.addLog('saved: ' + filename)
        self.settings.saveEmailKeywords(self.agup.email.keyword_dict)

    def doSaveAs(self):
        '''
        save the self.agup data to the data file name selected from a dialog box
        
        You may choose any file name and extension that you prefer.
        It is strongly suggested you choose the default file extension,
        to identify AGUP PRP Project files more easily on disk.
        Multiple projects files, perhaps for different review cycles,
        can be saved in the same directory.  Or you can save each project file
        in a different directory as you choose.

        By default, the file extension will be **.agup**, indicating
        that this is an AGUP PRP Project file.  The extensions *.prp* or *.xml*
        may be used as alternatives.  Each of these describes a file with *exactly 
        the same file format*, an XML document.
        '''
        history.addLog('Save As requested', False)
        filename = self.settings.getPrpFile()
        filename = QtGui.QFileDialog.getSaveFileName(parent=self, 
                                                     caption="Save the PRP project", 
                                                     directory=filename,
                                                     filter=AGUP_filters)
        filename = os.path.abspath(str(filename))
        if len(filename) == 0:
            return
        if os.path.isdir(filename):
            history.addLog('cannot save, selected a directory: ' + filename)
            return
        if os.path.islink(filename):     # might need deeper analysis
            history.addLog('cannot save, selected a link: ' + filename)
            return
        if os.path.ismount(filename):
            history.addLog('cannot save, selected a mount point: ' + filename)
            return

        self.agup.write(filename)
        self.setPrpFileText(filename)
        self.modified = False
        for w in (self.windows['proposal_view'], self.windows['reviewer_view']):
            if w is not None:
                w.details_panel.modified = False
        history.addLog('saved: ' + filename)
        self.adjustMainWindowTitle()

    def onAssignmentsChanged(self):
        '''
        called when a reviewer assignment checkbox has been changed
        '''
        self.modified = True
        self.adjustMainWindowTitle()
        windows_to_update = (self.windows['summary_report'],
                             self.windows['email_report'],
                             self.windows['assignment_report'],
                             self.windows['analysisGrid_report'],
                             self.windows['proposal_view'],
                             )
        for win in windows_to_update:
            if win is not None:
                win.update()
        self.custom_signals.checkBoxGridChanged.emit()
    
    def onTopicValuesChanged(self, *args, **kw):
        '''
        called when a proposal or reviewer topic value has been changed
        '''
        self.modified = True
        self.adjustMainWindowTitle()
        self.custom_signals.topicValueChanged.emit(*args, **kw)

    def doAutomatedAssignment(self):
        '''
        make automated assignments of reviewers to proposals
        '''
        auto_assign = auto_assignment.Auto_Assign(self.agup)
        number_changed = auto_assign.simpleAssignment()
        history.addLog('doAutomatedAssignment() complete', False)
        if number_changed > 0:
            if self.windows['proposal_view'] is not None:
                self.windows['proposal_view'].close()
                self.windows['proposal_view'] = None
            self.onAssignmentsChanged()

    def doUnassignProposals(self):
        '''
        Remove ALL assignments of reviewers to proposals
        '''
        history.addLog('doUnassignProposals() requested', False)
        ret = self.requestConfirmation('Remove ALL assignments of reviewers to proposals', 
                                    'Remove ALL?', 
                                    QtGui.QMessageBox.Ok
                                    | QtGui.QMessageBox.Cancel, 
                                    QtGui.QMessageBox.Cancel)
        if ret == QtGui.QMessageBox.Cancel:
            history.addLog('doUnassignProposals() was canceled', False)
            return

        counter = 0
        for prop in self.agup.proposals:
            for full_name, value in prop.eligible_reviewers.items():
                if value is not None:
                    prop.eligible_reviewers[full_name] = None
                    counter += 1
        if counter == 0:
            msg = 'no assignments to be removed'
        else:
            msg = str(counter)
            msg += ' assignment'
            if counter > 1:
                msg += 's'
            msg += ' removed'
        history.addLog(msg)
        if self.windows['proposal_view'] is not None:
            self.windows['proposal_view'].close()
            self.windows['proposal_view'] = None
        self.onAssignmentsChanged()

    def doSummaryReport(self):
        '''
        this report is helpful to balance proposal assignments
        
        show a read-only text page with how many primary and secondary proposals assigned to each reviewer
        '''
        import report_summary
        history.addLog('doSummaryReport() requested', False)
        window_key = 'summary_report'
        win = self.windows[window_key]
        if win is None:
            try:
                win = report_summary.Report(None, self.agup, self.settings)
                self.windows[window_key] = win
                self.custom_signals.checkBoxGridChanged.connect(win.update)
            except Exception:
                history.addLog(traceback.format_exc())
        else:
            win.update()
            win.show()

    def doLettersReport(self):
        '''
        prepare the email form letters to each reviewer with their assignments
        '''
        import email_mvc_view
        history.addLog('doLettersReport() requested', False)
        window_key = 'email_report'
        win = self.windows[window_key]
        if win is None:
            try:
                win = email_mvc_view.AGUP_Emails_View(None, self.agup, self.settings)
                self.windows[window_key] = win
                win.show()
                self.custom_signals.checkBoxGridChanged.connect(win.update)
            except Exception:
                history.addLog(traceback.format_exc())
        else:
            win.update()
            win.show()

    def doAssignmentsReport(self):
        '''
        show a read-only text page with assignments for each proposal
        '''
        import report_assignments
        history.addLog('doAssignmentsReport() requested', False)
        window_key = 'assignment_report'
        win = self.windows[window_key]
        if win is None:
            try:
                win = report_assignments.Report(None, self.agup, self.settings)
                self.windows[window_key] = win
                win.show()
                self.custom_signals.checkBoxGridChanged.connect(win.update)
            except Exception:
                history.addLog(traceback.format_exc())
        else:
            win.update()
            win.show()

    def doAnalysis_gridReport(self):
        '''
        show a table with dotProducts for each reviewer against each proposal *and* assignments
        '''
        import report_analysis_grid
        history.addLog('doAnalysis_gridReport() requested', False)
        window_key = 'analysisGrid_report'
        win = self.windows[window_key]
        if win is None:
            try:
                win = report_analysis_grid.Report(None, self.agup, self.settings)
                self.windows[window_key] = win
                win.show()
                self.custom_signals.checkBoxGridChanged.connect(win.update)
                self.custom_signals.topicValueChanged.connect(win.update)
            except Exception:
                history.addLog(traceback.format_exc())
        else:
            win.update()
            win.show()
    
    def doEditEmailTemplate(self):
        '''
        edit the template to send emails, include editor for keyword substitutions
        '''
        import editor_email_template
        history.addLog('doEditEmailTemplate() requested', False)
        window_key = 'email_template_editor'
        win = self.windows[window_key]
        if win is None:
            try:
                win = editor_email_template.Editor(None, self.agup, self.settings)
            except Exception:
                history.addLog(traceback.format_exc())
            self.windows[window_key] = win
            win.custom_signals.changed.connect(self.onTemplateChanged)
        else:
            win.show()

    def onTemplateChanged(self):
        ''' '''
        self.modified = True
        self.adjustMainWindowTitle()

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

    # widget getters and setters

    def setPrpFileText(self, text):
        ''' '''
        self.prp_file.setText(text)
        self.settings.setPrpFile(text)
        self.adjustMainWindowTitle()

    def setRcFileText(self, text):
        ''' '''
        self.rcfile.setText(text)
        self.adjustMainWindowTitle()

    def getReviewCycleText(self):
        ''' '''
        return str(self.review_cycle.text())
    
    def setReviewCycleText(self, text):
        ''' '''
        self.review_cycle.setText(text or '')
        self.settings.setReviewCycle(text)
        self.adjustMainWindowTitle()
    
    def _num_to_text_(self, number):
        if number > 0:
            text = str(number)
        else:
            text = 'no'
        return text

    def setNumTopicsWidget(self, number):
        ''' '''
        self.num_topics.setText(self._num_to_text_(number))

    def setNumReviewersWidget(self, number):
        ''' '''
        self.num_reviewers.setText(self._num_to_text_(number))

    def setNumProposalsWidget(self, number):
        ''' '''
        self.num_proposals.setText(self._num_to_text_(number))
    
    def setIndicators(self):
        ''' '''
        self.setNumTopicsWidget(len(self.agup.topics))
        self.setNumReviewersWidget(len(self.agup.reviewers))
        self.setNumProposalsWidget(len(self.agup.proposals))
        self.setReviewCycleText(self.agup.getCycle())
    
    def requestConfirmation(self, 
                         message, 
                         informative_text, 
                         buttons=None, 
                         default_button=None):
        '''
        request confirmation from the user about something
        '''
        if buttons is None:
            buttons = QtGui.QMessageBox.Ok
        if default_button is None:
            default_button = QtGui.QMessageBox.Ok
        box = QtGui.QMessageBox()
        box.setText(message)
        box.setInformativeText(informative_text)
        box.setStandardButtons(buttons)
        box.setDefaultButton(default_button)
        return box.exec_()


def process_command_line():
    '''
    support command-line options such as ```--help``` and ```--version```
    '''
    import argparse
    import Assign_GUP
    version = Assign_GUP.__version__
    doc = Assign_GUP.__doc__
    doc = 'v' + version + ', ' + doc.strip()
    parser = argparse.ArgumentParser(description=doc)
    parser.add_argument('-v', '--version', action='version', version=version)
    results = parser.parse_args()
    pass  # if we get here, then OK to proceed to start GUI


def main():
    '''start the program'''
    import sys
    process_command_line()
    app = QtGui.QApplication(sys.argv)
    mw = AGUP_MainWindow()
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
