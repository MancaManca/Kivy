import kivy
kivy.require('1.9.0')

from kivy.uix.textinput import TextInput
from kivy.uix.actionbar import ActionItem

from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_string("""
<ActionTextInput>:
    background_color: 0.2,0.2,0.2,1
    foreground_color: 1,1,1,1
    cursor_color: 1,1,1,1
    padding: 14
    size_hint: None, 1
    width: 200
    hint_text: 'search'
    minimum_width: 200
""")


class ActionTextInput(TextInput,ActionItem):

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'w':
            self.player1.center_y += 10
        elif keycode[1] == 's':
            self.player1.center_y -= 10
        elif keycode[1] == 'up':
            self.player2.center_y += 10
        elif keycode[1] == 'down':
            self.player2.center_y -= 10
        print (keycode[1])
        return True
