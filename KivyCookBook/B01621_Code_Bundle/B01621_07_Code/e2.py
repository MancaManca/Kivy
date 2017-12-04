import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.image import Image 
from kivy.loader import Loader

class e2App(App):
	
	def _image_loaded(self, proxyImage):
		if proxyImage.image.texture:
			self.image.texture = proxyImage.image.texture
	
	def build(self):
		proxyImage = Loader.image('http://iftucr.org/IFT/ANL_files/artistica.jpg')
		proxyImage.bind(on_load=self._image_loaded) 
		self.image = Image()
		return self.image

if __name__ == '__main__':
	e2App().run()
