import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

class MyW(Widget):

	def my_callback(self,dt):
		self.ids.label1.text = 'My callback is called ! ' + str(dt)
	
	def on_touch_down(self, touch):
		trigger = Clock.create_trigger(self.my_callback)
		if touch.is_double_tap:
			trigger()

class e3App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e3App().run()
