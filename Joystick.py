import pygame

class Controller:
    def __init__(self) -> None:
        pygame.init() #DONE IN INTERFACE
        # Initialize the gamepad/controller
        pygame.joystick.init()
        # Check if any joystick/gamepad is connected
        if pygame.joystick.get_count() == 0:
            print("No gamepad found.")
            return
        

        # Initialize the first gamepad
        self.joystick = pygame.joystick.Joystick(0) #only one joystick
        self.joystick.init()

        print(f"Gamepad Name: {self.joystick.get_name()}")

    def eventHandler(self):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.JOYBUTTONDOWN:
                print(event)
                if event.button == 2:
                    # Open camera menu function
                    self.cameraMenu()
                if event.button == 3:
                    # Open other manipulator menu
                    self.manipulatorMenu()
                if event.button == 4:
                    # Decrease z coordinate
                    self.decreaseZ()
                if event.button == 5:
                    # Increase value of z
                    self.increaseZ()
                if event.button == 7:
                    # Change manipulator control
                    self.changeManipulator()
            
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0: # 0 and 1 are axis for left joystick
                    # change y value
                    self.changeX()
                elif event.axis == 1:
                    self.changeY()
                elif event.axis == 2:
                    self.changeRoll()
                elif event.axis == 3 :
                    # change x value
                    self.changePitch()

    def cameraMenu(self):
        print("CameraMenu")

    def manipulatorMenu(self):
        print("ManipulatorMnu")

    def increaseZ(self):
        print("increaseZ")

    def decreaseZ(self):
        print("decreaseZ")

    def changeManipulator(self):
        print("change manipulator")

    def changeY(self):
        print("changey")

    def changeX(self):
        print("changex")
    
    def changeRoll(self):
        print("change Roll")

    def changePitch(self):
        print("change Pitch")

contrl = Controller()

try:
    while True:
        contrl.eventHandler()

except KeyboardInterrupt:
    pass

finally:
    #Clean up
    pygame.quit()