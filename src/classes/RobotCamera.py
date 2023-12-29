import time
import serial
import re

class RobotCamera:
    def __init__(self, port, home=False):
        
        self.camera_position_options = {
            1: [b"2000\r", b"-12249\r", b"-8210\r", b"-25802\r", b"0\r"],
            2: [b"2000\r", b"-13687\r", b"-27171\r", b"-3323\r", b"0\r"],
            3: [b"2000\r", b"-1167\r", b"-26033\r", b"13945\r", b"0\r"]
        }

        self.ser = serial.Serial(port)
        
        if home:
            print("Homing robot")
            self.home()
        
        self.ser.write(b"CON \r")
        time.sleep(1)

        self.mode = None
        self.movement_mode = None

        self.set_mode('auto')
                
        time.sleep(1)

        self.check_messages(self.ser.read_all().decode('ascii'))
        
        self.current_option = None
        self.move_one_by_one(1)

        self.commands = {
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

    def home(self):
        self.ser.write(b"HOME \r")
        time.sleep(180)

    def enable_conection(self):
        self.ser.write(b"CON \r")
        time.sleep(0.1)

    def set_mode(self, mode):
        if mode == self.mode:
            print("Mode already set to", mode)
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

    def move_manual(self, axis: str, direction: str):
        self.set_mode('manual')
        if direction not in ['increase', 'decrease']:
            raise ValueError("Direction must be 'increase' or 'decrease'")

        if axis not in ['p', 'r']:
            raise ValueError("Axis for the Camera Robot must be 'p' (pitch) or 'r' (roll)")

        command_to_send = self.commands[axis][direction]
        self.ser.write(bytes(f"{command_to_send} \r", encoding='utf-8'))
        self.check_messages(self.ser.read_all().decode('ascii'))
  
    def move_one_by_one(self, option):
        if option == self.current_option:
            print("Option already selected")
            return
        
        self.current_option = option
        position_command = self.camera_position_options[option]
        
        print("Changing to auto mode")
        self.set_mode('auto')
        
        print("First movement")
        self.ser.write(b"HERE P1 \r")
        time.sleep(0.1)
        self.ser.write(b"SETPV P1 1 -7000\r")
        time.sleep(0.5)
        self.ser.write(b"MOVE P1 \r")
        time.sleep(0.5)

        self.check_messages(self.ser.read_all().decode('ascii'))

        print("Second movement")
        temp_position_command = position_command.copy()
        temp_position_command[0] = b'-7000\r'
        
        self.ser.write(b"SETPV P1\r")
        time.sleep(0.1)

        for command in temp_position_command:
            print(command)
            self.ser.write(command)
            response = self.ser.read_all().decode('ascii')
            self.check_messages(response)
            time.sleep(0.1)

        self.ser.write(b"MOVE P1\r")
        time.sleep(2)

        print("Third movement")
        self.ser.write(b"SETPV P1\r")
        time.sleep(0.1)
        for command in position_command:
            print(command)
            self.ser.write(command)
            response = self.ser.read_all().decode('ascii')
            self.check_messages(response)
            time.sleep(0.1)
        self.ser.write(b"MOVE P1 \r")
        time.sleep(0.5)
        
    def check_messages(self, response):
        print(response)
        # response = self.ser.read_all().decode('ascii')
        if bool(re.search("DISABLED", response)) or bool(re.search("IMPACT", response)):
            print("ASKJHDS")
            if self.mode == 'manual':
                self.ser.write(b"C \r")
            else:
                self.ser.write(b"CON \r")
            return True

        if response != '': print(response)

        return False

    def print_pose(self):
        print(self.pose)