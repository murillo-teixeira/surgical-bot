import pygame
import sys
import math


def process_input(axes, buttons):
    # Camera positions

    if buttons[0] == 1:
        print("camera position 1")
    elif buttons[1] == 1:
        print("camera position 2")
    elif buttons[2] == 1:
        print("camera position 3")
    elif buttons[3] == 1:
        print("camera position 4")

    # change z axes

    if buttons[4] == 1 and buttons[6] == 0:
        print("decrease bisturi z")
    elif buttons[4] == 0 and buttons[6] == 1:
        print("increase bisturi z")

    # change bisturi x and y

    if axes[0] >= 0.4:
        print("decrease bisturi y by scale -> " + str(axes[0]))
    elif axes[0] <= -0.4:
        print("increase bisturi y by scale -> " + str(-axes[0]))

    if axes[1] >= 0.4:
        print("decrease bisturi x by scale -> " + str(axes[1]))
    elif axes[1] <= -0.4:
        print("increase bisturi x by scale -> " + str(-axes[1]))

    # change the pitch and roll

    if axes[2] >= 0.4:
        print("decrease roll by scale -> " + str(axes[2]))
    elif axes[2] <= -0.4:
        print("increase roll by scale -> " + str(-axes[2]))

    if axes[3] >= 0.4:
        print("decrease pitch by scale -> " + str(axes[3]))
    elif axes[3] <= -0.4:
        print("increase pitch x by scale -> " + str(-axes[3]))



def main():
    # Counter
    count = 0

    # Initialize Pygame
    pygame.init()

    # Initialize the gamepad
    pygame.joystick.init()

    # Check if any joystick/gamepad is connected
    if pygame.joystick.get_count() == 0:
        print("No gamepad found.")
        return

    # Initialize the first gamepad
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Gamepad Name: {joystick.get_name()}")

    try:
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                # Get gamepad input
                axes = [round(joystick.get_axis(i), 3) for i in range(joystick.get_numaxes())]
                buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
                process_input(axes, buttons)

                # Counting
                # count += 1
                # print(count)
                # Process input
                # print(f"Axes: {axes}")
                # print(f"Buttons: {buttons}")


    except KeyboardInterrupt:
        pass

    finally:
        # Clean up
        pygame.quit()


if __name__ == "__main__":
    main()
