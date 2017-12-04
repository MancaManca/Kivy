import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.logger import Logger

class MyW(Widget):
	Logger.info('MyW: This is a info message.')
	Logger.debug('MyW: This is a debug message.')
	try:
		raise Exception('bleh')
	except Exception: 
		Logger.exception('Something happened!')

class e3App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e3App().run()
