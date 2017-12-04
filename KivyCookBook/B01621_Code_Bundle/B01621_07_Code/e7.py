import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.factory import Factory

class MyWidget1(Widget):
	def on_touch_down(self, touch): 
		with self.canvas:
			Color(1, 1, 0)
			d = 30.
			Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d)) 
			touch.ud['line'] = Line(points=(touch.x, touch.y))
	
	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

Factory.register('MyWidget1', cls=MyWidget1)

class e7App(App):
				
	def build(self):
		return  Factory.MyWidget1()

if __name__ == '__main__':
	e7App().run()
