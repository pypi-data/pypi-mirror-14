
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Proposals: underlying data class for the MVC model 
'''

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore
from lxml import etree

import agup_data
import proposal
import resources
import topics
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('proposals.xsd')
ROOT_TAG = 'Review_list'


class AGUP_Proposals_List(QtCore.QObject):
    '''
    the list of all proposals
    '''
    
    def __init__(self, agup):
        QtCore.QObject.__init__(self)

        self.agup = agup
        self.proposals = {}
        self.prop_id_list = []
        self.cycle = ''
    
    def __len__(self):
        return len(self.proposals)

    def __iter__(self):
        for prop_id in self.keyOrder():
            yield self.proposals[prop_id]

    def inOrder(self):
        return sorted(self.proposals.values())

    def keyOrder(self):
        return sorted(self.proposals.keys())

    def exists(self, prop_id):
        '''given ID string, does proposal exist?'''
        return prop_id in self.prop_id_list
    
    def getProposal(self, prop_id):
        '''return proposal selected by ID string'''
        if not self.exists(prop_id):
            raise IndexError, 'Proposal not found: ' + prop_id
        return self.proposals[prop_id]

    def getByIndex(self, index):
        '''
        given index in sorted list of proposals, return indexed proposal
        
        note:  index is *not* the proposal ID number
        '''
        if index < 0 or index >= len(self.prop_id_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.prop_id_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with proposals
        '''
        doc = xml_utility.readValidXmlDoc(filename, 
                                          agup_data.AGUP_MASTER_ROOT_TAG, 
                                          agup_data.AGUP_XML_SCHEMA_FILE,
                                          alt_root_tag=ROOT_TAG, 
                                          alt_schema=XML_SCHEMA_FILE,
                                          )
        root = doc.getroot()
        if root.tag == agup_data.AGUP_MASTER_ROOT_TAG:
            proposals_node = root.find('Proposal_list')
        else:
            proposals_node = root    # pre-agup reviewers file

        db = {}
        self.prop_id_list = []
        self.cycle = root.get('cycle', None) or root.get('period', None) or ''
        for node in proposals_node.findall('Proposal'):
            prop_id = xml_utility.getXmlText(node, 'proposal_id')
            prop = proposal.AGUP_Proposal_Data(node, filename)
            db[prop_id] = prop
            self.prop_id_list.append(prop_id)
        self.prop_id_list = sorted(self.prop_id_list)
        self.proposals = db
    
    def writeXmlNode(self, specified_node):
        '''
        write Proposals' data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        node = etree.SubElement(specified_node, 'Proposal_list')
        for prop in self.inOrder():
            prop.writeXmlNode(etree.SubElement(node, 'Proposal'))

    def addTopic(self, key, value=None):
        '''
        add a new topic key and initial value to all proposals
        '''
        value = value or topics.DEFAULT_TOPIC_VALUE
        for prop in self.inOrder():
            prop.addTopic(key, value)
    
    def addTopics(self, key_list):
        '''
        add several topics at once (with default values)
        '''
        for key in key_list:
            self.addTopic(key)

    def setTopicValue(self, prop_id, topic, value):
        '''
        set the topic value on a proposal identified by GUP ID
        '''
        if prop_id not in self.proposals:
            raise KeyError, 'Proposal ID not found: ' + str(prop_id)
        self.proposals[prop_id].setTopic(topic, value)

    def removeTopic(self, key):
        '''
        remove an existing topic key from all proposals
        '''
        for prop in self:
            prop.removeTopic(key)

    def removeTopics(self, key_list):
        '''
        remove several topics at once
        '''
        for key in key_list:
            self.removeTopic(key)
