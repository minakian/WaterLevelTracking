import sys
import glob
import serial
import time
import csv
from datetime import datetime


def serial_ports():
  """ Opens a port with the H1 Humidifier
      Reads the water tank information every X seconds
      Writes that data to a .csv file
  """
  if sys.platform.startswith('win'):
    ports = ['COM%s' % (i + 1) for i in range(256)]
  elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    # this excludes your current terminal "/dev/tty"
    ports = glob.glob('/dev/tty[A-Za-z]*')
  elif sys.platform.startswith('darwin'):
    ports = glob.glob('/dev/tty.usb*')
  else:
    raise EnvironmentError('Unsupported platform')

  result = []
  for port in ports:
    try:
      s = serial.Serial(port, baudrate=115200)
      cmd = "GFWV\r"
      s.write(bytes(cmd,"utf-8"))
      time.sleep(0.1)
      response = s.read(s.in_waiting)
      try:
        print(response[5])
        print(s)
        if(response[5] == 70):
          return port
        print('No Port')
        return port
      except:
        print("Invalid Data")
    except:
        print("invalid port")
#      result.append(port)
      

#  return result

def readWaterCalibration(serial_port):
  s = serial.Serial(serial_port, baudrate=115200)
  cmd = "WATER\r"
  s.write(bytes(cmd,"utf-8"))
  time.sleep(0.1)
  response = s.read(s.in_waiting)
  response = response.decode('utf-8')[6:]
  s.close()
  return response

def writeDataToFile(data):
  with open('test.csv', 'a') as f:
#    writer = csv.writer(f)
#    writer.writerow(data)
    f.write('%s,'%datetime.now() + data )
  

def trackWaterCalibration(serial_port):
  data = readWaterCalibration(serial_port)
  writeDataToFile(data)

if __name__ == '__main__':
  s = serial_ports()
  while(1):
    trackWaterCalibration(s)
    time.sleep(60)