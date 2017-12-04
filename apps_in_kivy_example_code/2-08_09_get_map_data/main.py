# BEGIN IMPORT
from kivy.network.urlrequest import UrlRequest
# END IMPORT

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()

    # BEGIN SEARCHLOCATION
    def search_location(self):
        search_template = "http://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a1"# <1>
        search_url = search_template
        request = UrlRequest(search_url, self.found_location) # <2>
        print(request.resp_headers)

    def found_location(self, request, data):  # <3>
        print('found started')

        for d in data:  # <4>
            print(d)
    # END SEARCHLOCATION


class WeatherApp(App):
    pass

if __name__ == '__main__':
	WeatherApp().run()
