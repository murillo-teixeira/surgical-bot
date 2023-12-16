import pygame
import time
import numpy as np
from classes.Robot import Robot
from classes.Joystick import Controller
from classes.Pose import Pose
import cv2
from helpers.process_input import process_input
from helpers.interface import *


pygame.init()
pygame.joystick.init()

robot_bisturi = Robot("COM11")
robot_camera = Robot("COM9")

controller = Controller(0)

all_buttons_pressed = []

running = True
# previous_button_states = []
menu_button_state = False

#GUI part
# set max values for x, y, z
x_max = 7
y_max = 7
z_max = 5

# Set up the Pygame window
width, height = 900, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robotis GUI")

# Load background image
background_image = pygame.image.load("C:/Users/fatim/Desktop/IST/Robotics/scorbot/src/assets/background.jpeg")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (width, height))


# Set up the camera
camera = cv2.VideoCapture(1)  # Change the argument to the camera index if using an external camera

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()


# put here the function that gets the values of x y and z
x = 0
y = 0
z = 0

while running:
    try:
        axes, buttons, hat = controller.get_input_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # robot_bisturi.close()
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 8:
                    print("speed change")
                    # robot_bisturi.change_speed()
                if event.button == 0:
                    print("Show camera menu")
                    menu_button_state = True
            if event.type == pygame.JOYHATMOTION:
                if menu_button_state:
                    print(event.value)
                    if event.value == (0, 1):
                        print("option 1")
                        robot_bisturi.move_one_by_one(robot_bisturi.ROBOT_OPTION_1)
                    if event.value == (1, 0):
                        print("option 2")
                        robot_bisturi.move_one_by_one(robot_bisturi.ROBOT_OPTION_1)
                    if event.value == (0, -1):
                        print("option 3")
                        robot_bisturi.move_one_by_one(robot_bisturi.ROBOT_OPTION_3)
                    # if event.value == (0, 1):
                    #     print("option 1")
                    menu_button_state = False


        time.sleep(0.05)
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


        if not menu_button_state:
            a, b, c = process_input(axes, buttons, robot_bisturi, robot_camera)#, which_robot, robot_camera)
            # a, b, c = 0, 0, 0
            x +=a
            y+=b
            z+=c
        all_buttons_pressed.append([time.time(), axes, buttons, hat, menu_button_state])
        
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

        pygame.display.flip()

        time.sleep(0.05)

    except Exception as e:
        print("Error", e)


camera.release()
pygame.quit()

print("Logging...")
with open(f"logs/{str(time.time())}.txt", "w") as txt_file:
    for line in all_buttons_pressed:
        txt_file.write(str(line) + "\n") 