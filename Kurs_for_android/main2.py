import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')
from kivy.app import App

class CustomPopup(Popup):
    pass

class Navbar(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Navbar, self).__init__(**kwargs)
        # self.add_widget(Label(text='action bar'))
class MainView(BoxLayout):
    orientation = 'vertical'
    sd = ObjectProperty()
    se = ObjectProperty()
    pl = ObjectProperty()
    ost = ObjectProperty()
    tro = ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.add_widget(Navbar())
        self.add_widget(CarouselView())
class CarouselView(Carousel):
    def __init__(self, *args, **kwargs):
        super(CarouselView, self).__init__(**kwargs)

        self.add_widget(Label(text='main widget'))
        self.add_widget(Label(text='second widget'))
# class MainScreen(BoxLayout):
#     sd = ObjectProperty()
#     se = ObjectProperty()
#     pl = ObjectProperty()
#     ost = ObjectProperty()
#     tro = ObjectProperty()
#
#     # BEGIN SEARCHLOCATION
#     def search_location(self):
#         search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
#         # print search_url
#         self.request = UrlRequest(search_url, self.populate,on_error=self.on_error,on_failure=self.on_failure) # <2>
#     def on_error(self,request,*args):
#         print (args)
#         print ('on error {}'.format(request.result))
#     def on_failure(self,request,*args):
#         print (args)
#         print ('on failure {}'.format(request.result))
#     def populate(self,request,*args):
#         # print'entered populate'
#         anchorStart, anchorEnd = makeHTMLTags("td")
#         htmlText = request.result
#         anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd
#         l = []
#         for tokens, start, end in anchor.scanString(htmlText):
#             l.append(tokens.body)
#
#         baba = None
#         deda = None
#
#         for i, j in enumerate(l):
#             if j == 'EUR':
#                 baba = i + 2
#             if j == 'USD':
#                 deda = i + 2
#         #############################################################
#
#         print('{}'.format(l))
#         eur = l[baba]
#         conv_eur = str(eur)
#         print ('{}'.format(conv_eur))
#         dol = l[deda]
#         conv_dol = str(dol)
#         print ('{}'.format(conv_dol))
#
#         troskovi = {
#             'porez': 22400,
#             'stan': float(eur) * 225,
#             'osiguranje': 3000,
#             'kuca': 20000,
#             'racuni': 10000,
#         }
#
#         tr = sum(troskovi.values())
#         plata = float(float(dol) * 1350)
#         ostatak = float(float(dol) * 1350) - float(tr)
#
#         self.sd.text = conv_dol
#         self.se.text = conv_eur
#         self.pl.text = str(plata)
#         self.tro.text = str(tr)
#         self.ost.text = str(ostatak)
#         # END SEARCHLOCATION


class Paycheck2App(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        root.add_widget(MainView())
        return root
    def on_pause(self):
        return True
    def show_popup(self):
        p = CustomPopup()
        p.open()
    pass

if __name__ == '__main__':
    Paycheck2App().run()








