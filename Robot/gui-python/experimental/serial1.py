
import time
import serial

ser = serial.Serial(
  port="/dev/ttyAMA0",
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)
counter = 0

serial_commands = {
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

while 1:
  x = ser.readline()
  print "Esperando mensaje..."
  print x
  time.sleep(1)
  print "Mandando mensaje..."
  ser.write("Hello, World")
