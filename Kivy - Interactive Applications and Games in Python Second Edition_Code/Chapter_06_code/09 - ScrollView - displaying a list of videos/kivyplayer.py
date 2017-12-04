# File name: kivyplayer.py
import kivy
kivy.require('1.9.0')

import json
import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.actionbar import ActionPrevious
from kivy.animation import Animation

from kivy.lang import Builder

import videocontroller
from loaddialog import LoadDialog
from sidebar import ListItem

Builder.load_file('actiontextinput.kv')

_surl = 'http://www.ted.com/talks/subtitles/id/%s/lang/en'
_meta = 'results/%s.json'


class ActionListButton(ToggleButtonBehavior, ActionPrevious):
    def on_state(self, instance, value):
        if self.state == 'normal':
            self.animationSB = Animation(right=0)
            self.animationSB.start(self.root.side_bar)
        else:
            self.root.side_bar.x=0

class KivyPlayer(FloatLayout):

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.playlist.bind(minimum_height=self.playlist.setter('height'))

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
        content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load a file list", content=content, size_hint=(1, 1))
        self._popup.open()

    def load_list(self, path, filename):
        json_data=open(os.path.join(path, filename[0]))
        data = json.load(json_data)
        json_data.close()
        self.load_from_json(data)
        self.dismiss_popup()

    def load_from_json(self, data):
        self.playlist.clear_widgets()
        for val in data['results']:
            t = val['talk']
            video = self.video_controller.video
            meta = _meta % t['id']
            surl = _surl % t['id']
            item = ListItem(video, meta, surl, text=t['name'])
            self.playlist.add_widget(item)
        self.list_button.state = 'down'

    def dismiss_popup(self):
        self._popup.dismiss()

    def search(self, text):
        pass


class KivyPlayerApp(App):
    def build(self):
        return KivyPlayer()

if __name__=="__main__":
    KivyPlayerApp().run()
