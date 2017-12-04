# File name: controlbar.py
import kivy
kivy.require('1.9.0')

from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.lang import Builder

Builder.load_file('controlbar.kv')


class VideoStop(ButtonBehavior, Image):

    def stop(self, video, play_pause):
        play_pause.state = 'normal'
        video.state = 'stop'


class VideoSlider(Slider):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            video = self.parent.parent.video
            self.prev_state = video.state
            self.prev_touch = touch
            video.state = 'pause'
        return super(self.__class__, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and \
            hasattr(self, 'prev_touch') and \
            touch is self.prev_touch:
            video = self.parent.parent.video
            video.seek(self.value)
            if self.prev_state != 'stop':
                video.state = self.prev_state
        return super(self.__class__, self).on_touch_up(touch)

