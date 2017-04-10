from kivy.app import App
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.clock import Clock

kv = """
BoxLayout:
    Widget:
        Scatter:
            center: self.parent.center
            size: text.size
            do_rotation: False
            do_translation: False
            do_scale: False
            rotation: app.angle
            Label:
                id: text
                size: self.texture_size
                text: "test with scatter"
    Widget:
        Label:
            center: self.parent.center
            size: self.texture_size
            canvas.before:
                PushMatrix
                Rotate:
                    angle: app.angle
                    origin: self.center
            canvas.after:
                PopMatrix
            text: "test with matrix transformation"
"""


class TextVerticalApp(App):
    angle = NumericProperty(0)

    def build(self):
        Clock.schedule_interval(self.update_angle, 0)
        return Builder.load_string(kv)

    def update_angle(self, dt, *args):
        self.angle += dt * 100

if __name__ == '__main__':
	TextVerticalApp().run()
