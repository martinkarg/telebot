# Import library for serial communication
import serial
# Import library for using/processing system time
import time
# Import selenium for web automation
import selenium
# Import library to make web requests
import requests

# GLOBAL VARS

global ser

global Serial_Commands
Serial_Commands = {
    'forward': 16,
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
    'level_3': 3
}

global Key_Commands
Key_Commands = {
        'w': Serial_Commands['forward'],
        's': Serial_Commands['stop'],
        'a': Serial_Commands['left'],
        'd': Serial_Commands['right'],
        'q': Serial_Commands['anti_clockwise'],
        'e': Serial_Commands['clockwise']
    }

global Old_Commands
Old_Commands = " "

# FUNCTIONS

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

if __name__ == '__main__':
    while 1:
        print GetCommand()