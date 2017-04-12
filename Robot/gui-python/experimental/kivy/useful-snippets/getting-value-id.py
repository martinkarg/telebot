import sys

from kivy.config import Config 

# Configuration of kivy https://kivy.org/docs/api-kivy.config.html
#Config.set('graphics', 'fullscreen', 'auto')
#Config.set('graphics', 'borderless', '1')
#Config.set('kivy', 'exit_on_escape', '1')
#Config.set('kivy', 'keyboard_mode', 'systemanddock')


from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty

from settingsjson import settings_json

Builder.load_string('''
<Interface>:
    background_color: (0,0,1,1)
    orientation: 'vertical'
    Slider:
        id: slider_bar
        min: -25
        max: 25
        value: 0
        on_value: root.get_value()
    ProgressBar:
        id: battery_bar
        max: 100
        value: root.battery
    Label:
        id: robot_number_label
        # uses 'root' to get the value of a variable in the parent class
        text: 'Robot: ' + root.robot_number
    Button:
        id: settings_button
        size_hint: None, None
        pos: 200,200
        text: 'Settings'
        on_release: app.open_settings()
    Button:
        id: quit_button
        size_hint: None, None
        position: 200,200
        text: 'Quit'
        background_color: (1,0,0,1)
        on_press:
            root.quit_program()
''')

robot_number1 = "15.5454"

class Interface(BoxLayout):
    robot_number = robot_number1
    battery = 45

    def quit_program(self):
        sys.exit(0)

    def get_value(self):
        print self.ids.slider_bar.value

class SettingsApp(App):
    def build(self):
        #self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        setting = self.config.get('example', 'boolexample')
        return Interface()

    def build_config(self, config):
        config.setdefaults('example', {
            'boolexample': True,
            'numericexample': 10,
            'optionsexample': 'option2',
            'stringexample': 'some_string',
            'pathexample': '/some/path'})

    def build_settings(self, settings):
        settings.add_json_panel('Robot Settings',
                                self.config,
                                data=settings_json)
        settings.add_json_panel('Test',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value


SettingsApp().run()
