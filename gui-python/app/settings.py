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
from kivy.uix.settings import SettingString
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

from kivy.properties import ObjectProperty

from settingsjson import settings_json

Robot_Number = "15.5454"

class PasswordLabel(Label):
    pass

class SettingPassword(SettingString):
    def _create_popup(self, instance):
        super(SettingPassword, self)._create_popup(instance)
        self.textinput.password = True

    def add_widget(self, widget, *largs):
        if self.content is None:
            super(SettingString, self).add_widget(widget, *largs)
        if isinstance(widget, PasswordLabel):
            return self.content.add_widget(widget, *largs)

class Interface(RelativeLayout):
    robot_number = Robot_Number
    battery = 45

    def quit_program(self):
        sys.exit(0)

    def get_value(self):
        print self.ids.slider_bar.value

class RobotApp(App):
    def build(self):
        #self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        setting = self.config.get('example', 'robot_number')
        return Interface()

    def build_config(self, config):
        config.setdefaults('example', {
            'robot_number': Robot_Number,
            'optionsexample': 'option2',
            'wifi': 'Some Acces Point',
            'wifi_password': ''})

    def build_settings(self, settings):
        settings.register_type('password', SettingPassword)
        settings.add_json_panel('Robot Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

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
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        size_hint: None, None
    ProgressBar:
        id: battery_bar
        max: 100
        value: root.battery
        pos_hint: {'center_x': 0.1, 'center_y': 0.9}
        size_hint: None, None
    Label:
        id: robot_number_label
        # uses 'root' to get the value of a variable in the parent class
        text: 'Robot: ' + root.robot_number
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    Button:
        id: settings_button
        size_hint: None, None
        pos_hint: {'center_x': 0.9, 'center_y': 0.9}
        text: 'Settings'
        on_release: app.open_settings()
    Button:
        id: quit_button
        size_hint: None, None
        pos_hint: {'center_x': 0.75, 'center_y': 0.9}
        text: 'Quit'
        background_color: (1,0,0,1)
        on_press: root.quit_program()

<SettingPassword>:
    PasswordLabel:
        text: '(set)' if root.value else '(unset)'
        pos: root.pos
        font_size: '15sp'
''')

if __name__ == '__main__':
    RobotApp().run()
