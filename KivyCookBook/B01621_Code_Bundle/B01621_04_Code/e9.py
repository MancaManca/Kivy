import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

class MyW(FloatLayout):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)

class e9App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e9App().run()