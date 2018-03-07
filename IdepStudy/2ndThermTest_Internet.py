from serial import Serial
import re
import time

serial_pattern = r"T: (\d+\.\d*)\n";
serial_port = '/dev/ttyACM0';
serial_bauds = 9600;

def open_serial_port() :
  s = Serial(serial_port, serial_bauds);
  line = s.readline();
  print ("---The Open Serial Method is Running---")
  return s

def read_temperature(s):
  line = s.readline();
  m = re.match(serial_pattern, line);
  print("---The read temp method is running---")
  return float(m.group(1))


bool1 = True
while(bool1):
  read_temperature(open_serial_port())
  i += 1
  if (i == 100):
    bool1 = False
  print("this is iteration number " + i + " of the while loop")
  sleep(5/1000.0)

