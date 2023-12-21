import pygame
import numpy as np


width, height = 900, 600
# background_image = pygame.image.load("C:/Users/fatim/Desktop/IST/Robotics/scorbot/src/assets/background.jpeg")  # Replace "background.jpg" with your image file
# background_image = pygame.transform.scale(background_image, (width, height))

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


# Function to show a popup message with a waiting animation
def show_popup_message(message, font, window):
    popup_surface = pygame.Surface((200, 100), pygame.SRCALPHA)
    popup_rect = popup_surface.get_rect(center=(width // 2, height // 2))

    # Draw the popup background
    pygame.draw.rect(popup_surface, (255, 255, 255, 200), popup_rect)

    # Draw the message
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(popup_rect.width // 2, popup_rect.height // 2 - 10))
    popup_surface.blit(text, text_rect)

    # Draw a waiting animation (e.g., rotating line)
    angle = 0
    count = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.line(popup_surface, (0, 0, 0), (popup_rect.width // 2, popup_rect.height - 20),
                         (popup_rect.width // 2 + int(20 * np.cos(angle)),
                          popup_rect.height - 20 + int(20 * np.sin(angle))), 2)

        angle += 0.1
        count += 0.1
        if count >= 6.3:
            print("cheguei")
            angle = 0
            count = 0
            # Clear the surface to remove the popup
            popup_surface.fill((0, 0, 0, 0))
            window.blit(background_image, (0, 0))
            popup_surface.blit(text, text_rect)

        window.blit(background_image, (0, 0))
        window.blit(popup_surface, popup_rect.topleft)
        pygame.display.flip()

        clock.tick(30)
