import sys
import glob
import serial
import time
import csv
import argparse
from datetime import datetime

flag_print = 0

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
  cmd = "GWTL\r"
  s.write(bytes(cmd,"utf-8"))
  time.sleep(0.1)
  response2 = s.read(s.in_waiting)
  response2 = response2.decode('utf-8')[8:-2]
#  response2 = response2[:-2]
  response2 += ',' + response
  s.close()
  if flag_print:
    print(response2)
  return response2

def writeDataToFile(data):
  with open('test.csv', 'a') as f:
#    writer = csv.writer(f)
#    writer.writerow(data)
    f.write('%s,'%datetime.now() + data )
  

def trackWaterCalibration(serial_port):
  data = readWaterCalibration(serial_port)
  writeDataToFile(data)

def parseArguments():
  parser = argparse.ArgumentParser(
    description='This application reads the water level and calibration from a Habitat H1 humidifier, then stores the information as a time series to a .csv file named "test.csv"',
  )
  parser.add_argument('--print', '-p', action="store_true", default=False, 
                      help="If included, prints the data read from the device")
  parser.add_argument('--sleep', '-s', action="store", dest="sleep_time", default=60, type=int,
                      help="The time in seconds between readings, default=60")

  result = parser.parse_args()

  return result.print, result.sleep_time

if __name__ == '__main__':
  flag_print, sleep_time = parseArguments()
  s = serial_ports()
  while(1):
    trackWaterCalibration(s)
    time.sleep(sleep_time)