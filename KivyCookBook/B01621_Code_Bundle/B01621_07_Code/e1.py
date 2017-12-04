import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget

class MyW(Widget):
	pass

class e1App(App):
				
	def build(self):
		self.title = 'My Title'
		self.icon = 'f0.png'
		#self.load_kv(filename='e2.kv')
		return MyW()
	
	def on_start(self):
		print("Hi")
		return True
		
	def on_pause(self):
		print("paused")
		return True

	def on_resume(self):
		print("active")
		pass
		
	def on_stop(self):
		print("Bye!")
		pass
		
if __name__ == '__main__':
	e1App().run()
