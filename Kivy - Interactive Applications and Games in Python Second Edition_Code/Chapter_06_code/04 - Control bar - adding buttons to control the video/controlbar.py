# File name: controlbar.py
import kivy
kivy.require('1.9.0')

from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_file('controlbar.kv')


class VideoPlayPause(ToggleButtonBehavior, Image):
    pass


class VideoStop(ButtonBehavior, Image):

    def stop(self, video, play_pause):
        play_pause.state = 'normal'
        video.state = 'stop'

