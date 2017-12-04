import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse

class MyW(Widget):
	
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs) 
		with self.canvas:
			self.rect = Ellipse(pos=self.pos, size=(10,10)) 
		
		self.bind(pos=self.update_rect)
		self.bind(size=self.update_rect)
	
	def update_rect(self, *args): 
			self.rect.pos = self.pos 
			self.rect.size = self.size

class e4App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e4App().run()
