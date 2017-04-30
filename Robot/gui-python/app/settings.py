# Import library to use system functions
import sys
# Import library to parse '.ini' files
import ConfigParser
# Import library for getting and configuring time strings
from time import gmtime, strftime
# Import library for reading networks and configuring current network
import wifi
# Import library for reading json data from .json files
import json
# Import library for serial communication
import serial
# Import library for using/processing system time
import time
# Import selenium for web automation
import selenium
# Import library to make web requests
import requests
# Import library used for managing .log files
import logging
# Import library used to extract, format and print stack traces
import traceback

import webbrowser

import os

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

global Log_File
Log_File = "telebot_error.log"

global ser

global Wireless_Interface
Wireless_Interface = "wlan0"

global Serial_Commands
Serial_Commands = {
    'forward': 16,
    'backward': 150,
    'right': 32,
    'left': 48,
    'clockwise': 64,
    'anti_clockwise': 80,
    'stop': 96,
    'sensor_1': 112,
    'sensor_2': 128,
    'battery': 144
}

global Speed_Modes
Speed_Modes = {
    'level_0': 0,
    'level_1': 1,
    'level_2': 2,
    'level_3': 3,
    'level_4': 4,
    'level_5': 5,
    'level_6': 6,
    'level_7': 7,
    'level_8': 8,
    'level_9': 9,
    'level_10': 10,
    'level_11': 11,
    'level_12': 12,
    'level_13': 13,
    'level_14': 14,
    'level_15': 15,
}

global Key_Commands
Key_Commands = {
        'w': Serial_Commands['forward'],
        's': Serial_Commands['stop'],
        'a': Serial_Commands['left'],
        'd': Serial_Commands['right'],
        'q': Serial_Commands['anti_clockwise'],
        'e': Serial_Commands['clockwise'],
        'x': Serial_Commands['backward']
    }

global Speed
Speed = "level_0"

global Old_Commands
Old_Commands = " "

global Robot_ID
global Robot_Password
Robot_ID = Robot_Password = "robot01"

############################################################
############ FUNCTIONS #####################################
############################################################

def PlaceCall():
    robot_login = "https://connection-robertoruano.c9users.io/robot_login.php?username=" + Robot_ID + "&pswrd=" + Robot_Password
    os.system("sudo su -c \"chromium-browser '" + robot_login + "'\" -s /bin/sh pi")
    return robot_login

def ErrorLog(message):
    logging.basicConfig(filename = Log_File, level = logging.DEBUG)
    logging.warning(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
                    str(message))
    return None

def DebugLog(message):
    logging.basicConfig(filename= Log_File, level = logging.DEBUG)
    logging.debug(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
                  str(message))
    return None
    
def InfoLog(message):
    logging.basicConfig(filename = Log_File, level = logging.DEBUG)
    logging.info(strftime(" %d-%m-%Y %H:%M:%S -> ", gmtime()) + 
                 str(message))
    return None

''' 
    Function: Starts a serial object at 9600 baud rate with default 
              settings
    Parameters: None
    Returns: Serial object ser
    StartSerial()
'''
def StartSerial():
    ser = serial.Serial(
      port="/dev/ttyS0",
      baudrate = 9600,
      parity = serial.PARITY_NONE,
      stopbits = serial.STOPBITS_ONE,
      bytesize = serial.EIGHTBITS,
      timeout = 1
    )
    return ser

# Initialize ser as Serial object
ser = StartSerial()

''' 
    Function: Sends a message to specified serial object
    Parameters: Serial ser, String message
    Returns: boolean True when done
    SendMessage(ser, "hello")
'''
def SendMessage(ser, message):
    ser.write(message)
    return True

''' 
    Function: Gets a message at specified Serial object
    Parameters: Serial ser
    Returns: String serial_message
    GetsMessage(ser)
'''
def GetMessage(ser):
    serial_message = ser.readline()
    return serial_message

