import pygame

def main():
    pygame.init()

    # Screen dimensions
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("RGB Color Blocks")

    # Font for displaying text
    font = pygame.font.SysFont(None, 24)

    # Define the two RGB colors
    rgb_color1 = (1,102,252) # First RGB color 48.1
    rgb_color2 = (210,210,39)  # Second RGB color 198.9

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
        text_surface1 = font.render(f"RGB Color 1: {rgb_color1}", True, (255, 255, 255))
        screen.blit(text_surface1, (10, 10))

        # Render color information text for the second block
        text_surface2 = font.render(f"RGB Color 2: {rgb_color2}", True, (255, 255, 255))
        screen.blit(text_surface2, (screen_width // 2 + 10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
