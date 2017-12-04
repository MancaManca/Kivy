import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

class MyW(Widget):

	def on_touch_down(self, touch):

		self.add_widget(Button(text=str(touch.pos),pos=touch.pos))
		if touch.is_double_tap:
			self.remove_widget(self.ids.label1)
		if touch.is_triple_tap:
			self.clear_widgets()

class e2App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e2App().run()