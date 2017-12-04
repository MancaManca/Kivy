# kivy -m kivy.atlas myatlas 2065 *.png

import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class MyW(Widget):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		a = Button(size=(200,200),background_normal='atlas://myatlas/f1', background_down='atlas://myatlas/f2')
		self.add_widget(a)

class e2App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e2App().run()
