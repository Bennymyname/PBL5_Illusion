import pandas as pd
import pygame
import numpy as np
import cv2
import csv
import os
import random

def lab_to_rgb(lab_color):
    """Convert a CIElab color to RGB color space using OpenCV."""
    lab_color = np.array(lab_color, dtype=np.float32).reshape(1, 1, 3)
    rgb_color = cv2.cvtColor(lab_color, cv2.COLOR_Lab2RGB).reshape(3)
    return tuple(np.clip(rgb_color * 255, 0, 255).astype(np.uint8))

def precompute_ring_widths(r_max, decay_factor, num_rs=8):
    ring_widths = []
    total_width = 0
    r = r_max
    for _ in range(num_rs):
        dr = r * (1 - decay_factor)
        ring_widths.append(dr)
        total_width += dr
        r *= decay_factor
    ring_widths = [rw * (r_max / total_width) for rw in ring_widths]
    return ring_widths

def draw_pattern(screen, xc, yc, r_max, vals_t, decay_factor, rotation_angle=0, ring_widths=None):
    num_ts = 96
    num_rs = 8
    num_vals = len(vals_t)

    if ring_widths is None:
        ring_widths = precompute_ring_widths(r_max, decay_factor, num_rs)

    r = r_max
    for r_idx, dr in enumerate(ring_widths):
        t_val_pos = r_idx % num_vals

        for t_idx in range(num_ts):
            theta1 = t_idx * 2 * np.pi / num_ts + rotation_angle
            theta2 = (t_idx + 1) * 2 * np.pi / num_ts + rotation_angle

            points = [
                (xc + r * np.cos(theta1), yc + r * np.sin(theta1)),
                (xc + (r - dr) * np.cos(theta1), yc + (r - dr) * np.sin(theta1)),
                (xc + (r - dr) * np.cos(theta2), yc + (r - dr) * np.sin(theta2)),
                (xc + r * np.cos(theta2), yc + r * np.sin(theta2))
            ]

            color_val = tuple(int(v) for v in vals_t[t_val_pos])
            pygame.draw.polygon(screen, color_val, points)

            t_val_pos = (t_val_pos + 1) % num_vals

        r -= dr

def write_blank_line_to_csv():
    """Write a blank line to the CSV file."""
    with open('gray_fixeddifference2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])

def write_to_csv(lab_color1, lab_color2, rgb1, rgb2, angular_velocity):
    """Write data to a CSV file."""
    file_exists = os.path.isfile('gray_fixeddifference2.csv')
    with open('gray_fixeddifference2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ['Lab (g1)', 'RGB (g1)', 'Actual Luminance (g1)',
                 'Lab (g2)', 'RGB (g2)', 'Actual Luminance (g2)', 'Final Angular Velocity'])

        # Convert the Lab values from numpy arrays to plain floats
        lab_color1 = (float(lab_color1[0]), lab_color1[1], lab_color1[2])
        lab_color2 = (float(lab_color2[0]), lab_color2[1], lab_color2[2])

        writer.writerow([lab_color1, rgb1, 48, lab_color2, rgb2, 199, format(angular_velocity, '.3f')])


