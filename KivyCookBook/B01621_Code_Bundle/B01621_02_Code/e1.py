import kivy
kivy.require('1.9.0')  

from kivy.app import App
from kivy.uix.widget import Widget

class MyW(Widget):

    def on_touch_down(self, touch):
        if 'button' in touch.profile:
            self.ids.button1.text = touch.button

class e1App(App):

    def build(self):
        return MyW()

if __name__ == '__main__':
    e1App().run()