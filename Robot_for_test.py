import serial
import re
import time
import pygame
import sys
import numpy as np
import math
import cv2

class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Orientation:
    def __init__(self):
        self.roll = 0
        self.pitch = 0

class Pose:
    def __init__(self):
        self.position = Position()
        self.orientation = Orientation()

    def update_pose(self, pose_array):
        self.position.x = pose_array[0]
        self.position.y = pose_array[1]
        self.position.z = pose_array[2]
        self.orientation.pitch = pose_array[3]
        self.orientation.roll = pose_array[4]

    def __str__(self):
        return f"X: {self.position.x}, Y: {self.position.y}, Z: {self.position.z}, P: {self.orientation.pitch}, R: {self.orientation.roll}"
    
class Robot:
    def __init__(self, port):
        self.ROBOT_INITIAL_POSITION = [b"5440\r", b"-353\r", b"2616\r", b"-853\r", b"-201\r"]
        self.ROBOT_OPTION_1 = ""
        self.ROBOT_OPTION_2 = ""
        self.ROBOT_OPTION_3 = ""
        self.ROBOT_OPTION_4 = ""
        
        self.ser = serial.Serial(port)
        
        self.ser.write(b"CON \r")
        time.sleep(1)

        self.mode = None
        self.movement_mode = None
        self.set_mode('manual')
        self.set_movement_mode('J')
                
        time.sleep(1)

        self.speed_mode = 'slow'
        self.set_speed_mode('slow')

        self.commands = {
            'x': {
                'increase': '1',
                'decrease': 'Q',
            },
            'y': {
                'increase': '2',
                'decrease': 'W',
            },
            'z': {
                'increase': '3',
                'decrease': 'E',
            },
            'p': {
                'increase': '4',
                'decrease': 'R',
            },
            'r': {
                'increase': '5',
                'decrease': 'T',
            },
        }

    def close(self):
        self.ser.close()

    def set_speed_mode(self, speed_mode):
        if speed_mode == self.speed_mode:
            return
        self.speed_mode = speed_mode
        if speed_mode == 'fast':
            self.ser.write(b"S\r")
            time.sleep(0.2)
            self.ser.write(b"20\r")
        elif speed_mode == 'slow':
            self.ser.write(b"S\r")
            time.sleep(0.2)
            self.ser.write(b"5\r")
        time.sleep(0.5)

    def change_speed(self):
        if self.speed_mode == 'fast':
            self.set_speed_mode('slow')
        elif self.speed_mode == 'slow':
            self.set_speed_mode('fast')

    def home(self, port):
        self.ser.write(b"HOME \r")
        time.sleep(180)

    def set_movement_mode(self, movement_mode):
        if movement_mode == self.movement_mode:
            return

        self.movement_mode = movement_mode
        if movement_mode == 'J':
            self.ser.write(b"J\r")
        if movement_mode == 'X':
            self.ser.write(b"X\r")

    def set_mode(self, mode):
        if mode == self.mode:
            return

        self.mode = mode
        self.ser.write(b"~\r")
        
        if mode == "manual":
            desired_command = "MANUAL MODE!"
            undesired_command = "EXIT"
        elif mode == "auto":
            desired_command = "EXIT"
            undesired_command = "MANUAL MODE!"

        check = ''
        start_time = time.time()
        while True:
            check += self.ser.read_all().decode('ascii')
            print(check)

            if bool(re.search(undesired_command, check)):
                self.ser.write(b"~\r")
                return
            if bool(re.search(desired_command, check)):
                return

            if time.time() - start_time > 10: 
                raise TimeoutError

            time.sleep(0.05)

        # if bool(re.search("DISABLED", check)) or bool(re.search("IMPACT", response)):
        #     if self.mode == 'manual':
        #         self.ser.write(b"C \r")
        #     else:
        #         self.ser.write(b"CON \r")

    def move_manual(self, axis: str, direction: str):
        self.set_mode('manual')
        if direction not in ['increase', 'decrease']:
            raise ValueError("Direction must be 'increase' or 'decrease'")

        if axis not in ['x', 'y', 'z', 'p', 'r']:
            raise ValueError("Axis must be 'x', 'y', 'z', 'p' (pitch) or 'r' (roll)")

        if axis in ['p', 'r'] and self.movement_mode == 'X':
            self.set_movement_mode('J')
        if axis in ['x', 'y', 'z'] and self.movement_mode == 'J':
            self.set_movement_mode('X')

        command_to_send = self.commands[axis][direction]
        self.ser.write(bytes(f"{command_to_send} \r", encoding='utf-8'))
        self.check_messages()

    def move_automatic(self, position_command):
        self.set_mode('auto')
        self.ser.write(b"TEACH P0 \r") #put intermediate position?
        time.sleep(0.1)
        for command in position_command:
            self.check_messages()
            self.ser.write(command)
            time.sleep(0.1)
        
        self.ser.write(b"MOVE P0\r")
        
    def check_messages(self):
        response = self.ser.read_all().decode('ascii')
        if bool(re.search("DISABLED", response)) or bool(re.search("IMPACT", response)):
            if self.mode == 'manual':
                self.ser.write(b"C \r")
            else:
                self.ser.write(b"CON \r")
                
        print(response)

    def print_pose(self):
        print(self.pose)

