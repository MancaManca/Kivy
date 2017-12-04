import kivy
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import pyparsing
from pyparsing import makeHTMLTags, SkipTo

kivy.require('1.9.1')

from kivy.app import App

class MButton(Button):
    pass

class Sc1(Screen):

    def __init__(self, **kwargs):
        super(Sc1, self).__init__(**kwargs)

    sd = ObjectProperty()
    se = ObjectProperty()
    pl = ObjectProperty()
    ost = ObjectProperty()
    tro = ObjectProperty()

    pass

class Sc2(Screen):
    flag = False

    def __init__(self, **kwargs):
        super(Sc2, self).__init__(**kwargs)
        mb = BoxLayout(orientation='vertical')


        for i in range(4):
            mb.add_widget(Label(text='tuki{}'.format(i)))
        # self.add_widget(Label(text="src2"))
        b = Button(text='go')
        b.bind(on_press=self.do_action)
        mb.add_widget(b)
        self.add_widget(mb)

    def p(self, *args):
        print('f')

    def got_success(self, req, *args):
        print("got success response")
        #############################################################

        anchorStart, anchorEnd = makeHTMLTags("td")
        htmlText = req.result
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

        self.manager.get_screen('Home').sd.text = conv_dol
        self.manager.get_screen('Home').se.text = conv_eur
        self.manager.get_screen('Home').pl.text = str(plata)
        self.manager.get_screen('Home').tro.text = str(tr)
        self.manager.get_screen('Home').ost.text = str(ostatak)
        # print(self.manager.get_screen('Home'))
    def do_action(self,*args):

        print('button pressed')
        search_url = 'http://www.nbs.rs/kursnaListaModul/srednjiKurs.faces'
        req = UrlRequest(search_url,debug=True,on_success=self.got_success)

    pass


class MyW(BoxLayout):

    def __init__(self, **kwargs):
        super(MyW, self).__init__(**kwargs)
        s = Sc1
        self.ids.sm.add_widget(s(name='Home'))
        d = Sc2
        self.ids.sm.add_widget(d(name='Settings'))
        self.ids.buttons.add_widget(MButton(text="Home"))
        self.ids.buttons.add_widget(MButton(text="Settings"))


# class Controller(BoxLayout):


class ControllerApp(App):
    def build(self):
        return MyW()


if __name__ == '__main__':
    ControllerApp().run()
