from kivy.network.urlrequest import UrlRequest
import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        search_template = "http://samples.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a1"
        search_url = search_template
        request = UrlRequest(search_url, self.found_location)

    # BEGIN SEARCHLOCATION
    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        self.search_results.item_strings = cities
        print(cities)
    # END SEARCHLOCATION


class WeatherApp(App):
    pass

if __name__ == '__main__':
	WeatherApp().run()
