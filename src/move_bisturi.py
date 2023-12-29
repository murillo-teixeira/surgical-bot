import sys
import pygame
import time
import numpy as np
from classes.RobotBisturi import RobotBisturi
from classes.RobotCamera import RobotCamera
from classes.Joystick import Controller
from classes.Pose import Pose
import cv2
from helpers.process_input import process_input
from helpers.interface import *

debug = False

pygame.init()
pygame.joystick.init()

robot_bisturi = RobotBisturi("COM14", debug=debug)
# robot_camera = RobotCamera("COM7", home=home)

controller = Controller(0)

running = True
# previous_button_states = []
menu_button_state = False

# put here the function that gets the values of x y and z
x = 0
y = 0
z = 0

time_since_previous_listpv = time.time()
time_since_previous_print = time.time()
movement_in_progress = False
time_between_listpv = 10

while running:
    try:
        axes, buttons, hat = controller.get_input_state()
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                robot_bisturi.close()
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 8:
                    if debug: print("speed change")
                    robot_bisturi.change_speed()
                if event.button == 9:
                    robot_bisturi.enable_conection()
                if event.button == 2:
                    robot_bisturi.move_to_home()
                    # robot_camera.enable_conection()

        if not menu_button_state:
            movement_in_progress = process_input(axes, buttons, robot_bisturi, 'robot_camera')
        
        if time.time() - time_since_previous_listpv > time_between_listpv and not movement_in_progress:
            time_since_previous_listpv = time.time()
            robot_bisturi.get_current_position()
            print(" position!")
        
        if time.time() - time_since_previous_print > 2:
            time_since_previous_print = time.time()
            print(x, y, z)
            
        x, y, z = robot_bisturi.get_position_estimate()

        time.sleep(0.05)

    except Exception as e:
        print("Error", e)


pygame.quit()
