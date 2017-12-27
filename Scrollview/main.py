import webbrowser

import kivy
from kivy.cache import Cache
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label

kivy.require('1.0.8')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class MainViewControl(BoxLayout):

    def __init__(self, **kwargs):
        super(MainViewControl, self).__init__(**kwargs)
        print('main view wrap {}'.format(self.height))
        print('mian view wrap{}'.format(self.size))
        # self.add_widget(Label(text='Main Screen Label',size_hint_y=.1))
        self.add_widget(CarouselViewWrap())
    pass


class CarouselViewWrap(BoxLayout):
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super(CarouselViewWrap, self).__init__(**kwargs)
        self.add_widget(CarouselView())
        print('carousel view wrap {}'.format(self.height))
        print('carousel view wrap{}'.format(self.size))
        print(self.parent)

    pass

class CarouselView(Carousel):
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super(CarouselView, self).__init__(**kwargs)
        print('carousel view {}'.format(self.height))
        print('carousel view {}'.format(self.size))
        for x in range(3):
            # self.add_widget(Label(text='carousel test {}'.format(x)))
            print(x)
            # self.add_widget(Label(text=str(x)))
            self.add_widget(ScrollVWrap())

    pass


class ScrollVWrap(BoxLayout):
    orientation = 'vertical'

    def __init__(self, **kwargs):
        super(ScrollVWrap, self).__init__(**kwargs)
        print('scroll view wrpa {}'.format(self.height))
        print('scroll view wrpa {}'.format(self.size))


        self.add_widget(ScrollV())
    pass

class ScrollV(ScrollView):
    orientation = 'vertical'
    def __init__(self, **kwargs):
        super(ScrollV, self).__init__(**kwargs)
        print('called scroll view instance')
        print(self.pos_hint)
        print('scroll view  {}'.format(self.height))
        print('scroll view  {}'.format(self.size))

        self.add_widget(Page())
# class PageWrap(BoxLayout):
#     def __init__(self, **kwargs):
#         super(PageWrap, self).__init__(**kwargs)
#         self.add_widget(Page())
    pass

class Page(GridLayout):
    print('pageinitialized')

    def __init__(self, **kwargs):
        super(Page, self).__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        print('page  {}'.format(self.height))
        print('page  {}'.format(self.size))
        print(self.children)
        # self.add_widget(Button(text='r', on_press=self.re))
        # self.add_widget(Button(text='a', on_press=self.set_ui))
        # self.add_widget(Button(text='r', on_press=self.re))
        # self.add_widget(Button(text='a', on_press=self.set_ui))

        # self.add_widget(Button(text='a',on_press=self.set_ui))
        # if Cache.get('mycache', Page().key):
        #     print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 1')
        #     print(Cache.get('mycache', Page().key))
        #     print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2')
        #     instance = Cache.get('mycache', Page().key)
        #     self.add_widget(instance)
        #
        #
        #     # retrieve the cached object
        # else:
        #     self.add_widget(Page())
    def re(self, *args):
        print('called')
        self.clear_widgets()

    def set_ui(self,*args):
        print('called setui')
        print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 1')
        # print(Cache.get('mycache', PageContent().key))
        print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2')
        print(Cache.print_usage())
        # if Cache.get('mycache', PageContent().key) == 1:
        #     print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 1')
        #     print(Cache.get('mycache', PageContent().key))
        #     print('cached >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> 2')
        #     instance = Cache.get('mycache', PageContent().key)
        #     for gg in range(20):
        #         self.add_widget(instance)
        #
        #
        #     # retrieve the cached object
        # else:

        for yo in range(20):
            print(yo)

            # self.add_widget(Label(text=str(yo),size=((self.width-20)/2, 40),size_hint=(None, None)))
            # self.add_widget(Image(source='1.jpg', size=((self.width - 20) / 2, (self.height-20) / 4), size_hint=(None, None)))
            self.add_widget(PageContent())
        print(self.children)
    # register a new Cache

    pass

class PageContent(BoxLayout):
    orientation = 'vertical'
    bla = ObjectProperty(None)

    # size = ((Page.width - 20) / 2, (Page.height - 20) / 4)
    # width = '(Page.width-20 )/ 2'
    # height = (Page.height - 20) / 4
    # size_hint = (None,None)
    def __init__(self, **kwargs):
        print('initi page cont')
        super(PageContent, self).__init__(**kwargs)
        print('parent {}'.format(self.get_parent_window()))
        print('page content  {}'.format(self.height))
        print('page  content {}'.format(self.size))
        print()
        self.add_widget(Image(source='1.jpg',size_hint_y=.9))
        self.add_widget(Button(text='text',size_hint_y=.1))
        print(self.bla)


        # create an object + id
    def cache_page(self):
        Cache.register('mycache', limit=10, timeout=None)
        self.key = 'objectid'
        instance = self
        Cache.append('mycache', self.key, instance)
    # def open_u(url,*args):
    #     webbrowser.open(url)

    pass


class ScrollViewApp(App):

    def build(self):
        root = BoxLayout()
        # # create a default grid layout with custom width/height
        # layout = GridLayout(cols=1, padding=10, spacing=10,
        #         size_hint=(None, None), width=500)
        #
        # # when we add children to the grid layout, its size doesn't change at
        # # all. we need to ensure that the height will be the minimum required
        # # to contain all the childs. (otherwise, we'll child outside the
        # # bounding box of the childs)
        # layout.bind(minimum_height=layout.setter('height'))
        #
        # # add button into that grid
        # for i in range(30):
        #     btn = Button(text=str(i), size=(480, 40),
        #                  size_hint=(None, None))
        #     layout.add_widget(btn)
        #
        # # create a scroll view, with a size < size of the grid
        # root = ScrollView(size_hint=(None, None), size=(500, 320),
        #         pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)
        # root.add_widget(layout)
        root.add_widget(MainViewControl())
        print(root.children)
        print(root.size)
        return root


if __name__ == '__main__':

    ScrollViewApp().run()
