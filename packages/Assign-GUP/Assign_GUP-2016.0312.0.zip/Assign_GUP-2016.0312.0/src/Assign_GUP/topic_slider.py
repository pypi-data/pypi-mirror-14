
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
add label, slider, value to a QGridLayout

Coordinate the action of a slider with the topic value::

  label   value   slider                 
  bio     0.7     |---|---|---|[-]|---|
  phys    0.2     |--[|]--|---|---|---|

======  =========  ====================================================
widget  type       description
======  =========  ====================================================
label   QLabel     mnemonic name (no white space)
value   QLineEdit  string with floating point value: 0 <= value <= 1.0
slider  QSlider    graphical adjustment of value
======  =========  ====================================================

These three widgets will be added to the *parent* widget,
assumed to be on the same row of a QGridLayout.

A *topic* (known here as *label*) is some scientific area 
of interest to the PRP.
Such as, for the SAXS review panel, some of the proposals
are for XPCS (X-ray Photon Correlation Spectroscopy).

Each proposal will have a strength value assigned for
each topic, indicating how important that topic is to the
proposed experiment.

Each reviewer will have a strength value assigned for
each topic, indicating the strength of that reviewer 
in the particular topic.

The strength values will be constrained to the range [0 .. 1].
A QValidator() object will be used to color the background of 
the QLineEdit to indicate whether or not the entered text is 
acceptable.  The value of the slider will update with 
acceptable values from the text entry.  The background color
indicates acceptable or invalid input.  The slider will be updated
for acceptable values.
The validator will also constrain the input to a precision
of 2 decimal places.

---------
'''


import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore, QtGui
else:
    from PyQt4 import QtCore, QtGui

import history
import traceback


class AGUP_TopicSlider(QtCore.QObject):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent, row, label, value):
        QtCore.QObject.__init__(self)
        self.slider_factor = 100    # slider = int(slider_factor * value_widget + 0.5)

        self.slider = QtGui.QSlider(
                                value=int(self.slider_factor*value),
                                maximum=self.slider_factor,
                                pageStep=10,
                                tracking=False,
                                orientation=QtCore.Qt.Horizontal,
                                tickPosition=QtGui.QSlider.TicksAbove,  # looks like a user preference
                                #tickPosition=QtGui.QSlider.TicksBothSides,
                                #tickPosition=QtGui.QSlider.TicksBelow,
                                #tickPosition=QtGui.QSlider.NoTicks,
                                tickInterval=20
                               )

        self.value_widget = QtGui.QLineEdit(str(value))
        self.value_widget.setMaximumWidth(self.slider_factor)
        self.validator = QtGui.QDoubleValidator()
        self.validator.setRange(0.0, 1.0)
        self.validator.setDecimals(2)
        self.value_widget.setValidator(self.validator)
        
        self.label = label
        self.parent = parent
        self.value = value

        parent.addWidget(QtGui.QLabel(label), row, 0)
        parent.addWidget(self.value_widget, row, 1)
        parent.addWidget(self.slider, row, 2)
        
        self.value_changing = False # issue #33: avoid changing value text while editing value
        
        # connect slider changes with value_widget and vice versa
        self.slider.valueChanged.connect(self.onSliderChange)
        self.slider.sliderMoved.connect(self.onSliderChange)
        self.value_widget.textEdited.connect(self.onValueChange)
    
    def onSliderChange(self, value):
        '''update the QLineEdit when the slider is changed'''
        if not self.value_changing: # but not while editing the value text
            self.setValue(str(value / float(self.slider_factor)))
    
    def onValueChange(self, value):
        '''update the QSlider when the value is changed'''
        state = self.validator.validate(self.value_widget.text(), 0)[0]
        color = 'white'
        if state == QtGui.QValidator.Acceptable:
            self.value_changing = True
            self.setSliderValue(int(float(value)*self.slider_factor + .5))
            self.value_changing = False
        elif state == QtGui.QValidator.Intermediate:
            color = 'yellow'
        else:
            color = 'red'
        self.value_widget.setStyleSheet('background-color: ' + color)

    def getValue(self):
        ''' '''
        # if can't convert, get value from slider
        text = self.value_widget.text()
        state = self.validator.validate(text, 0)[0]
        if state == QtGui.QValidator.Acceptable:
            value = float(text)
        else:
            value = self.getSliderValue() / float(self.slider_factor)
        return value
    
    def setValue(self, value):
        '''
        set strength of this topic (0:low, 1.0: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the slider value.
        '''
        self.value_widget.setText(str(value))
    
    def getSliderValue(self):
        ''' '''
        value = self.slider.value()
        return value
    
    def setSliderValue(self, value):
        '''
        set value of the slider indicating strength of this topic (0:low, 100: high)
        
        :param int value: 0 <= value <= 100
        
        This routine sets the text value.
        '''
        self.slider.setValue(value)
