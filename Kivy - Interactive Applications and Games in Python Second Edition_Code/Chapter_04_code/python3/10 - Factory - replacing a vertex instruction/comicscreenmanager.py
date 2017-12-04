# File name: comicscreenmanager.py
import kivy
kivy.require('1.9.0')
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

class MyColorPicker(GridLayout):
    color= ListProperty((0,.3,.6,1))

    def select_color(self,color):
        self.color = color
        self.parent.manager.current = 'comicscreen'