''' 
    Function: Gets battery status from the serial data
    Parameters: None
    Returns: int battery_value
    GetBattery()
''' 
def GetBattery():
    SendMessage(ser, chr(Serial_Commands["battery"]))
    robot_battery = GetMessage(ser)
    InfoLog("Battery read at: " + str(robot_battery) + "%")
    return 15

def GetCall():
    s = requests.get("https://connection-robertoruano.c9users.io/PHP/call.html")
    string = str(s.content)
    if "calling" in string:
        InfoLog("Received call")
        return True
    else:
        InfoLog("No new call")
        return False

''' 
    Function: Gets file log.html, and returns the newest command
    Parameters: None
    Returns: char commands
    GetCommand()
'''
def GetCommand():
    global Old_Commands
    string = ""
    commands = "n"
    s = requests.get("https://connection-robertoruano.c9users.io/PHP/log.html")
    string = str(s.content)
    if len(string)>len(Old_Commands):
        character_numbers = len(Old_Commands)-len(string)
        Old_Commands = string
        commands = Old_Commands.strip()[-1]
        SendMessage(ser,chr(Key_Commands[commands] + Speed_Modes[Speed]))
        InfoLog("Read and sent command: " +  commands)
        return commands
    s = requests.get("https://connection-robertoruano.c9users.io/PHP/log.html")
    string = str(s.content)
    InfoLog("No new command")
    return commands

''' Configuration of kivy https://kivy.org/docs/api-kivy.config.html
    Function: Configures the app to be fullscreen, borderless, to exit
              when user presses ESC key and allows touch keyboard
    Parameters: None
    Returns: None
    ConfigKivy()
'''
def ConfigKivy():
    Config.set('graphics', 'fullscreen', '1')
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
    Function: Gets current date and time
    Parameters: None
    Returns: string "day-month-year hour:minute:second"
    GetDate()
''' 
def GetDate():
    return strftime("%d-%m-%Y %H:%M:%S", gmtime())

''' 
    Function: Gets available WiFi networks
    Parameters: str interface (to use for scanning)
    Returns: list of strings with available SSID's
    ScanWifi()
''' 
def ScanWifi():
    interface = Wireless_Interface
    # Scan networks & generate a list of Cells
    networks = wifi.Cell.all(interface)
    # Declare list to hold SSID names, and fill it
    SSID_List = list()
    for network in networks:
        SSID_List.append(str(network.ssid) + ', ' + str(network.encryption_type) 
                         + ', ' + str(network.quality))
    # Return list with SSID strings
    InfoLog("Scanned networks: " + str(SSID_List))
    return SSID_List

''' 
    Function: Changes the settings screen variables to display all
              available wifi networks in the options_wifi container
    Parameters: str original_json_string (to modify)
    Returns: str modified_json_string (adds WiFi networks)
    ChangeSettings(settings_json)
''' 
def ChangeSettings(settings_json):
    #print settings_json
    test = settings_json.split("\"insertion\"")
    #print "Split str: " + str(test[0]) + str(test[1])
    SSID_List = ScanWifi()
    test = ''
    for ssid in SSID_List:
        ssid = '\"' + ssid + '\"'
        test = test + ',' + ssid
    json_string = settings_json.split("\"insertion\"")
    settings_json = json_string[0] + test[1:len(test)] + json_string[1]
    return settings_json

''' 
    Function: Connects to specified WiFi network using specified pwd
    Parameters: str interface (to connect with), str ssid (to connect to), 
                str password (to use)
    Returns: None
    ChangeWifi("Some_Network", "password")
''' 
def ChangeWifi(interface, ssid, password):
    cell = Cell.all(interface)[0]
    scheme = Scheme.for_cell(interface, 'robot_connection', ssid, password)
    scheme.save()
    scheme.activate()
    return None

############################################################
############# KIVY CLASSES #################################
############################################################

'''
    Class: Defines a new type of SettingOptions for autogenerated
           WiFi list
    Parameters: SettingOptions
'''
class WifiList(SettingOptions):
    pass

'''
    Class: Defines a new type of label for passwords
    Parameters: Label object
