# File name: sidebar.py
import kivy
kivy.require('1.9.0')

from kivy.network.urlrequest import UrlRequest
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('sidebar.kv')

class ListItem(ToggleButton):
    video = ObjectProperty(None)

    def __init__(self, video, meta, surl, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.video = video
        self.meta = meta
        self.surl = surl

    def on_state(self, instance, value):
        if self.state == 'down':
            req = UrlRequest(self.meta, self.got_meta)
        
    def got_meta(self, req, results):
        data = results['talk']
        self.video.surl = self.surl
        self.video.source = data['media']['internal']['950k']['uri']
        self.video.image = data['images'][-1]['image']['url']
