import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory

Factory.register('MyWidget1', module='e7')

class MyW(Widget):
	pass

class e8App(App):
				
	def build(self):
		return Factory.MyWidget1()

if __name__ == '__main__':
	e8App().run()