import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button

class MyW(Widget):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		carousel = Carousel(direction='right') 
		for i in range(3):
			src = "f%d.png" % i 
			image = Factory.AsyncImage(source=src, allow_stretch=True) 
			carousel.add_widget(image)
		self.add_widget(carousel)

class e1App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e1App().run()
