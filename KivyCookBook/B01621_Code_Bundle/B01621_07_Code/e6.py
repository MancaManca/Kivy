import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class MyW(BoxLayout):
	pass

class e6App(App):				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e6App().run()

