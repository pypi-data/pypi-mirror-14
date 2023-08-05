
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Reviewers: underlying data class for the MVC model 
'''

import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore
from lxml import etree
import traceback

import agup_data
import history
import reviewer
import resources
import topics
import xml_utility


REVIEW_PANEL_TAG = 'Review_panel'
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_ROOT_TAG = 'AGUP_Review_Session'


class AGUP_Reviewers_List(QtCore.QObject):
    '''
    the list of all reviewers
    '''
    
    def __init__(self, agup):
        QtCore.QObject.__init__(self)

        self.agup = agup
        self.reviewers = {}     # .clear()
        self.reviewer_sort_list = []
    
    def __len__(self):
        return len(self.reviewers)

    def __iter__(self):
        for item in self.keyOrder():
            yield self.reviewers[item]

    def inOrder(self):
        ''' '''
        return sorted(self.reviewers.values())

    def keyOrder(self):
        ''' '''
        return sorted(self.reviewers.keys())

    def exists(self, sort_name):
        '''given sort_name string, does reviewer exist?'''
        return sort_name in self.reviewer_sort_list
    
    def getReviewer(self, sort_name):
        '''return reviewer selected by sort_name string'''
        if not self.exists(sort_name):
            raise IndexError, 'Reviewer not found: ' + sort_name
        return self.reviewers[sort_name]
    
    def getReviewerAssignments(self, sort_name, role=None):
        '''
        find all proposals assigned to the named reviewer
        
        :param str sort_name: key for reviewer name
        :param int role: one of [None, 0, 1, 2], 
            where None or 0 mean get both roles
        '''
        valid_roles = (None, 
                       0, 
                       proposal.PRIMARY_REVIEWER_ROLE, 
                       proposal.SECONDARY_REVIEWER_ROLE)
        if role not in valid_roles:
            raise ValueError, 'unknown role specified: ' + str(role)
        rvwr = self.getReviewer(sort_name)
        if role in (None, 0, proposal.PRIMARY_REVIEWER_ROLE):
            primaries = rvwr.getAssignments(self.agup.proposals)
            if role == proposal.PRIMARY_REVIEWER_ROLE:
                return primaries
        if role in (None, 0, proposal.SECONDARY_REVIEWER_ROLE):
            secondaries = rvwr.getAssignments(self.agup.proposals)
            if role == proposal.SECONDARY_REVIEWER_ROLE:
                return secondaries
        return tuple(primaries, secondaries)
    
    def getByFullName(self, full_name):
        '''return reviewer selected by full_name string'''
        if len(full_name) == 0:
            raise ValueError, 'no name provided'
        sort_name = None
        for rvwr in self.inOrder():
            if rvwr.getFullName() == full_name:
                sort_name = rvwr.getKey('name')
                break
        return self.getReviewer(sort_name)

    def getByIndex(self, index):
        ''' '''
        if not 0 <= index < len(self.reviewer_sort_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.reviewer_sort_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with reviewers
        '''
        doc = xml_utility.readValidXmlDoc(filename, 
                                          agup_data.AGUP_MASTER_ROOT_TAG, 
                                          agup_data.AGUP_XML_SCHEMA_FILE,
                                          )
        root = doc.getroot()
        if root.tag == agup_data.AGUP_MASTER_ROOT_TAG:
            reviewers_node = root.find(REVIEW_PANEL_TAG)
        else:
            reviewers_node = root    # pre-agup reviewers file
            raise RuntimeError, 'import of panel.xml file no longer supported'

        db = {}
        self.reviewer_sort_list = []
        self.cycle = reviewers_node.get('period', None)
        for node in reviewers_node.findall('Reviewer'):
            sort_name = node.attrib['name'].strip()
            db[sort_name] = reviewer.AGUP_Reviewer_Data(node, filename)
            self.reviewer_sort_list.append(sort_name)
        self.reviewer_sort_list = sorted(self.reviewer_sort_list)
        self.reviewers = db
    
    def writeXmlNode(self, specified_node):
        '''
        write Reviewers' data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        node = etree.SubElement(specified_node, REVIEW_PANEL_TAG)
        for rvwr in self.inOrder():
            rvwr.writeXmlNode(etree.SubElement(node, 'Reviewer'))

    def addTopic(self, key, value=None):
        '''
        add a new topic key and initial value to all reviewers
        '''
        value = value or topics.DEFAULT_TOPIC_VALUE
        for item in self.inOrder():
            item.addTopic(key, value)
    
    def addTopics(self, key_list):
        '''
        add several topics at once (with default values)
        '''
        for key in key_list:
            self.addTopic(key)

    def setTopicValue(self, sort_name, topic, value):
        '''
        set the topic value on a reviewer identified by sort_name
        '''
        if sort_name not in self.reviewers:
            raise KeyError, 'Reviewer name not found: ' + str(sort_name)
        self.reviewers[sort_name].setTopic(topic, value)

    def removeTopic(self, key):
        '''
        remove an existing topic key from all reviewers
        '''
        for item in self:
            item.removeTopic(key)

    def removeTopics(self, key_list):
        '''
        remove several topics at once
        '''
        for item in key_list:
            self.removeTopic(item)
