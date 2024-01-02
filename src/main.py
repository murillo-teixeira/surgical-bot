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

def main(home = False):
    pygame.init()
    pygame.joystick.init()

    robot_bisturi = RobotBisturi("COM14", home=home, debug=debug)
    robot_camera = RobotCamera("COM17", home=home, debug=debug)

    controller = Controller(0)

    all_buttons_pressed = []

    running = True
    # previous_button_states = []
    menu_button_state = False

    #GUI part
    # set max values for x, y, z
    x_max = 5400
    y_max = 1687
    z_max = 1922
    x_min = 4009
    y_min = -1580
    z_min = -400
    tolerance = 50

    # Set up the Pygame window
    width, height = 900, 600
    window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Robotic surgeon")

    # Load background image
    background_image = pygame.image.load("C:/Users/Murillo/repositories/scorbot/src/assets/background.jpeg")
    background_image = pygame.transform.scale(background_image, (width, height))

    # Set up the camera
    camera = cv2.VideoCapture(2)  # Change the argument to the camera index if using an external camera

    # Set up the clock for controlling the frame rate
    clock = pygame.time.Clock()

    # put here the function that gets the values of x y and z
    x = 0
    y = 0
    z = 0

    time_since_previous_listpv = time.time()
    time_since_previous_print = time.time()
    movement_in_progress = False
    time_between_listpv = 10
    
    speed = 'slow' # TODO

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
                        print("speed change")
                        robot_bisturi.change_speed()
                    if event.button == 0:
                        print("Show camera menu")
                        if menu_button_state:
                            menu_button_state = False
                        else:
                            menu_button_state = True
                    if event.button == 9:
                        robot_bisturi.enable_conection()
                        robot_camera.enable_conection()
                    if event.button == 2:
                        robot_bisturi.move_to_home()
                if event.type == pygame.JOYHATMOTION:
                    if menu_button_state:
                        menu_button_state = False
                        if event.value == (0, 1):
                            print("option 1")
                            robot_camera.move_one_by_one(1)
                        elif event.value == (1, 0):
                            print("option 2")
                            robot_camera.move_one_by_one(2)
                        elif event.value == (0, -1):
                            print("option 3")
                            robot_camera.move_one_by_one(3)
                        else:
                            menu_button_state = True

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

            if time.time() - time_since_previous_listpv > time_between_listpv and not movement_in_progress:
                time_since_previous_listpv = time.time()
                robot_bisturi.get_current_position()
                print(" position!")
            
            if time.time() - time_since_previous_print > 2:
                time_since_previous_print = time.time()
                print(x, y, z)
                if z < z_min + tolerance + 400:
                    print("Z is too low, please move it up")
                if z > z_max - tolerance - 400:
                    print("Z is too high, please move it down")
                if y < y_min + tolerance + 100:
                    print("Y is too low, please move it up")
                if y > y_max - tolerance - 100:
                    print("Y is too high, please move it down")
                if x < x_min + tolerance + 100:
                    print("X is too low, please move it right")
                if x > x_max - tolerance - 100:
                    print("X is too high, please move it left")

            # TODO POPUP
            # print(x, y, z)
            # if z < z_min + tolerance + 400:
            #     print("Z is too low, please move it up")
            # if z > z_max - tolerance - 400:
            #     print("Z is too high, please move it down")
            # if y < y_min + tolerance + 100:
            #     print("Y is too low, please move it up")
            # if y > y_max - tolerance - 100:
            #     print("Y is too high, please move it down")
            # if x < x_min + tolerance + 100:
            #     print("X is too low, please move it right")
            # if x > x_max - tolerance - 100:
            #     print("X is too high, please move it left")
                
            x, y, z = robot_bisturi.get_position_estimate()

            if not menu_button_state:
                movement_in_progress = process_input(axes, buttons, robot_bisturi, robot_camera, x, y, z, x_max, y_max, z_max, x_min, y_min, z_min, tolerance)
            

            all_buttons_pressed.append([time.time(), axes, buttons, hat, menu_button_state])
            
            # arrow head points -> upper point (665, 70) ,  lower point (840, 250)
            x_point = int((int(x) - x_min) * 175 / (x_max - x_min) + 665)
            y_point = int(250 - (int(y) - y_min) * 180 / (y_max - y_min))
            pygame.draw.circle(window, (177, 80, 251), (x_point, y_point), 3)  # circle

            # z
            # bar points -> upper point (760,285), lower point (760, 485)
            z_point = int(485 - (int(z) - z_min) * 200 / (z_max - z_min))
            bar_length = int((int(z) - z_min) * 200 / (z_max - z_min))
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

# Executes main reading the arguments from the terminal
if __name__ == "__main__":
    arguments = sys.argv[1:]

    # only run the main function if there is the home argument
    if len(arguments) > 0 and arguments[0] == "--home":
        home = False if arguments[1] == '0' else True
        main(home=home)
    else:
        main()
