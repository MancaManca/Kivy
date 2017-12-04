import kivy
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')
from kivy.app import App

class MainScreen(BoxLayout):
    sd = ObjectProperty()
    se = ObjectProperty()
    pl = ObjectProperty()
    ost = ObjectProperty()
    tro = ObjectProperty()

    # BEGIN SEARCHLOCATION
    def search_location(self):
        search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
        request = UrlRequest(search_url, self.populate) # <2>

    def populate(self,request,*args):
        print('entered populate')
        anchorStart, anchorEnd = makeHTMLTags("td")
        htmlText = request.result
        anchor = anchorStart + SkipTo(anchorEnd).setResultsName("body") + anchorEnd
        l = []
        for tokens, start, end in anchor.scanString(htmlText):
            l.append(tokens.body)

        baba = None
        deda = None

        for i, j in enumerate(l):
            if j == 'EUR':
                baba = i + 2
            if j == 'USD':
                deda = i + 2
        #############################################################

        # print('{}'.format(l))
        eur = l[baba]
        conv_eur = str(eur)
        print('{}'.format(conv_eur))
        dol = l[deda]
        conv_dol = str(dol)
        print('{}'.format(conv_dol))

        troskovi = {
            'porez': 22400,
            'stan': float(eur) * 225,
            'osiguranje': 3000,
            'kuca': 20000,
            'racuni': 10000,
        }

        tr = sum(troskovi.values())
        plata = float(float(dol) * 1350)
        ostatak = float(float(dol) * 1350) - float(tr)

        self.sd.text = conv_dol
        self.se.text = conv_eur
        self.pl.text = str(plata)
        self.tro.text = str(tr)
        self.ost.text = str(ostatak)
        # END SEARCHLOCATION


class PaycheckApp(App):
    pass

if __name__ == '__main__':
    PaycheckApp().run()








