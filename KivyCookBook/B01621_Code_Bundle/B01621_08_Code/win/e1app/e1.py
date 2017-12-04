import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory

Factory.register('MyWidget1', module='e0')

class MyW(Widget):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		self.add_widget(Factory.MyWidget1())

class e1App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e1App().run()