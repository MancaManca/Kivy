import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class MyW(Widget):

	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs) 
		btn = Button(text='click me')
		btn.bind(on_press=self.on_press_callback, state=self.state_callback)
#		self.bind(pos=self.state_callback)	# See there's more section!
		self.add_widget(btn)

	def state_callback(self, obj, value): 
		print obj, value
	
	def on_press_callback(self, obj):
		self.ids.label1.text = 'press on button'

class e4App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e4App().run()
