
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Data for one Reviewer of General User Proposals
'''

from lxml import etree

import proposal
import tools
import topics
import xml_utility


class AGUP_Reviewer_Data(object):
    '''
    A Reviewer of General User Proposals
    '''
    
    # these are the XML tags to find in a Reviewer node
    tagList = ('full_name', 'phone', 'email', 'notes', 'joined', 'URL')
    
    def __init__(self, xmlParentNode = None, xmlFile = None):
        '''
        :param xmlParentNode: lxml node of the Reviewer
        :param xmlFile: name of the XML file
        :param xmlFile: str
        '''
        self.db = {}
        self.topics = topics.Topics()
        self.db['name'] = None
        self.xmlFile = xmlFile

        for item in self.tagList:
            self.db[item] = None
        if xmlParentNode != None:
            self.importXml( xmlParentNode )

    def __str__(self):
        '''
        Canonical string representation
        '''
        if self.getFullName() == None or self.db['email'] == None:
            return str(None)
        return "%s <%s>" % (self.db['full_name'], self.db['email'])

    def importXml(self, reviewer):
        '''
        Fill the class variables with values from the XML node
        
        :param reviewer: lxml node node of the Reviewer
        '''
        self.db['name'] = reviewer.attrib['name'].strip()
        for k in self.tagList:
            text = xml_utility.getXmlText(reviewer, k)
            if text is None:
                self.db[k] = None
            else:
                self.db[k] = tools.text_encode(text)
        self.topics = topics.Topics()
        node = reviewer.find('Topics')
        if node is not None:
            for t_node in node.findall('Topic'):
                key = t_node.attrib['name']
                try:
                    value = float( t_node.attrib['value'])
                except ValueError:
                    value = 0.0
                self.topics.add(key, value)
    
    def writeXmlNode(self, specified_node):
        '''
        write this Reviewer's data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        specified_node.attrib['name'] = self.getSortName()
        for tag in self.tagList:
            etree.SubElement(specified_node, tag).text = self.getKey(tag)
        self.topics.writeXml(specified_node)
    
    def getSortName(self):
        ''' '''
        return self.getKey('name')
    
    def getFullName(self):
        ''' '''
        return self.getKey('full_name')
    
    def getKey(self, key):
        ''' '''
        return self.db[key]
    
    def setKey(self, key, value):
        '''
        save a value to a known key
        
        example::
        
            self.setKey('full_name', 'Pete Jemian')
        
        '''
        if key not in self.db:
            raise KeyError, 'unknown key: ' + key
        self.db[key] = value
    
    def getTopic(self, topic):
        '''
        return the value of the named topic
        '''
        return self.topics.get(topic)
    
    def getTopicList(self):
        '''
        return a list of all topics
        '''
        return self.topics.getTopicList()
    
    def addTopic(self, topic, value=None):
        '''
        declare a new topic and give it an initial value
        
        topic must not exist or KeyError exception will be raised
        '''
        value = value or topics.DEFAULT_TOPIC_VALUE
        self.topics.add(topic, value)
    
    def addTopics(self, topics_list):
        '''
        declare several new topics and give them all default values
        
        each topic must not exist or KeyError exception will be raised
        '''
        self.topics.addTopics(topics_list)
    
    def setTopic(self, topic, value=None):
        '''
        set value of an existing topic
        
        topic must exist or KeyError exception will be raised
        '''
        value = value or topics.DEFAULT_TOPIC_VALUE
        self.topics.set(topic, value)

    def removeTopic(self, key):
        '''
        remove the named topic
        '''
        self.topics.remove(key)

    def removeTopics(self, key_list):
        '''
        remove several topics at once
        '''
        for key in key_list:
            self.removeTopic(key)
    
    def getAssignments(self, proposals, role):
        '''find all proposals assigned to this reviewer with the given role'''
        if role not in (proposal.PRIMARY_REVIEWER_ROLE, proposal.SECONDARY_REVIEWER_ROLE):
            raise ValueError, 'unknown role value: ' + str(role)
        my_name = self.db['full_name']
        assignments = []
        for prop_num, prop in proposals.proposals.items():
            reviewers = prop.getAssignedReviewers()
            if my_name == reviewers[role-1]:
                assignments.append(prop_num)
        return sorted(assignments)
