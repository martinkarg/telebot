from kivy.config import Config 

# Sets fullscreen to automatic
# Config.set('graphics', 'fullscreen', '1')


from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.graphics.context_instructions import Color
import sys

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

# Basically, in kv language, root is the class of the widget, so you can
# call whatever part of it using root.whatever or root.whatever() for
# a function

# size_hint_y is for not giving any size hint to the object, and height, well

# Can also use the id of something to get an attribute: menu_screen.height like CSS

Builder.load_string("""
<MenuScreen>:
	id: menu_screen 
	canvas:
		Color:
			rgba: self.battery_percentage
		Rectangle:
			pos: self.pos
			size: 400, 400
    BoxLayout:
        Button:
            text: 'Go to settings'
            on_press:
                root.manager.transition.direction = 'left'
                root.manager.current = 'settings'
            background_color: (0,1,0,1)
            size_hint_y: None
            height: 200
        Button:
            text: 'Quit'
            background_color: (1,0,0,1)
            on_press:
            	root.quit_program()
        Label:
        	text: 'Hello, there'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
""")

# Declare both screens
class MenuScreen(Screen):
    battery_percentage = ObjectProperty([0, 125, 125, 1])

    def quit_program():
    	sys.exit(0)

class SettingsScreen(Screen):
    pass

class TestApp(App):

	def build(self):
		# Create the screen manager
		screen_manager = ScreenManager()
		# Add both screens to screen manager
		screen_manager.add_widget(MenuScreen(name='menu'))
		screen_manager.add_widget(SettingsScreen(name='settings'))
		return screen_manager

if __name__ == '__main__':
    try:
    	TestApp().run()
    except KeyboardInterrupt:
    	exit()