import kivy
kivy.require('1.8.0') # replace with your current kivy version !

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import RenderContext
from kivy.properties import StringProperty

# This header must be not changed, it contain the minimum information from Kivy.
header = '''
#ifdef GL_ES
precision highp float;
#endif
/* Outputs from the vertex shader */
varying vec4 frag_color;
varying vec2 tex_coord0;
/* uniform texture samplers */
uniform sampler2D texture0;
'''

# Our shader
our_shader = "$HEADER$" + '''
uniform vec2 resolution;
uniform float time;
void main(void)
{
   float x = gl_FragCoord.x;
   float y = gl_FragCoord.y;
   float mov0 = x+y+cos(sin(time)*2.)*100.+sin(x/100.)*1000.;
   float mov1 = y / resolution.y / 0.2 + time;
   float c1 = abs(sin(mov1+time));
   float c2 = abs(sin(c1+sin(mov0/1000.+time)));
   float c3 = abs(sin(x/1000.));
   gl_FragColor = vec4(c1,c2,c3,1.0);
}
'''

class ShaderWidget(FloatLayout):

    # property to set the source code for fragment shader
    fs = StringProperty(None)

    def __init__(self, **kwargs):
        # Instead of using Canvas, we will use a RenderContext,
        # and change the default shader used.
        self.canvas = RenderContext()

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas
        super(ShaderWidget, self).__init__(**kwargs)

        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def on_fs(self, instance, value):
        # set the fragment shader to our source code
        shader = self.canvas.shader
        old_value = shader.fs
        shader.fs = value
        if not shader.success:
            shader.fs = old_value
            raise Exception('failed')

    def update_glsl(self, *largs):
        self.canvas['time'] = Clock.get_boottime()
        self.canvas['resolution'] = list(map(float, self.size))
        # This is needed for the default vertex shader.
        self.canvas['projection_mat'] = Window.render_context['projection_mat']


class e6App(App):
    def build(self):
        return ShaderWidget(fs=our_shader)

if __name__ == '__main__':
    e6App().run()
