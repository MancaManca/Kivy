# File name: videocontroller.py
import kivy
kivy.require('1.9.0')

from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder

import video
import controlbar

Builder.load_file('videocontroller.kv')

class VideoController(FloatLayout):
    pass
