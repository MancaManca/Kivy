# File name: kivyplayer.py
import kivy
kivy.require('1.9.0')

from kivy.app import App

from videocontroller import VideoController

class KivyPlayerApp(App):
    def build(self):
        return VideoController()

if __name__=="__main__":
    KivyPlayerApp().run()
