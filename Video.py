import pygame
import pygame.camera

pygame.init() # will be done in Main
pygame.camera.init()

class Video:
    def __init__(self):

        pygame.camera.init()
        self.size = (640,480) # parameter to the class?
        
        # Create a dsiplay surface
        self.display = pygame.display.set_mode(self.size, 0)


        # Look for all the camera available
        self.camera_list = pygame.camera.list_cameras()

        if not self.camera_list:
            raise ValueError("No cameras detected")
        
        # Print the available camera indices
        print("Available cameras:", self.camera_list)

        
        #Initialize the first camera
        self.camera = pygame.camera.Camera(self.camera_list[0], self.size, "RGB")
        self.camera.start()
        self.screen = pygame.surface.Surface(self.size, 0 , self.display)


        capture = True

        while capture:
            self.screen = self.camera.get_image(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.camera.stop()
                    capture = False
            



video = Video()