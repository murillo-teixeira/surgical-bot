import pygame


class Interface:
    def __init__(self):
        pygame.init()
        self.size = (640,480)
        self.window = pygame.display.set_mode((self.size), pygame.RESIZABLE)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

interface = Interface()