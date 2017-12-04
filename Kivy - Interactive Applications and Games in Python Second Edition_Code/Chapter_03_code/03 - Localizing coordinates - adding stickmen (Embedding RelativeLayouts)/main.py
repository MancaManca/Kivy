import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

class Relatives (RelativeLayout):

    def test(self, event, other):
        a_label = self.a
        red_layout = a_label.parent

        (x, y) = a_label.pos
        print ("1. Original coordinates of a Label: %s, %s" % (x, y))

        (x, y) = red_layout.to_parent(a_label.x, a_label.y)
        print ("2. Coordinates of a_label relative to its parent (red): %s, %s" % (x, y))

        (x, y) = red_layout.to_local(x, y)
        print ("3. Back to original coordinates of a Label: %s, %s" % (x, y))

        (x, y) = red_layout.to_window(x, y, relative=False)
        print ("4. Absolute coordinates of a_label: %s, %s" % (x, y))

        (x, y) = red_layout.to_widget(x, y, relative=False)
        print ("5. Back to widget coordinates of a_label: %s, %s" % (x, y))


class RelativesApp(App):
    def build(self):
        return Relatives()

RelativesApp().run()
