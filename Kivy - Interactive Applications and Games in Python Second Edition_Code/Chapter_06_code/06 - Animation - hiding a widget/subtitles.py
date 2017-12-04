# File name: subtitles.py
import kivy
kivy.require('1.9.0')

from kivy.network.urlrequest import UrlRequest

class Subtitles:

    def __init__(self, url):
        self.subtitles = []
        req = UrlRequest(url, self.got_subtitles)

    def got_subtitles(self, req, results):
        self.subtitles = results['captions']

    def next(self, secs):
        for sub in self.subtitles:
            ms = secs*1000 - 12000
            st = 'startTime'
            d = 'duration'
            if ms >= sub[st] and ms <= sub[st] + sub[d]:
                return sub
        return None
