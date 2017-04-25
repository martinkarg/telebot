import time
import serial

ser = serial.Serial(
  port="/dev/ttyUAMA0",
  baudrate = 9600,
  parity = serial.PARITY_NONE,
  stopbits = serial.STOPBITS_ONE,
  bytesize = serial.EIGHTBITS,
  timeout = 1
)
counter = 0

while 1:
  x = ser.readline()
  print x
  time.sleep(1)
  ser.write("Hello, World")
