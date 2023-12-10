import pygame
import cv2
import numpy as np


# Function to create a gradient-filled rectangle
def draw_gradient_rect(surface, rect, color1, color2):
    color1 = pygame.Color(*color1)
    color2 = pygame.Color(*color2)

    for y in range(200):
        if y >= rect.height:
            break
        t = y / 200
        color = pygame.Color(
            int((1 - t) * color1.r + t * color2.r),
            int((1 - t) * color1.g + t * color2.g),
            int((1 - t) * color1.b + t * color2.b),
            int((1 - t) * color1.a + t * color2.a)
        )
        pygame.draw.line(surface, color, (rect.x, rect.y + rect.height - y), (rect.x + rect.width, rect.y + rect.height - y))


# set max values for x, y, z
x_max = 7
y_max = 7
z_max = 5

# Initialize Pygame
pygame.init()

# Set up the Pygame window
width, height = 900, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Robotis GUI")

# Load background image
background_image = pygame.image.load(r"C:\Users\fatim\Desktop\IST\Robotics\scorbot\Camera&Interface\background.jpeg")  # Replace "background.jpg" with your image file
background_image = pygame.transform.scale(background_image, (width, height))


# Set up the camera
camera = cv2.VideoCapture(1)  # Change the argument to the camera index if using an external camera

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background image
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

    # put here the function that gets the values of x y and z
    x = 2
    y = 3
    z = 2

    # x and y axes
    # arrow head points -> upper point (665, 70) ,  lower point (840, 250)
    x_point = int(x*175/x_max + 665)
    y_point = int(250 - y*180/y_max)
    pygame.draw.circle(window, (177, 80, 251), (x_point, y_point), 3)  # circle


    # z
    # bar points -> upper point (760,285), lower point (760, 485)
    z_point = int(485 - z*200/z_max)
    bar_length = int(z*200/z_max)
    left_graph_rect = pygame.Rect(760-10, z_point, 20, bar_length)

    gradient_color1 = (104, 239, 243, 255)  # Top color
    gradient_color2 = (237, 161, 251, 255)  # Bottom Color

    gradient_surface = pygame.Surface((left_graph_rect.width, left_graph_rect.height), pygame.SRCALPHA)
    draw_gradient_rect(gradient_surface, gradient_surface.get_rect(), gradient_color2, gradient_color1)

    window.blit(gradient_surface, left_graph_rect.topleft)
    # pygame.draw.rect(window, (0, 0, 255), left_graph_rect)  # Example: Blue filled rectangle


    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)  # Adjust the frame rate as needed

# Release the camera and quit Pygame
camera.release()
pygame.quit()