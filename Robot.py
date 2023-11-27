import serial
import re
import time

from Pose import Pose

class Robot:
    def __init__(self, port):
        self.ser = serial.Serial(port)
        self.ser.write(b"CON \r")
        time.sleep(1)
        self.ser.write(b"HOME \r")
        time.sleep(180)
        response = self.ser.read_all()
        print(response.decode('ascii'))

        self.pose = Pose()

        self.get_intial_position()

    def get_intial_position(self):
        self.ser.write(b"HERE P1 \r")
        time.sleep(1)
        self.ser.write(b"LISTPV P1 \r")
        time.sleep(1)
        response = self.ser.read_all()
        pattern = "X:([\s-]\d+)\s*Y:([\s-]\d+)\s*Z:([\s-]\d+)\s*P:([\s-]\d+)\s*R:([\s-]\d+)"
        match = re.search(pattern, response.decode('ascii'))
        self.pose.update_pose([
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5))
        ])

    
    '''
    Starts from the initial position and updates the position
    '''

    def move_robot_x(self, increment):

            self.pose.update_pose([
                self.pose.position.x + increment,
                self.pose.position.y,
                self.pose.position.z,
                self.pose.orientation.roll,
                self.pose.orientation.pitch,
            ])
            position_command = "SETPVC P1 X " + self.pose.position.x
            self.ser.write(bytes(position_command, encoding='utf-8'))
            self.ser.read_all() # prints Done.
            self.ser.write(b"MOVE P1")
            self.ser.read_all() # prints Done.

    def move_robot_y(self, increment):

        self.pose.update_pose([
            self.pose.position.x,
            self.pose.position.y + increment,
            self.pose.position.z,
            self.pose.orientation.roll,
            self.pose.orientation.pitch,
        ])

        self.ser.write(b"SETPVC P1 Y", self.pose.position.y)
        self.ser.read_all()
        self.ser.write(b"MOVE P1")
        self.ser.read_all()

    def move_robot_z(self, increment):

        self.pose.update_pose([
            self.pose.position.x,
            self.pose.position.y,
            self.pose.position.z + increment,
            self.pose.orientation.roll,
            self.pose.orientation.pitch,
        ])

        self.ser.write(b"SETPVC P1 Z", self.pose.position.z)
        self.ser.read_all()
        self.ser.write(b"MOVE P1")
        self.ser.read_all()

    def move_robot_pitch(self, increment):

        self.pose.update_pose([
            self.pose.position.x,
            self.pose.position.y,
            self.pose.position.z,
            self.pose.orientation.roll,
            self.pose.orientation.pitch + increment,
        ])

        self.ser.write(b"SETPVC P1 P", self.pose.orientation.pitch)
        self.ser.read_all()
        self.ser.write(b"MOVE P1")
        self.ser.read_all()

    def move_robot_roll(self, increment):

        self.pose.update_pose([
            self.pose.position.x,
            self.pose.position.y,
            self.pose.position.z,
            self.pose.orientation.roll + increment,
            self.pose.orientation.pitch,
        ])

        self.ser.write(b"SETPVC P1 R", self.pose.orientation.roll)
        self.ser.read_all()
        self.ser.write(b"MOVE P1")
        self.ser.read_all()

    '''
    
    def move_robot(self, increment, coord):

        self.pose.update_pose([
            self.pose.position.x + increment,
            self.pose.position.y,
            self.pose.position.z,
            self.pose.orientation.roll,
            self.pose.orientation.pitch,
        ])

        self.ser.write(b"SETPVC P1 %s %f" % (coord, self.pose.position.x))

        self.ser.write(b"MOVE P1")
    '''

    def print_pose(self):
        print(self.pose)

# port = "COM4"
# robot = Robot(port)
# robot.update_current_position()
# robot.print_pose()
