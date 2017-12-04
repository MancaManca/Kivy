# File name: kivyplayer.py
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.actionbar import ActionPrevious
from kivy.animation import Animation

from kivy.lang import Builder

import videocontroller

Builder.load_file('actiontextinput.kv')

class ActionListButton(ToggleButtonBehavior, ActionPrevious):
    pass


class KivyPlayer(FloatLayout):

    def hide_bars(self, instance, playing):
        if playing:
            self.list_button.state = 'normal'
            self.animationAB = Animation(y=self.height)
            self.action_bar.disabled = True
            self.animationAB.start(self.action_bar)
        else:
            self.action_bar.disabled = False
            self.action_bar.top = self.height
            if hasattr(self, 'animationAB'):
                self.animationAB.cancel(self.action_bar)

    def toggle_mute(self, instance, state):
        if state == 'down':
            self.video_controller.video.volume = 0
        else:
            self.video_controller.video.volume = 1

    def show_load_list(self):
        pass

    def search(self, text):
        pass

class KivyPlayerApp(App):
    def build(self):
        return KivyPlayer()

if __name__=="__main__":
    KivyPlayerApp().run()
