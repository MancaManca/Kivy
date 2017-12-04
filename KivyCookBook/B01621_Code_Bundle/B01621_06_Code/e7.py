import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Fbo, Color, Rectangle

class MyW(Widget):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)

		with self.canvas:

			self.fbo = Fbo(size=(256, 256))
  
			Rectangle(size=(32, 32), texture=self.fbo.texture) 
			Rectangle(pos=(32, 0), size=(64, 64), texture=self.fbo.texture) 
			Rectangle(pos=(96, 0), size=(128, 128), texture=self.fbo.texture)
			Rectangle(pos=(224, 0), size=(256, 128), texture=self.fbo.texture)

		with self.fbo:
			Color(1, 0, 0, .8) 
			Rectangle(size=(256, 64)) 
			Color(0, 1, 1, .8) 
			Rectangle(size=(64, 256))

class e7App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e7App().run()
