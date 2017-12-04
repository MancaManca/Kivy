# File name: style.py
import kivy
kivy.require('1.9.0')
from kivy.graphics import Line 
from kivy.factory import Factory

class NewLine (Line):
    def __init__(self, **kwargs):
        if not kwargs.get('width'):
             kwargs['width'] = 1.5
        Line.__init__(self, **kwargs)

Factory.unregister('Line')
Factory.register('Line', cls=NewLine)
