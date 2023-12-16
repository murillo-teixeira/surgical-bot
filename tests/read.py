import pygame
import time
from src.helpers.process_input import process_input

pygame.init()
pygame.joystick.init()



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
        self.hat = [self.joystick.get_hat(i) for i in range(self.joystick.get_numhats())]

        return self.axes, self.buttons, self.hat
    
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
                # robot_bisturi.change_speed()
            if event.button == 0:
                print("Show camera menu")
                menu_button_state = True
        if event.type == pygame.JOYHATMOTION:
            if menu_button_state:
                print(event.value)
                if event.value == (0, 1):
                    print("option 1")
                    # robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_1)
                if event.value == (1, 0):
                    print("option 2")
                    # robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_1)
                if event.value == (0, -1):
                    print("option 3")
                    # robot_camera.move_one_by_one(robot_camera.ROBOT_OPTION_3)
                # if event.value == (0, 1):
                #     print("option 1")
                menu_button_state = False

    if not menu_button_state:
        a, b, c = process_input(axes, buttons, "robot_bisturi", "S")#, which_robot, robot_camera)

    time.sleep(0.05)