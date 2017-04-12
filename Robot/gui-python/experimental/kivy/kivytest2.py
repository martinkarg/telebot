from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

# Button
# class TestApp(App):
# 	def build(self):
# 		# return Button(text='Hello!',
# 		# 			  background_color=(0,0,1,1),
# 		# 			  font_size=150)

class TestApp(App):
    def build(self):
        f = FloatLayout()
        s = Scatter()
        l = Label(text='Hello!',
                  font_size=150)

        f.add_widget(s)
        s.add_widget(l)
        return f

if __name__ == '__main__':
		TestApp().run()