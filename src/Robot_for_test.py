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
    #def get_position

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
    a = 0
    b = 0
    c = 0
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
        c = -1
    elif not buttons[4] and buttons[6]:
        robot_bisturi.move_manual('z', 'increase')
        print("Increase z")
        c = 1

    if axes[0] >= threshold:
        robot_bisturi.move_manual('y', 'increase')
        print("Increase y")
        b = 1
    elif axes[0] <= -threshold:
        robot_bisturi.move_manual('y', 'decrease')
        print("Decrease y")
        b = -1

    if axes[1] >= threshold:
        robot_bisturi.move_manual('x', 'decrease')
        print("Decrease x")
        a = -1
    elif axes[1] <= -threshold:
        robot_bisturi.move_manual('x', 'increase')
        print("Increase x")
        a = 1

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

    return a,b,c

pygame.init()
pygame.joystick.init()

robot_bisturi = Robot("COM12")
#robot_camera = Robot("COM9")
controller = Controller(0)


running = True
# previous_button_states = []

# Function to create a gradient-filled rectangle
def draw_gradient_rect(surface, rect, color1, color2):
    color1 = pygame.Color(*color1)
    color2 = pygame.Color(*color2)

    for y in range(200):
        if y >= rect.height:
            break
        t = y / 200
        color = pygame.Color(
            int((1 - t) * color1.r + t * color2.r),
            int((1 - t) * color1.g + t * color2.g),
            int((1 - t) * color1.b + t * color2.b),
            int((1 - t) * color1.a + t * color2.a)
        )
        pygame.draw.line(surface, color, (rect.x, rect.y + rect.height - y), (rect.x + rect.width, rect.y + rect.height - y))


# set max values for x, y, z
x_max = 7
y_max = 7
z_max = 5

# Set up the Pygame window
width, height = 900, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robotis GUI")

# Load background image
background_image = pygame.image.load("background.png")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (width, height))


# Set up the camera
camera = cv2.VideoCapture(1)  # Change the argument to the camera index if using an external camera

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()


# Function to show a popup message with a waiting animation
def show_popup_message(message, font, window):
    popup_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
    popup_rect = popup_surface.get_rect(center=(width // 2, height // 2))

    # Draw the popup background
    pygame.draw.rect(popup_surface, (255, 255, 255, 200), popup_rect)

    # Draw the message
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(popup_rect.width // 2, popup_rect.height // 2 - 10))
    popup_surface.blit(text, text_rect)

    # Draw a waiting animation (e.g., rotating line)
    angle = 0
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.line(popup_surface, (0, 0, 0), (popup_rect.width // 2, popup_rect.height - 20),
                         (popup_rect.width // 2 + int(20 * np.cos(angle)),
                          popup_rect.height - 20 + int(20 * np.sin(angle))), 2)

        angle += 0.1
        count += 0.1
        if count >= 6.3:
            print("cheguei")
            angle = 0
            count = 0
            # Clear the surface to remove the popup
            popup_surface.fill((0, 0, 0, 0))
            window.blit(background_image, (0, 0))
            popup_surface.blit(text, text_rect)

        window.blit(background_image, (0, 0))
        window.blit(popup_surface, popup_rect.topleft)
        pygame.display.flip()

        clock.tick(30)

# put here the function that gets the values of x y and z
x = 0
y = 0
z = 0
print(controller)
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

        # Draw background image
    window.blit(background_image, (0, 0))

    # Capture video frame from the camera
    ret, frame = camera.read()

    # Resize the frame
    frame = cv2.resize(frame, (574, 359))

    # Convert OpenCV image to Pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    window.blit(frame, (35, 75))


    
    axes, buttons = controller.get_input_state()
    # which_robot = 'bisturi'
    # which_robot =

    a,b,c = process_input(axes, buttons, robot_bisturi)#, which_robot, robot_camera)
    x +=a
    y+=b
    z+=c
    if x >= x_max:
        x = x_max
    if y >= y_max:
        y = y_max
    if z >= z_max:
        z = z_max
    if x <= 0:
        x = 0
    if y <= 0:
        y = 0
    if z <= 0:
        z = 0
    # x and y axes
    # arrow head points -> upper point (665, 70) ,  lower point (840, 250)
    x_point = int(x * 175 / x_max + 665)
    y_point = int(250 - y * 180 / y_max)
    pygame.draw.circle(window, (177, 80, 251), (x_point, y_point), 3)  # circle

    # z
    # bar points -> upper point (760,285), lower point (760, 485)
    z_point = int(485 - z * 200 / z_max)
    bar_length = int(z * 200 / z_max)
    left_graph_rect = pygame.Rect(760 - 10, z_point, 20, bar_length)

    gradient_color1 = (104, 239, 243, 255)  # Top color
    gradient_color2 = (237, 161, 251, 255)  # Bottom Color

    gradient_surface = pygame.Surface((left_graph_rect.width, left_graph_rect.height), pygame.SRCALPHA)
    draw_gradient_rect(gradient_surface, gradient_surface.get_rect(), gradient_color2, gradient_color1)

    window.blit(gradient_surface, left_graph_rect.topleft)
    # pygame.draw.rect(window, (0, 0, 255), left_graph_rect)  # Example: Blue filled rectangle

    # Show popup message
    # show_popup_message("Robot 1 resetting", font, window)

    # Update the display
    pygame.display.flip()

    time.sleep(0.05)

# Release the camera and quit Pygame
camera.release()
pygame.quit()