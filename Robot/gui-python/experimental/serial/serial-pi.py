import serial
import time

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

def SendMessage(ser, message):
    ser.write(message)
    return True

def GetMessage(ser):
    serial_message = ser.readline()
    return serial_message

if __name__ == '__main__':
  ser = StartSerial()
  while 1:
    SendMessage(ser,"Hola")
    time.sleep(5)
    print GetMessage(ser)