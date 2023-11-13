import serial
import time
import re

ser = serial.Serial("COM13")

ser.write(b"CON \r")
time.sleep(1)
ser.write(b"HERE P1 \r")
time.sleep(1)
ser.write(b"LISTPV P1 \r")
time.sleep(1)
thing = ser.read_all()
pattern = "X:([\s-]\d+)\s*Y:([\s-]\d+)\s*Z:([\s-]\d+)"
match = re.search(pattern, thing.decode('ascii'))
print('X:', int(match.group(1)))
print('Y:', int(match.group(2)))
print('Z:', int(match.group(3)))
ser.close()