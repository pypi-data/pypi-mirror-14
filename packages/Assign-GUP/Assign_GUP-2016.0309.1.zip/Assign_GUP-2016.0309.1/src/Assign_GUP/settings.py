
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

r'''
Support for AGUP program settings

A settings file is used to preserve certain values of the application
(such as window positions and full path to the project file).
The name of the settings file is given in the main window.
Note, the settings file may have the suffix ".ini" on some operating systems.
Remove the settings file to clear any settings.
There is also a menu item to clear this file and reset it to defaults.

This module uses QSettings (http://doc.qt.io/qt-4.8/qsettings.html).
        
..  note:: Multi-monitor support : method restoreWindowGeometry()
    
    On multi-monitor systems such as laptops, window may be
    restored to offscreen position.  Here is how it happens:
    
    * geo was saved while window was on 2nd screen while docked
    * now re-opened on laptop display and window is off-screen
    
    For now, keep the windows on the main screen 
    or learn how to edit the settings file.

---------
'''


import datetime
import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import __init__
orgName = __init__.__settings_orgName__
appName = __init__.__package_name__
GLOBAL_GROUP = '___global___'


class ApplicationQSettings(QtCore.QSettings):
    '''
    manage and preserve default settings for this application using QSettings
    
    Use the .ini file format and save under user directory
    '''
    
    def __init__(self):
        QtCore.QSettings.__init__(self, 
                                  QtCore.QSettings.IniFormat, 
                                  QtCore.QSettings.UserScope, 
                                  orgName, 
                                  appName)
        self.init_global_keys()
    
    def init_global_keys(self):
        d = dict(
            this_file = self.fileName(),
            review_cycle = '',           # redundant, treat as non-authoritative
            prp_file = '',
            version = 1.0,
            timestamp = str(datetime.datetime.now())
        )
        for k, v in d.items():
            if self.getKey(GLOBAL_GROUP + '/' + k) in ('', None):
                self.setValue(GLOBAL_GROUP + '/' + k, v)

    def _keySplit_(self, full_key):
        '''
        split full_key into (group, key) tuple
        
        :param str full_key: either `key` or `group/key`, default group (unspecified) is GLOBAL_GROUP
        '''
        if len(full_key) == 0:
            raise KeyError, 'must supply a key'
        parts = full_key.split('/')
        if len(parts) > 2:
            raise KeyError, 'too many "/" separators: ' + full_key
        if len(parts) == 1:
            group, key = GLOBAL_GROUP, str(parts[0])
        elif len(parts) == 2:
            group, key = map(str, parts)
        return group, key
    
    def keyExists(self, key):
        '''does the named key exist?'''
        return key in self.allKeys()

    def getKey(self, key):
        '''
        return the Python value (not a QVariant) of key or None if not found
        
        :raises TypeError: if key is None
        '''
        return self.value(key).toPyObject()
    
    def setKey(self, key, value):
        '''
        set the value of a configuration key, creates the key if it does not exist
        
        :param str key: either `key` or `group/key`
        
        Complement:  self.value(key)  returns value of key
        '''
        #?WHY? if not self.keyExists(key):
        group, k = self._keySplit_(key)
        if group is None:
            group = GLOBAL_GROUP
        self.remove(key)
        self.beginGroup(group)
        self.setValue(k, value)
        self.endGroup()
        if key != 'timestamp':
            self.updateTimeStamp()
 
    def getReviewCycle(self):
        ''' '''
        return str(self.getKey(GLOBAL_GROUP + '/review_cycle')) or ''
 
    def setReviewCycle(self, review_cycle):     # redundant, treat as non-authoritative
        ''' '''
        key = GLOBAL_GROUP + '/review_cycle'
        self.remove(key)
        self.setKey(key, str(review_cycle))
 
    def getPrpFile(self):
        ''' '''
        return str(self.getKey(GLOBAL_GROUP + '/prp_file')).strip() or ''
 
    def setPrpFile(self, prp_file):
        ''' '''
        key = GLOBAL_GROUP + '/prp_file'
        self.remove(key)
        self.setKey(key, str(prp_file))

    def resetDefaults(self):
        '''
        Reset all application settings to default values.
        '''
        for key in self.allKeys():
            self.remove(key)
        self.init_global_keys()
    
    def updateTimeStamp(self):
        ''' '''
        self.setKey('timestamp', str(datetime.datetime.now()))

    def saveEmailKeywords(self, keyword_dict):
        '''
        remember the email substitution keywords
        '''
        group = 'Email_Keywords'
        for k, v in keyword_dict.items():
            self.setKey(group + '/' + k, v)

    def getEmailKeywords(self):
        '''
        return the email substitution keywords as a dictionary
        '''
        group = 'Email_Keywords'
        self.beginGroup(group)
        key_list = self.childKeys()
        self.endGroup()
        db = {}
        for key in key_list:
            db[str(key)] = str(self.getKey(group + '/' + key))
        return db
    
    def getGroupName(self, window, group):
        return group or window.__class__.__name__ + '_geometry'

    def saveWindowGeometry(self, window, group=None):
        '''
        remember where the window was
        
        :param obj window: instance of QWidget
        '''
        group = self.getGroupName(window, group)
        geo = window.geometry()
        self.setKey(group + '/x', geo.x())
        self.setKey(group + '/y', geo.y())
        self.setKey(group + '/width', geo.width())
        self.setKey(group + '/height', geo.height())

    def restoreWindowGeometry(self, window, group=None):
        '''
        put the window back where it was
        
        :param obj window: instance of QWidget
        '''
        group = self.getGroupName(window, group)
        width = self.getKey(group + '/width')
        height = self.getKey(group + '/height')
        if width is None or height is None:
            return
        window.resize(QtCore.QSize(int(width), int(height)))

        x = self.getKey(group + '/x')
        y = self.getKey(group + '/y')
        if x is None or y is None:
            return

        # is this window on any available screen?
        qdw = QtGui.QDesktopWidget()
        x_onscreen = False
        y_onscreen = False
        for screen_num in range(qdw.screenCount()):
            # find the "available" screen dimensions 
            # (excludes docks, menu bars, ...)
            available_rect = qdw.availableGeometry(screen_num)
            if available_rect.x() <= int(x) < available_rect.x()+available_rect.width():
                x_onscreen = True
            if available_rect.y() <= int(y) < available_rect.y()+available_rect.height():
                y_onscreen = True

        # Move the window to the primary window if it would otherwise be drawn off screen
        available_rect = qdw.availableGeometry(qdw.primaryScreen())
        if not x_onscreen:
            offset = available_rect.x() + available_rect.width()/10
            x = available_rect.x() + offset
            width = min(int(width), available_rect.width())
        if not y_onscreen:
            offset = available_rect.y() + available_rect.height()/10
            y = available_rect.y() + offset
            height = min(int(height), available_rect.height())

        window.setGeometry(QtCore.QRect(int(x), int(y), int(width), int(height)))

    def saveSplitterDetails(self, window):
        '''
        remember where the splitter was
        
        :param obj window: instance of QWidget
        '''
        group = self.__class__.__name__ + '_splitter'
        sizes = map(int, window.splitter.sizes())
        self.setKey(group + '/widths', ' '.join(map(str, sizes)))

    def restoreSplitterDetails(self, window):
        '''
        put the splitter back where it was
        
        :param obj window: instance of QWidget
        '''
        group = self.__class__.__name__ + '_splitter'
        sizes = self.getKey(group + '/widths')
        if sizes is not None:
            window.splitter.setSizes(map(int, str(sizes).split()))


def qmain():
    ss = ApplicationQSettings()
    print ss
    
    #ss.setValue('morning', 'early')
    #ss.setValue('main_window/x', 40)

    print ss.fileName()
    print ss.applicationName()
    print ss.organizationName()
    print ss.status()
    ss.setKey('billy/goat', 'gruff')
    for key in ss.allKeys():
        print str(key), ss.getKey(key), ss._keySplit_(key)
    ss.resetDefaults()


if __name__ == '__main__':
    qmain()
