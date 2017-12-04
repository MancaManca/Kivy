import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label


class e9App(App):
				
	def build(self):
		return Label(text='Hello [ref=world][color=0000ff]World[/color][/ref] dddddddddddddd', markup=True, font_size=80, font_name='DroidSans')

if __name__ == '__main__':
	e9App().run()
	