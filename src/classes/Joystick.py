import pygame

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