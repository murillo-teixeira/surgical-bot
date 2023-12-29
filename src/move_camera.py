import sys
import pygame
import time
import numpy as np
from classes.RobotCamera import RobotCamera
from classes.Joystick import Controller
from classes.Pose import Pose
import cv2
from helpers.process_input import process_input
from helpers.interface import *

pygame.init()
pygame.joystick.init()

robot_camera = RobotCamera("COM16")

controller = Controller(0)

all_buttons_pressed = []

running = True

menu_button_state = False

print("Everything connected")

while running:
    try:
        axes, buttons, hat = controller.get_input_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                robot_bisturi.close()
                pygame.quit()
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    print("Show camera menu")
                    menu_button_state = True
                if event.button == 9:
                    robot_bisturi.enable_conection()
                    robot_camera.enable_conection()
            if event.type == pygame.JOYHATMOTION:
                if menu_button_state:
                    menu_button_state = False
                    print(event.value)
                    if event.value == (0, 1):
                        print("option 1")
                        robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_1)
                    elif event.value == (1, 0):
                        print("option 2")
                        robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_2)
                    elif event.value == (0, -1):
                        print("option 3")
                        robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_3)
                    else:
                        menu_button_state = True

                    # if event.value == (0, 1):
                    #     print("option 1")

        if not menu_button_state:
            process_input(axes, buttons, "robot_bisturi", robot_camera)
        
        time.sleep(0.05)

    except Exception as e:
        print("Error", e)


pygame.quit()
