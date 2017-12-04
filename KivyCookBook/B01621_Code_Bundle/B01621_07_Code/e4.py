import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader

class MyW(Widget): 
	
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		b1=Button(text='Play')
		b1.bind(on_press=self.press) 
		self.add_widget(b1)
	
	def press(self, instance):
		sound = SoundLoader.load('owl.wav')
		if sound:
			print("Sound found at %s" % sound.source)
			print("Sound is %.3f seconds" % sound.length)
			sound.play()
			#sound.seek(60)
			print('playing')

class e4App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e4App().run()
