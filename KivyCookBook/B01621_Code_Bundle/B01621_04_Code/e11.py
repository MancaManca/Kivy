import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock


class MyW(AnchorLayout):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)

class e11App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e11App().run()