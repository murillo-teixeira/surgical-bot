import time
import serial
import re

class RobotBisturi:
    def __init__(self, port, home=False, debug=False):
        self.debug = debug
        # Update to joints
        self.ROBOT_INITIAL_POSITION = [b"0\r", b"8206\r", b"-1756\r", b"-18935\r", b"0\r"]
        self.ROBOT_INITIAL_POSITION_XYZ = [5593, -353, 591, -903, -201]

        self.ser = serial.Serial(port)
        if home:
            if self.debug: print("Homing robot")
            self.home()

        self.ser.write(b"CON \r")
        time.sleep(1)

        self.mode = None
        self.movement_mode = None

        self.move_to_home()
        self.estimate_robot_position = self.ROBOT_INITIAL_POSITION_XYZ.copy()
        
        time.sleep(1)

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
                'increase_value_fast': 17.5,
                'decrease_value_fast': -17.5,
                'increase_value_slow': 17.5/4,
                'decrease_value_slow': -17.5/4,
            },
            'y': {
                'increase': '2',
                'decrease': 'W',
                'increase_value_fast': 17.5,
                'decrease_value_fast': -17.5,
                'increase_value_slow': 17.5/4,
                'decrease_value_slow': -17.5/4,
            },
            'z': {
                'increase': '3',
                'decrease': 'E',
                'increase_value_fast': 17.3,
                'decrease_value_fast': -17.3,
                'increase_value_slow': 17.3/4,
                'decrease_value_slow': -17.3/4,
            },
            'p': {
                'increase': '4',
                'decrease': 'R',
                'increase_value': 1,
                'decrease_value': 1,
            },
            'r': {
                'increase': '5',
                'decrease': 'T',
                'increase_value': 1,
                'decrease_value': 1,
            },
        }

    def close(self):
        self.ser.close()

    def enable_conection(self):
        self.ser.write(b"CON \r")
        time.sleep(0.1)

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

    def home(self):
        self.ser.write(b"HOME \r")
        time.sleep(180)

    def get_position_estimate(self):
        return self.estimate_robot_position[0:3]

    def update_current_estimate_position(self, axis, direction):
        axis_index = list(self.commands.keys()).index(axis)
        if direction == 'increase' and self.speed_mode == 'fast':
            self.estimate_robot_position[axis_index] += self.commands[axis]['increase_value_fast']
        elif direction == 'decrease' and self.speed_mode == 'fast':
            self.estimate_robot_position[axis_index] += self.commands[axis]['decrease_value_fast']
        elif direction == 'increase' and self.speed_mode == 'slow':
            self.estimate_robot_position[axis_index] += self.commands[axis]['increase_value_slow']
        elif direction == 'decrease' and self.speed_mode == 'slow':
            self.estimate_robot_position[axis_index] += self.commands[axis]['decrease_value_slow']

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
            if self.debug: print(check)

            if bool(re.search(undesired_command, check)):
                self.ser.write(b"~\r")
                return
            if bool(re.search(desired_command, check)):
                return

            if time.time() - start_time > 10: 
                raise TimeoutError

            time.sleep(0.05)

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

        self.update_current_estimate_position(axis, direction)
      
    def move_to_home(self):
        self.set_mode('auto')
        time.sleep(1)
        self.ser.write(b"SETPV P0 \r") #put intermediate position?
        time.sleep(1)
        for command in self.ROBOT_INITIAL_POSITION:
            self.check_messages(self.ser.read_all().decode('ascii'))
            self.ser.write(command)
            time.sleep(0.1)
        
        self.ser.write(b"MOVE P0\r")
        self.estimate_robot_position = self.ROBOT_INITIAL_POSITION_XYZ.copy()
        time.sleep(1)

    def get_current_position(self):
        self.set_mode('auto')
        time.sleep(0.2)
        self.ser.write(b"HERE P1 \r")
        time.sleep(0.1)
        self.ser.write(b"LISTPV P1 \r")
        time.sleep(0.5)
        response = self.ser.read_all().decode('ascii')
        if self.debug: print(response)
        self.check_messages(response)
        pattern = "X:([\s-]\d+)\s*Y:([\s-]\d+)\s*Z:([\s-]\d+)\s*P:([\s-]\d+)\s*R:([\s-]\d+)"
        match = re.search(pattern, response)
        self.estimate_robot_position = [
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            int(match.group(4)),
            int(match.group(5))
        ]
       
    def check_messages(self, response):
        if self.debug: print(response)
        # response = self.ser.read_all().decode('ascii')
        if bool(re.search("DISABLED", response)) or bool(re.search("IMPACT", response)):
            if self.mode == 'manual':
                self.ser.write(b"C \r")
            else:
                self.ser.write(b"CON \r")
                
        if response != '' and self.debug: print(response)

    def print_pose(self):
        print(self.pose)