class Controller:
    def __init__(self, idx):
        self.joystick = pygame.joystick.Joystick(idx)
        self.joystick.init()
        self.threshold = 0.9
        self.axes = []
        self.buttons = []

    def get_input_state(self):
        self.axes = [round(self.joystick.get_axis(i), 1) for i in range(self.joystick.get_numaxes())]
        self.buttons = [self.joystick.get_button(i) == 1 for i in range(self.joystick.get_numbuttons())]

        return self.axes, self.buttons
    
def process_input(axes, buttons, robot_bisturi):# which_robot, robot_camera):
    threshold = 0.9
    # if which_robot == 'bisturi':
    #     # robot = robot_bisturi
    #     print("robot_bisturi")
    # elif which_robot == 'camera':
    #     print("robot_camera")
        # robot = robot_camera
    if buttons[0]:
        print(" show camera option menu") # Risk of pressing the button after
        if axes[0] >= threshold:
            print("option 3")
        if axes[0] <= -threshold:
            print("option 1")
        if axes[1] >= threshold:
            print("option 2")
        if axes[1] <= -threshold:
            print("option 4")
    elif buttons[1]:
        print("nothing")
    elif buttons[2]:
        # robot_bisturi.move_automatic(robot_bisturi.ROBOT_INITIAL_POSITION)
        print("reposition robot") # Should we do a verification before? Like press twice with message on the first time
    elif buttons[3]:
        print("nothing")
    # elif buttons[7]:
    #     print("change manipulator")
    #     if which_robot == 'bisturi':
    #         return 'camera'
    #     else:
    #         return 'bisturi'
        

    if buttons[4] and not buttons[6]:
        robot_bisturi.move_manual('z', 'decrease')
        print("Decrease z")
    elif not buttons[4] and buttons[6]:
        robot_bisturi.move_manual('z', 'increase')
        print("Increase z")

    if axes[0] >= threshold:
        robot_bisturi.move_manual('y', 'increase')
        print("Increase y")
    elif axes[0] <= -threshold:
        robot_bisturi.move_manual('y', 'decrease')
        print("Decrease y")

    if axes[1] >= threshold:
        robot_bisturi.move_manual('x', 'decrease')
        print("Decrease x")
    elif axes[1] <= -threshold:
        robot_bisturi.move_manual('x', 'increase')
        print("Increase x")

    if axes[2] >= threshold:
        robot_bisturi.move_manual('r', 'increase')
        print("Increase roll")
    elif axes[2] <= -threshold:
        robot_bisturi.move_manual('r', 'decrease')
        print("Decrease roll")

    if axes[3] >= threshold:
        robot_bisturi.move_manual('p', 'decrease')
        print("Decrease pitch")
    elif axes[3] <= -threshold:
        robot_bisturi.move_manual('p', 'increase')
        print("Increase pitch")
    # return which_robot

pygame.init()
pygame.joystick.init()

robot_bisturi = Robot("COM7")
robot_camera = Robot("COM8")
controller = Controller(0)


running = True
# previous_button_states = []



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # robot_bisturi.close()
            pygame.quit()
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 8:
                print("speed change")
                robot_bisturi.change_speed()
    
    axes, buttons = controller.get_input_state()
    # which_robot = 'bisturi'
    # which_robot = 
    process_input(axes, buttons, robot_bisturi)#, which_robot, robot_camera)

    time.sleep(0.05)