import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation

class MyW(Widget):
	
	def animate(self, instance):
		animation = Animation(pos=(100, 100), t='out_bounce')
		animation += Animation(pos=(200, 100), t='out_bounce')
		animation &= Animation(size=(500, 500))
		animation += Animation(size=(100, 50))
		
		animation.start(instance)

class e8App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e8App().run()