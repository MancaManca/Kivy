import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
#from kivy.uix.button import Button

class MyW(Widget):
	
### Section There's more code (Uncommented for use it)
# 
#	def __init__(self, **kwargs):
#		super(MyW, self).__init__(**kwargs)
#		self.add_widget(Button(text='button2', pos=(100,100)))
	
	def my_callback(self):
		self.ids.label1.text = 'Click ! '

	def my_callback1(self, inpt):
		self.ids.label1.text = 'Enter ! ' + str(inpt)

class e1App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e1App().run()