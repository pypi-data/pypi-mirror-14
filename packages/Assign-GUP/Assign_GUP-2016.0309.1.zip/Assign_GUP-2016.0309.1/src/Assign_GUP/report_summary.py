
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
show a read-only text page with how many primary and secondary proposals assigned to each reviewer

::

    total number of proposals: #
    primary proposals per reviewer: #.#
    
    Overall topic strength: TBA
     
    Primary assignments:
    reviewer1  ##: ##### ##### #####
    reviewer2  ##: ##### ##### #####
    reviewer3  ##: ##### ##### #####
     
    Secondary assignments:
    reviewer1  ##: ##### ##### #####
    reviewer2  ##: ##### ##### #####
    reviewer3  ##: ##### ##### #####
    
    Unassigned proposals: #

'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtGui
else:
    from PyQt4 import QtGui

import history
import plainTextEdit


class Report(plainTextEdit.TextWindow):
    ''' '''
    
    def __init__(self, parent, agup, settings):
        self.settings = settings
        self.agup = agup
        self.title = 'Reviewer Assignment Summary'
        text = self.makeText()

        plainTextEdit.TextWindow.__init__(self, 
                                          parent, 
                                          self.title, 
                                          text, 
                                          self.settings)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.show()
    
    def makeText(self):
        '''
        generate the text of the panel
        '''
        text = [self.title, 
                '', 
                'Total number of proposals: ' + str(len(self.agup.proposals)), 
                ]

        unassigned = []
        for prop in self.agup.proposals:
            for r in prop.getAssignedReviewers():
                if r is None:
                    unassigned.append(prop)
                    break
        text.append('Unassigned proposals: ' + str(len(unassigned)))

        # text.append('')
        # text.append('Overall topic strength: ' + 'TBA')

        if len(self.agup.reviewers) > 0:
            mean = float(len(self.agup.proposals)) / float(len(self.agup.reviewers))
            text.append('average primary proposals per reviewer: ' + str(int(mean*10+0.5)/10.0))    # 0.0 precision

            text.append('')
            width = max([len(_.getFullName()) for _ in self.agup.reviewers])
            fmt = '%s%d%s: ' % ('%0', width, 's %3d')
            for role, label in enumerate(['Primary', 'Secondary']):
                text.append(label + ' assignments:')
                for rvwr in self.agup.reviewers:
                    full_name = rvwr.getFullName()
                    prop_list = rvwr.getAssignments(self.agup.proposals, role+1)
                    row = fmt % (full_name, len(prop_list)) + ' '.join(prop_list)
                    text.append(row)
                text.append('')
        return '\n'.join(text)
    
    def update(self):
        ''' '''
        text = self.makeText()
        self.setText(text)
        history.addLog(self.__class__.__name__ + '.update()', False)
