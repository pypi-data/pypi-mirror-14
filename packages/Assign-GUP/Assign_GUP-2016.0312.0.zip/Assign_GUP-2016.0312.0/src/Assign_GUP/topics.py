
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Support AGUP topics
'''

import agup_data
import xml_utility
from lxml import etree

DEFAULT_TOPIC_VALUE = 0.0


class Topics(object):
    '''
    manage the list of AGUP topics (known here as ``key``)
    '''
    
    def __init__(self):
        self.clearAll()
    
    def __len__(self):
        return len(self.topics)

    def __iter__(self):
        for key in self.inOrder():
            yield key

    def inOrder(self):
        ''' '''
        return sorted(self.topics)
    
    def valueOrder(self):
        '''
        sort by topic values
        '''
        # make a dict with value as key and list(topics) as values
        db = {}
        for topic in self:
            val = str(self.get(topic))
            if val not in db:
                db[val] = []
            db[val].append(topic)
        
        # list of topics ordered by values (sub-ordered alphabetically)
        result = []
        for value in sorted(db.keys(), reverse=True):
            result += sorted(db[value])
        return result
    
    def exists(self, key):
        '''
        Is ``key`` already known?
        '''
        return key in self.topics
    
    def add(self, key, value = DEFAULT_TOPIC_VALUE):
        '''
        define a new topic (known here as ``key``)
        '''
        if self.exists(key):
            raise KeyError, 'This topic is already defined: ' + key
        key = key.strip()
        if len(key) == 0:
            raise KeyError, 'Must give a name for the topic'
        checkTopicValueRange(value)
        self.topics[key] = float(value)
        self._topics_string_ = ' '.join(self.getTopicList())
    
    def addTopics(self, key_list):
        '''
        add several topics at once (with default values)
        
        :param [str] key_list: list of topics (strings) to be added
        '''
        for key in key_list:
            self.add(key)
    
    def get(self, key):
        '''
        return value of an existing topic (known here as ``key``)
        
        topic must exist or KeyError exception will be raised
        '''
        if not self.exists(key):
            raise KeyError, 'This topic is not defined: ' + key
        return self.topics[key]
    
    def getTopicList(self):
        '''
        return a list of all topics
        '''
        return sorted(self.topics.keys())
    
    def set(self, key, value):
        '''
        set value of an existing topic (known here as ``key``)
        
        topic must exist or KeyError exception will be raised
        '''
        if not self.exists(key):
            raise KeyError, 'This topic is not defined: ' + key
        self.topics[key] = float(value)

    def clearAll(self):
        '''
        remove all keys from the list of topics
        '''
        self.topics = {}
        self._topics_string_ = ''     # to optimize comparisons of different Topics() objects

    def remove(self, key):
        '''
        remove the named topic
        
        :param str key: topic to be removed
        '''
        if self.exists(key):
            del self.topics[key]
        else:
            raise KeyError, 'Cannot remove (does not exist): ' + key
    
    def removeTopics(self, key_list):
        '''
        remove several topics at once
        
        :param [str] key_list: list of topics (strings) to be removed
        '''
        for key in key_list:
            self.remove(key)

    def compare(self, other_topics_object):
        '''
        compare topics in self.topics with the other_topics_object, return True if identical
        
        compares sorted list of topics between each object
        
        :param obj other_topics_object: instance of Topics()
        '''
        return other_topics_object._topics_string_ == self._topics_string_

    def diff(self, other_topics_object):
        '''
        differences in list of topics between self.topics and other_topics_object
        
        Comparison assumes that self.topics is the final result.
        Returned result shows topics added and removed from *other_topics_object*
        to obtain current list.
        
        :param obj other_topics_object: instance of Topics()
        :returns ([],[]): first list is topics added, second list is topics removed
        '''
        return diffLists(self.getTopicList(), other_topics_object.getTopicList())

    def dotProduct(self, other):
        r'''
        normalized dot product of Proposal (*self*) and Reviewer (*other*) topic strengths, :math:`\vec{p} \cdot \vec{r}`

        :param obj other: instance of Topics()
        :returns: :math:`\sum{\vec{p} \cdot \vec{r}} / \sum{\vec{p}}`
        
        * :math:`\vec{p}` is array of topic value strengths for Proposal
        * :math:`\vec{r}` is array of topic value strengths for Reviewer
        '''
        if not self.compare(other):
            raise KeyError, 'these two lists of topics are not the same, cannot dot product'
        if len(self.getTopicList()) == 0:
            return 0.0      # trivial result and avoids div-by-zero error
        
        props = [self.get(topic) for topic in self.getTopicList()]      # proposals
        denominator = sum(props)
        if denominator == 0.0:
            return 0.0

        rvwrs = [other.get(topic) for topic in self.getTopicList()]     # reviewers
        numerator = sum([u*v for u, v in zip(props, rvwrs)])
        dot_product = numerator / denominator   # sum(proposal_weight * reviewer_strength)
        return dot_product
    
    def importXml(self, xmlFile, read_values=True):
        '''
        :param str filename: name of XML file with Topics
        :param bool read_values: import topic values?
        '''
        root_tag = agup_data.AGUP_MASTER_ROOT_TAG
        xsd_file = agup_data.AGUP_XML_SCHEMA_FILE
        doc = xml_utility.readValidXmlDoc(xmlFile, root_tag, xsd_file)
        self.clearAll()
        self.importXmlTopics(doc.getroot(), read_values)
    
    def importXmlTopics(self, parent_node, read_values=True):
        '''
        make this common code segment reuseable
        
        :param obj parent_node: XML parent node
        :param bool read_values: import topic values?
        '''
        node = parent_node.find('Topics')
        if node is not None:
            for subnode in node.findall('Topic'):
                topic = subnode.attrib['name']
                value = DEFAULT_TOPIC_VALUE
                if read_values:
                    value = subnode.attrib['value']
                self.add(topic, value)
    
    def writeXml(self, specified_node, write_values=True):
        '''
        write Topics' data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        :param bool read_values: write topic values?
        '''
        from lxml import etree
        node = etree.SubElement(specified_node, 'Topics')
        if self.topics is not None:
            for topic in self.topics:
                subnode = etree.SubElement(node, 'Topic')
                subnode.attrib['name'] = topic
                if write_values:
                    subnode.attrib['value'] = str(self.get(topic))


def checkTopicValueRange(value):
    '''
    topic values must be 0..1 inclusive: standardize this check

    :param float value: topic value to be checked
    '''
    if not 0 <= float(value) <= 1.0:
        msg = 'value must be between 0 and 1: given=' + str(value)
        raise ValueError, msg


def diffLists(new_list, old_list):
    '''
    differences between two lists, return tuple([items added], [items removed])
    
    assumes each list had only unique entries, no redundancies

    :param [str] new_list: new list of strings to be compared
    :param [str] old_list: old list of strings to be compared
    '''
    added_items = [str(_) for _ in new_list if _ not in old_list]
    removed_items = [str(_) for _ in old_list if _ not in new_list]
    return added_items, removed_items


def sortListUnique(the_list):
    '''
    sort list and eliminate redundant items

    * make a dictionary with each list item
    * redundancies will be overwritten

    :param [str] the_list: list of strings to be sorted
    '''
    the_dict = {_:None for _ in the_list}
    return sorted( the_dict.keys() )


def synchronizeTopics(a_list, b_list):
    '''
    make the topic names in each list be the same
    
    * assumes each topics list had only unique entries, no redundancies
    * modifies objects in place
    
    :param obj a_list: instance of Topics()
    :param obj b_list: instance of Topics()
    '''
    if not a_list.compare(b_list):
        added, removed = a_list.diff(b_list)
        b_list.addTopics(added)         # topics not in b_list
        a_list.addTopics(removed)       # topics not in a_list
