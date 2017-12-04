import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout 

class MyW(BoxLayout):
	pass
	
class CustomLayout(FloatLayout): 
	pass
	
class e3App(App): 
	def build(self):
		return MyW()
		
if __name__ == '__main__':
	e3App().run()