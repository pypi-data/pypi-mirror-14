
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Generic MVC Model for AGUP
'''

# :see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
# :see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/

import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore


class AGUP_MVC_Model(QtCore.QAbstractListModel):
    '''
    Generic MVC model for AGUP
    
    This is an adapter for the actual data object
    '''
    
    def __init__(self, data_object=[], headerdata=None, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.data_object = data_object

    def columnCount(self, parent):
        ''' '''
        #return len(self.headerdata)     # table
        return 1        # list

    def rowCount(self, parent):
        ''' '''
        return len(self.data_object)

    def data(self, index, role):
        ''' '''
        if not index.isValid():
            return None
            # For the foreground role you will need to edit this to suit your data
        row = index.row()
        if role == QtCore.Qt.ForegroundRole:
            item = self.data_object.getByIndex(row)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return self.data_object.getByIndex(row)

    # Use this only if you want the items in the table to be editable
    #   def setData(self, index, value, color):
    #       self.data_object.getByIndex(row) = value
    #       self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, ''const QModelIndex &)'), index, index)
    #       return True

    #   def flags(self, index):
    #       return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
