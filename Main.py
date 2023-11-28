from Robot import Robot
from Interface import Interface
from Joystick import Controller
import pygame

# Initialize the pygame
pygame.init()

# Initialize robot 
PORT_CAMERA = "COM5"
PORT_SCALPEL = "COM4"
robot_camera = Robot(PORT_CAMERA)
robot_scalpel = Robot(PORT_SCALPEL)

is_camera = False

# Initialize controller
controller = Controller()

# Initialize interface
WINDOW_SIZE = (640,480)
window = pygame.display.set_mode((WINDOW_SIZE), pygame.RESIZABLE)



running = True

while running:
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
            if event.button == 2:
                # TODO Open camera menu function
                controller.cameraMenu()
            if event.button == 3:
                # TODO Open other manipulator menu
                controller.manipulatorMenu()
            if event.button == 4:
                # Decrease z coordinate
                if is_camera:
                    robot_camera.move_robot_z(-100)
                else:
                    robot_scalpel.move_robot_z(-100)
            if event.button == 5:
                # Increase value of z
                if is_camera:
                    robot_camera.move_robot_z(100)
                else:
                    robot_scalpel.move_robot_z(100)
            if event.button == 7:
                # Change manipulator control
                is_camera = not is_camera
        
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0: # 0 and 1 are axis for left joystick
                # change y value
                if is_camera:
                    robot_camera.move_robot_y(event.value*100)
                else:
                    robot_scalpel.move_robot_y(event.value*100)
            elif event.axis == 1:
                if is_camera:
                    robot_camera.move_robot_x(event.value*100)
                else:
                    robot_scalpel.move_robot_x(event.value*100)
            elif event.axis == 2:
                if is_camera:
                    robot_camera.move_robot_pitch(event.value*100)
                else:
                    robot_scalpel.move_robot_pitch(event.value*100)
            elif event.axis == 3 :
                if is_camera:
                    robot_camera.move_robot_roll(event.value*100)
                else:
                    robot_scalpel.move_robot_roll(event.value*100)
