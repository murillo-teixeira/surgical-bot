import pygame
import time
from classes.Robot import Robot
from classes.Joystick import Controller
from classes.Pose import Pose

from helpers.process_input import process_input


pygame.init()
pygame.joystick.init()

robot_bisturi = Robot("COM4")
# robot_camera = Robot("COM4")

controller = Controller(0)


running = True
# previous_button_states = []
menu_button_state = False

while running:
    
    axes, buttons, hat = controller.get_input_state()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # robot_bisturi.close()
            pygame.quit()
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 8:
                print("speed change")
                robot_bisturi.change_speed()
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


    # print(axes, buttons, hat)
    if not menu_button_state:
        process_input(axes, buttons, robot_bisturi, "robot_camera")

    time.sleep(0.05)