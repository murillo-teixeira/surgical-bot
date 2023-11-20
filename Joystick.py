import pygame

class Controller:
    def __init__(self) -> None:
        pygame.init()
        # Initialize the gamepad
        pygame.joystick.init()
        # Check if any joystick/gamepad is connected
        if pygame.joystick.get_count() == 0:
            print("No gamepad found.")
            return
        
        # Initialize the first gamepad
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

        print(f"Gamepad Name: {self.joystick.get_name()}")

class Joystick:
    def __init__(self) -> None:
        Controller.__init__()
    