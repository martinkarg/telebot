# Import library to use system functions
import sys
# Import library to parse '.ini' files
import ConfigParser
# Import library for getting and configuring time strings
from time import gmtime, strftime
# Import library for reading networks and configuring current network
import wifi

# Import Kivy Super Objects 
from kivy.config import Config 
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

# Import Kivy UIX Objects
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingString
from kivy.uix.settings import SettingOptions
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

# Import Kivy properties
from kivy.properties import ObjectProperty

# Import .json to configure settings screen
from settingsjson import settings_json

############################################################
############ FUNCTIONS #####################################
############################################################

''' Configuration of kivy https://kivy.org/docs/api-kivy.config.html
    Function: Configures the app to be fullscreen, borderless, to exit
              when user presses ESC key and allows touch keyboard
    Parameters: None
    Returns: None
    ConfigKivy()
'''
def ConfigKivy():
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'borderless', '1')
    Config.set('kivy', 'exit_on_escape', '1')
    Config.set('kivy', 'keyboard_mode', 'systemanddock')
    return None

''' 
    Function: Reads a .ini file and returns a dictionary
    Parameters: string ini_file, string section to be read
    Returns: dictionary with 'option': 'option value'
    GetIniFile("settings.ini", "settings_example")
''' 
def GetIniFile(ini_file, section):
    dict1 = {}
    config = ConfigParser.ConfigParser()
    config.read(str(ini_file))
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

''' 
    Function: Wrapper for GetIniFile and assigns the options
              /values read to the corresponding global variables
    Parameters: string ini_file, string section to be read
    Returns: None
    GetSettings("settings.ini", "settings_example")
''' 
def GetSettings(ini_file, section):
    settings = GetIniFile("robot.ini", "robot")
    Robot_Number = settings["robot_number"]
    WiFi = settings["wifi"]
    WiFi_Password = settings["wifi_password"]
    print Robot_Number
    return None

''' 
    Function: Gets battery status from the serial data
    Parameters: None
    Returns: int battery_value
    GetBattery()
''' 
def GetBattery():
    robot_battery = 15
    return robot_battery

''' 
    Function: Gets current date and time
    Parameters: None
    Returns: string "day-month-year hour:minute:second"
    GetDate()
''' 
def GetDate():
    return strftime("%d-%m-%Y %H:%M:%S", gmtime())

''' 
    Function: Gets available WiFi networks
    Parameters: interface name
    Returns: list of strings with available SSID's
    ScanWifi('wlan0')
''' 
def ScanWifi(interface):
    interface = 'wlp4s0'
    # Scan networks & generate a list of Cells
    networks = wifi.Cell.all(interface)
    # Declare list to hold SSID names, and fill it
    SSID_List = list()
    for network in networks:
        SSID_List.append(str(network.ssid) + ', ' + str(network.encryption_type) 
                         + ', ' + str(network.quality))
    # Return list with SSID strings
    return SSID_List

def ChangeWifi():
    pass

############################################################
############# KIVY CLASSES #################################
############################################################

class WifiList(SettingOptions):
    pass

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
    robot_number = GetIniFile("robot.ini","robot")["robot_number"]
    battery = GetBattery()

    def quit_program(self):
        sys.exit(0)

    def get_value(self):
        print self.ids.slider_bar.value

    def change_value(self):
        self.ids.robot_number_label.text = 'Test: ' + str(Robot_Number)

    # This should be called every x time
    def update(self, dt):
        self.ids.robot_number_label.text = 'Robot: ' + GetIniFile("robot.ini","robot")["robot_number"]
        self.ids.battery_bar.value = GetBattery()
        self.ids.battery_text.text = str(GetBattery()) + '%'
        self.ids.time.text = GetDate()

    def update_settings(self, dt):
        pass

class RobotApp(App):
    def build(self):
        app = Interface()

        self.use_kivy_settings = False

        # This just gets the robot_number current setting from self.config
        setting = self.config.get('robot', 'robot_number')

        Clock.schedule_interval(app.update, 1.0 / 60.0)
        Clock.schedule_interval(self.update_settings, 5.0)
        return app

    def update_settings(self, dt):
        #self.destroy_settings()
        #self.build_settings()
        pass

    def build_config(self, config):
        config.setdefaults('robot', {
            'robot_number': Robot_Number,
            'options_wifi': 'option1',
            'wifi': 'Some Acces Point',
            'wifi_password': ''})

    def build_settings(self, settings):
        settings.register_type('password', SettingPassword)
        settings.register_type('dynamic_list', WifiList)
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

############################################################
############# KIVY BUILDER #################################
############################################################

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
    Label:
        id: time
        text: '00:00:00'
        pos_hint: {'center_x': 0.85, 'center_y': 0.05}
        color: (1,1,1,1)
        font_size: 20
        bold: True
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

<SettingPassword>:
    PasswordLabel:
        text: '(set)' if root.value else '(unset)'
        pos: root.pos
        font_size: '15sp'
''')

############################################################
############# MAIN #########################################
############################################################

if __name__ == '__main__':
    Robot_Number = GetIniFile("robot.ini","robot")["robot_number"]
    print "Robot No. read from 'robot.ini': " + Robot_Number
    print ScanWifi('aaaa')
    RobotApp().run()