'''
class PasswordLabel(Label):
    pass

'''
    Class: Defines how password string is handled inside 
           main Config page
    Parameters: SettingString object
'''
class SettingPassword(SettingString):
    def _create_popup(self, instance):
        super(SettingPassword, self)._create_popup(instance)
        self.textinput.password = True

    def add_widget(self, widget, *largs):
        if self.content is None:
            super(SettingString, self).add_widget(widget, *largs)
        if isinstance(widget, PasswordLabel):
            return self.content.add_widget(widget, *largs)

'''
    Class: Interface object that drives most of the GUI
    Parameters: RelativeLayout defines how objects are ordered
'''
class Interface(RelativeLayout):
    robot_number = GetIniFile("robot.ini","robot")["robot_number"]
    battery = GetBattery()

    def quit_program(self):
        sys.exit(0)

    def get_value(self):
        print self.ids.slider_bar.value

    def change_value(self):
        self.ids.robot_number_label.text = 'Test: ' + robot_number

    # This should be called every 1/3 of a second
    def update(self, dt):
        self.ids.robot_number_label.text = 'Robot: ' + GetIniFile("robot.ini","robot")["robot_number"]
        self.ids.time.text = GetDate()
        Robot_ID = Robot_Password = "robot01"

    # This should be called every 2.5 minutes
    def update_battery(self, dt):
        self.ids.battery_bar.value = GetBattery()
        self.ids.battery_text.text = str(GetBattery()) + '%'

    def get_command(self, dt):
        GetCommand()

    def get_call(self, dt):
        if GetCall():
            PlaceCall()

'''
    Class: Main kivy app for GUI and managing time interruptions
'''
class RobotApp(App):

    '''
        Function: builds self
        Parameters: self referencing
        Returns: Interface app
    '''
    def build(self):
        app = Interface()

        self.use_kivy_settings = False

        # This just gets the robot_number current setting from self.config
        setting = self.config.get('robot', 'robot_number')

        Clock.schedule_interval(app.update, 1.0 / 60.0)
        Clock.schedule_interval(app.update_battery, 150.0)
        Clock.schedule_interval(app.get_command, 1.0 / 60.0)
        Clock.schedule_interval(app.get_call, 6.0 / 60.0)

        return app

    '''
        Function: builds configuration defaults
        Parameters: self referencing, global config object
        Returns: None
    '''
    def build_config(self, config):
        config.setdefaults('robot', {
            'robot_number': GetIniFile("robot.ini","robot")["robot_number"],
            'options_wifi': 'Some WiFi',
            'wifi_password': ''})

    def update_settings():
        pass

    '''
        Function: builds settings screen
        Parameters: self referencing, global settings object
        Returns: None
    '''
    def build_settings(self, settings):
        settings.register_type('password', SettingPassword)
        settings.register_type('dynamic_list', WifiList)
        settings.add_json_panel('Robot Settings',
                                self.config,
                                data=settings_json)

    '''
        Function: change setting when global configuration changes
        Parameters: self referencing, global config object,
                    key object, self value
        Returns: None
    '''
    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value
        if(key == 'options_wifi'):
            InfoLog("Changed WiFi to: " + GetIniFile("robot.ini","robot")["options_wifi"])
            #print "Changing WiFi"
            #ChangeWifi(GetIniFile("robot.ini","robot")["options_wifi"],
            #           GetIniFile("robot.ini","robot")["wifi_password"])

############################################################
############# KIVY BUILDER #################################
############################################################

Builder.load_string('''
<Interface>:
    canvas.before:
        Color:
            rgb: 0.356862745,0.117647059,0.517647059,1
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
    ConfigKivy()
    print Serial_Commands['forward']
    settings_json = ChangeSettings(settings_json)
    RobotApp().run()
    # while 1:
    #     SendMessage(ser,"Hola")
    #     time.sleep(5)
    #     print GetMessage(ser)
    # while 1:
    #     print GetCommand()
    # PlaceCall()
    # while 1:
    #     GetCall()
