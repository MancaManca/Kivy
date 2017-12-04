# main.py
import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget

class MyW(Widget):
	
	def on_touch_down(self, touch):
		if 'button' in touch.profile:
			self.ids.button1.text = touch.button 

		self.ids.label1.text = str(touch.profile)


class e1App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e1App().run()
