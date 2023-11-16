import serial
import re
import time

class Robot:
    def __init__(self, port):
        self.ser = serial.Serial(port)
        self.ser.write(b"CON \r")
        time.sleep(1)
        self.ser.write(b"HOME \r")
        time.sleep(1)
        response = ser.read_all()
        print(response.decode('ascii'))

        self.position = None
        self.orientation = None


    def update_current_position(self):
        self.ser.write(b"HERE P1 \r")
        time.sleep(1)
        self.ser.write(b"LISTPV P1 \r")
        time.sleep(1)
        response = self.ser.read_all()
        pattern = "X:([\s-]\d+)\s*Y:([\s-]\d+)\s*Z:([\s-]\d+)\s*P:([\s-]\d+)\s*R:([\s-]\d+)"
        match = re.search(pattern, response.decode('ascii'))
        self.position = [
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3))
        ]
        self.orientation = [
            int(match.group(4)),
            int(match.group(5)),
        ]

    def print_pose(self):
        print("Position:", self.position)
        print("Orientation:", self.orientation)

port = "COM13"
robot = Robot(port)
robot.update_current_position()
robot.print_pose()
