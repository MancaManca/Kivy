import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter


class MyW(Widget):
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		but1 = Button(text='hello') 
		scatter = Scatter(size=(400, 400), size_hint=(None, None))
		scatter.add_widget(but1)
		self.add_widget(scatter)


class e6App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e6App().run()
