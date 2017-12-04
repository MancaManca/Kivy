import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.videoplayer import VideoPlayer

class MyW(Widget): 
	
	def __init__(self, **kwargs):
		super(MyW, self).__init__(**kwargs)
		player = VideoPlayer(source='GOR.MOV', state='play', options={'allow_stretch': True}, size=(600,600))
		self.add_widget(player)

class e5App(App):
				
	def build(self):
		return MyW()

if __name__ == '__main__':
	e5App().run()