def main():
    pygame.init()

    # Original dimensions
    original_r_max = 180
    original_width = 1080 + 180 + 180
    original_height = 1080

    # Get the screen resolution
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h

    # Calculate the scaling factor to fit the original dimensions within the screen
    scale_factor = min(screen_width / original_width, screen_height / original_height)

    # Scale the original dimensions
    r_max = int(original_r_max * scale_factor)
    width = int(original_width * scale_factor)
    height = int(original_height * scale_factor)

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    decay_factor = 0.8
    rotation_angle = 0
    angular_velocity = random.choice([i * 0.1 for i in range(5, 21)] + [i * 0.1 for i in range(-20, -5)])  # Random initial angular velocity between 0.5 and 2 degrees per second
    angular_velocity_increment = 0.1  # Degrees per second increment
    print("Initial angular velocity:", angular_velocity, "degrees/second")

    # Fixed colors in Lab space
    lab_color1 = (52, 0, 0)
    lab_color2 = (83, 0, 0)

    # Convert CIELab colors to RGB
    g1 = lab_to_rgb(lab_color1)
    g2 = lab_to_rgb(lab_color2)

    print("g1_lab:", lab_color1)
    print("g1:", g1)
    print("g2_lab:", lab_color2)
    print("g2:", g2)
    print("Initial angular velocity:", format(angular_velocity, '.3f'), "degrees/second")

    color1 = (0, 0, 0)
    color2 = (255, 255, 255)

    is_clockwise = True

    # Precompute ring widths
    ring_widths = precompute_ring_widths(r_max, decay_factor)

    def draw_static_patterns():
        static_surface = pygame.Surface((width, height))
        static_surface.fill((128, 128, 128))

        for yc in range(r_max, height, 2 * r_max):
            for xc in range(r_max, width, 2 * r_max):
                if xc == 4 * r_max and yc == height - 2 * r_max:
                    continue
                if is_clockwise:
                    vals_t = [color1, g1, g2, color2, g2, g1]
                else:
                    vals_t = [color2, g2, g1, color1, g1, g2]
                draw_pattern(static_surface, xc, yc, r_max, vals_t, decay_factor, 0, ring_widths)

        for yc in range(2 * r_max, height, 2 * r_max):
            for xc in range(2 * r_max, width, 2 * r_max):
                if xc == 4 * r_max and yc == height - 2 * r_max:
                    continue
                if is_clockwise:
                    vals_t = [color1, g1, g2, color2, g2, g1]
                else:
                    vals_t = [color2, g2, g1, color1, g1, g2]
                draw_pattern(static_surface, xc, yc, r_max, vals_t, decay_factor, 0, ring_widths)

        return static_surface

    static_surface = draw_static_patterns()

    # Create an off-screen surface for the special circle
    special_surface = pygame.Surface((2 * r_max, 2 * r_max), pygame.SRCALPHA)
    special_surface = special_surface.convert_alpha()

    middle_bottom_x = r_max
    middle_bottom_y = r_max

    if is_clockwise:
        vals_t = [color1, g1, color2, g2]
    else:
        vals_t = [g2, color2, g1, color1]

    draw_pattern(special_surface, middle_bottom_x, middle_bottom_y, r_max, vals_t, decay_factor, 0, ring_widths)

    running = True


    while running:
        dt = clock.tick(60) / 1000  # Delta time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                write_blank_line_to_csv()
                print("Color of g1 and g2 in CIELab space:")
                print("g1_lab:", lab_color1)
                print("g2_lab:", lab_color2)
                print("Final angular velocity:", format(angular_velocity, '.3f'), "degrees/second")
                write_to_csv(lab_color1, lab_color2, g1, g2, angular_velocity)
                # write a blank line in csv
                write_blank_line_to_csv()

                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angular_velocity += angular_velocity_increment
                elif event.key == pygame.K_RIGHT:
                    angular_velocity -= angular_velocity_increment
                elif event.key == pygame.K_SPACE:
                    print("Color of g1 and g2 in CIELab space:")
                    print("g1_lab:", lab_color1)
                    print("g2_lab:", lab_color2)
                    print("Final angular velocity:", format(angular_velocity, '.3f'), "degrees/second")
                    write_blank_line_to_csv()
                    write_to_csv(lab_color1, lab_color2, g1, g2, angular_velocity)
                    print("-----------------------------------")

                    # Generate new angular velocity
                    angular_velocity = random.choice(
                        [i * 0.1 for i in range(5, 21)] + [i * 0.1 for i in range(-20, -5)])
                    print("Initial angular velocity:", format(angular_velocity, '.3f'), "degrees/second")

                    # Redraw static patterns and special circle with the fixed colors
                    static_surface = draw_static_patterns()
                    special_surface.fill((0, 0, 0, 0))  # Clear the surface
                    if is_clockwise:
                        vals_t = [color1, g1, color2, g2]
                    else:
                        vals_t = [g2, color2, g1, color1]
                    draw_pattern(special_surface, middle_bottom_x, middle_bottom_y, r_max, vals_t, decay_factor, 0, ring_widths)

        # Update the rotation angle based on angular velocity and delta time
        rotation_angle += angular_velocity * dt

        screen.blit(static_surface, (0, 0))

        rotated_special_surface = pygame.transform.rotozoom(special_surface, rotation_angle, 1)
        special_rect = rotated_special_surface.get_rect(center=(4 * r_max, height - 2 * r_max))

        screen.blit(rotated_special_surface, special_rect.topleft)

        # Draw small gray circles with alpha transparency
        transparent_gray = (128, 128, 128, 200)
        circle_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for yc in range(r_max, height, 2 * r_max):
            for xc in range(r_max, width, 2 * r_max):
                pygame.draw.circle(circle_surface, transparent_gray, (xc, yc), int(r_max * 0.05))

        for yc in range(2 * r_max, height, 2 * r_max):
            for xc in range(2 * r_max, width, 2 * r_max):
                pygame.draw.circle(circle_surface, transparent_gray, (xc, yc), int(r_max * 0.05))

        screen.blit(circle_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
