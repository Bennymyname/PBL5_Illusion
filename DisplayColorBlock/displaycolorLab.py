import pygame
import numpy as np
import cv2


def lab_to_rgb(lab_color):
    """Convert a CIElab color to RGB color space using OpenCV."""
    lab_color = np.array(lab_color, dtype=np.float32).reshape(1, 1, 3)
    rgb_color = cv2.cvtColor(lab_color, cv2.COLOR_Lab2RGB).reshape(3)
    return tuple(np.clip(rgb_color * 255, 0, 255).astype(np.uint8))


def main():
    pygame.init()

    # Screen dimensions
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Lab Color Blocks")

    # Font for displaying text
    font = pygame.font.SysFont(None, 24)

    # Define the two Lab colors
    # lab_color1 = (74.80381911122772, 79.2, -107.86)   # First Lab color
    # lab_color2 = (80.93390115563685, 80, 67)  # Second Lab color

    lab_color1 = (58.39157246, 79.2, -107.86)
    lab_color2 = (96.9211721, 79.2, -107.86)

    # Convert Lab colors to RGB
    rgb_color1 = lab_to_rgb(lab_color1)
    rgb_color2 = lab_to_rgb(lab_color2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the two rectangles with the specified colors
        pygame.draw.rect(screen, rgb_color1, (0, 0, screen_width // 2, screen_height))
        pygame.draw.rect(screen, rgb_color2, (screen_width // 2, 0, screen_width // 2, screen_height))

        # Render color information text for the first block
        text_surface1 = font.render(f"Lab Color 1: {lab_color1} - RGB: {rgb_color1}", True, (255, 255, 255))
        screen.blit(text_surface1, (10, 10))

        # Render color information text for the second block
        text_surface2 = font.render(f"Lab Color 2: {lab_color2} - RGB: {rgb_color2}", True, (255, 255, 255))
        screen.blit(text_surface2, (screen_width // 2 + 10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
