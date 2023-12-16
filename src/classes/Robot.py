import time
import serial
import re

class Robot:
    def __init__(self, port):
        self.ROBOT_INITIAL_POSITION = [b"5440\r", b"-353\r", b"2616\r", b"-853\r", b"-200\r"]
        self.ROBOT_OPTION_1 = [b"0\r", b"-0\r", b"-154\r", b"-1\r", b"0\r"]
        self.ROBOT_OPTION_2 = [b"-595\r", b"57\r", b"-28450\r", b"24110\r", b"0\r"] # second one should be different
        self.ROBOT_OPTION_3 = [b"-595\r", b"57\r", b"-28450\r", b"24110\r", b"0\r"] # second one should be different
        self.ROBOT_OPTION_4 = [b"7534\r", b"-353\r", b"6523\r", b"78\r", b"-200\r"] # The same as 1 for now
        
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

        self.check_messages(self.ser.read_all().decode('ascii'))


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
            self.check_messages(check)

            if bool(re.search(undesired_command, check)):
                self.ser.write(b"~\r")
                self.mode = mode
                return
            if bool(re.search(desired_command, check)):
                self.mode = mode
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
        self.check_messages(self.ser.read_all().decode('ascii'))

    def move_automatic(self, position_command):
        self.set_mode('auto')
        self.ser.write(b"TEACH P0 \r") #put intermediate position?
        time.sleep(0.1)
        for command in position_command:
            self.check_messages(self.ser.read_all().decode('ascii'))
            self.ser.write(command)
            time.sleep(0.1)
        
        self.ser.write(b"MOVE P0\r")
        time.sleep(1)
        
    def move_automatic_joints(self, position_command):
        self.set_mode('auto')
        self.ser.write(b"SETPV P0 \r") #put intermediate position?
        time.sleep(0.1)
        for command in position_command:
            self.check_messages(self.ser.read_all().decode('ascii'))
            self.ser.write(command)
            time.sleep(0.1)
        
        self.ser.write(b"MOVE P0\r")
        time.sleep(1)

    
    def move_one_by_one(self, position_command):
        self.set_mode('auto')
        
        self.ser.write(b"HERE P1 \r")
        time.sleep(0.1)
        self.ser.write(b"SETPV P1 1 -7000\r")
        time.sleep(0.5)
        self.ser.write(b"MOVE P1 \r")
        time.sleep(0.5)
        
        temp_position_command = position_command.copy()
        temp_position_command[0] = b'-7000\r'
        self.move_automatic_joints(temp_position_command)
        time.sleep(4)
        self.move_automatic_joints(position_command)
        
 
        
    def check_messages(self, response):
        print(response)
        # response = self.ser.read_all().decode('ascii')
        if bool(re.search("DISABLED", response)) or bool(re.search("IMPACT", response)):
            print("ASKJHDS")
            if self.mode == 'manual':
                self.ser.write(b"C \r")
            else:
                self.ser.write(b"CON \r")
                
        print(response)

    def print_pose(self):
        print(self.pose)