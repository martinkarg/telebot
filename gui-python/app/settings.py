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

global Robot_Number
Robot_Number = "15.5454"
global Robot_Battery
Robot_Battery = 80

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
    battery = Robot_Battery

    def quit_program(self):
        sys.exit(0)

    def get_value(self):
        print self.ids.slider_bar.value

    def change_value(self):
        self.ids.robot_number_label.text = 'Test: ' + str(Robot_Number)

    # This should be called every x time
    def update_values(self):
        self.ids.robot_number_label.text = 'Robot: ' + str(Robot_Number)
        self.ids.battery_bar.value = Battery_Percentage
        self.ids.battery_text.text = str(Battery_Percentage) + '%'


class RobotApp(App):
    def build(self):
        app = Interface()
        self.use_kivy_settings = False
        setting = self.config.get('example', 'robot_number')
        #app.change_value()
        return app

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
        print type(key)
        if(key == 'optionsexample'):
            print "hola"
        if(key == 'robot_number'):
            Robot_Number = value
            print "New number: " + str(Robot_Number)
            Interface().change_value()

Builder.load_string('''
<Interface>:
    canvas.before:
        Color:
            rgb: 0.3529,0.3216,0.3882,1
        Rectangle:
            pos: self.pos
            size: self.size
    ProgressBar:
        id: battery_bar
        max: 100
        value: root.battery
        pos_hint: {'center_x': 0.1, 'center_y': 0.9}
        size_hint: None, None
        background_color: (0,1,0,1)
    Label:
        id: battery_text
        text: str(root.battery) + '%'
        pos_hint: {'center_x': 0.23, 'center_y': 0.9}
        color: (1,1,1,1)
        font_size: 30
        bold: True
    Label:
        id: robot_number_label
        # uses 'root' to get the value of a variable in the parent class
        text: 'Robot: ' + root.robot_number
        pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        color: (1,1,1,1)
        font_size: 40
        bold: True
    Label:
        id: face
        text: ':]'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        color: (1,1,1,1)
        font_size: 60
        bold: True
        orientation: 'vertical'
    Button:
        id: settings_button
        size_hint: None, None
        size: 80, 40
        pos_hint: {'center_x': 0.9, 'center_y': 0.9}
        background_color: (0.3725,0.4118,0.4784,1)
        text: 'Settings'
        on_release: app.open_settings()
    Button:
        id: quit_button
        size_hint: None, None
        size: 80, 40
        pos_hint: {'center_x': 0.79, 'center_y': 0.9}
        background_color: (0.3725,0.4118,0.4784,1)
        text: 'Quit'
        on_press: root.quit_program()
    TextInput:
        id: motor_1_text
        text: 'Motor 1 (0-180)'
        on_text: root.change_value()
        size_hint: None, None
        size: 80, 40

<SettingPassword>:
    PasswordLabel:
        text: '(set)' if root.value else '(unset)'
        pos: root.pos
        font_size: '15sp'
''')

if __name__ == '__main__':
    RobotApp().run()
