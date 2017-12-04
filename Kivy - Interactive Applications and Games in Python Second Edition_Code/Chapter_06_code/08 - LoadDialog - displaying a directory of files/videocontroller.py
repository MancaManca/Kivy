# File name: videocontroller.py
import kivy
kivy.require('1.9.0')

from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.lang import Builder

import video
import controlbar

Builder.load_file('videocontroller.kv')

class VideoController(FloatLayout):
    playing = ObjectProperty(None)

    def on_playing(self, instance, value):
        if value:
            self.animationVB = Animation(top=0)
            self.control_bar.disabled = True
            self.animationVB.start(self.control_bar)
        else:
            self.play_pause.state = 'normal'
            self.control_bar.disabled = False
            self.control_bar.y = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if hasattr(self, 'animationVB'):
                self.animationVB.cancel(self.control_bar)
            self.play_pause.state = 'normal'
        return super(self.__class__, self).on_touch_down(touch)
