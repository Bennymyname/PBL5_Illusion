import pandas as pd
import pygame
import numpy as np
import cv2
import csv
import os
import random
from scipy.interpolate import interp1d

# Corrected data dictionary with all lists of the same length
data = {
    # R
    'R1': [91, 102, 115, 130, 145, 161, 177, 193, 209, 226, 243, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    'G1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 48, 68, 85, 102, 118, 133, 148, 163, 179],
    'B1': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 23, 37, 50, 63, 76, 89, 102, 115, 128],
    'L1*': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'a1*': [80] * 21,
    'b1*': [67] * 21,
    'MeasuredL1': [4.02, 5.3, 7.29, 9.9, 13.15, 17.3, 22.78, 28.8, 36.52, 45.22, 55.38, 63.95, 64.34, 67.75, 72.67,
                   80.61, 89.38, 101.9, 115.71, 132.07, 153.06],

    # G
    'R2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 33, 65, 89],
    'G2': [36, 42, 47, 55, 66, 78, 91, 104, 118, 132, 146, 160, 174, 188, 202, 217, 232, 246, 255, 255, 255],
    'B2': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 47, 66],
    'L2*': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'a2*': [-86.18] * 21,
    'b2*': [83.18] * 21,
    'MeasuredL2': [1.86, 2.46, 3.14, 4.37, 6.9, 10.12, 14.88, 21.21, 29.58, 39.37, 51.97, 67.14, 85.89, 106.16, 128.92,
                   159, 191.08, 226.12, 239.34, 241.59, 243.81],

    # B
    'R3': [0, 0, 0, 0, 0, 0, 0, 37, 68, 92, 112, 131, 149, 166, 183, 200, 217, 233, 250, 255, 255],
    'G3': [0, 0, 0, 0, 0, 0, 0, 15, 34, 50, 64, 78, 92, 106, 120, 134, 147, 161, 176, 190, 204],
    'B3': [161, 175, 189, 204, 218, 233, 248, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255],
    'L3*': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'a3*': [79.2] * 21,
    'b3*': [-107.86] * 21,
    'MeasuredL3': [7.12, 8.89, 10.98, 13.63, 16.55, 20.1, 24, 25.02, 26.31, 29.71, 34.52, 41.4, 51.13, 61.46, 76.01,
                   92.36, 111.64, 135.78, 165.07, 189.69, 213.92],

    # Yellow
    'R4': [33, 40, 45, 47, 51, 57, 66, 76, 88, 100, 113, 127, 142, 156, 171, 186, 202, 217, 232, 248, 255],
    'G4': [7, 21, 31, 42, 53, 65, 77, 89, 101, 114, 126, 139, 152, 165, 179, 192, 206, 220, 234, 248, 255],
    'B4': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 27],
    'L4*': [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
    'a4*': [-21.56] * 21,
    'b4*': [94.48] * 21,
    'MeasuredL4': [0.66, 1.32, 2.05, 3.3, 5.03, 7.81, 11.86, 16.95, 23.24, 32.2, 41.9, 55.3, 70.28, 88.81, 111.59,
                   135.5, 166.46, 200.69, 238.73, 283.59, 300.31],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define the interpolation functions
f1 = interp1d(df['MeasuredL1'], df['L1*'], fill_value="extrapolate")
f2 = interp1d(df['MeasuredL2'], df['L2*'], fill_value="extrapolate")
f3 = interp1d(df['MeasuredL3'], df['L3*'], fill_value="extrapolate")
f4 = interp1d(df['MeasuredL4'], df['L4*'], fill_value="extrapolate")

def get_l_values(measured_luminance):
    L1_star = f1(measured_luminance)
    L2_star = f2(measured_luminance)
    L3_star = f3(measured_luminance)
    L4_star = f4(measured_luminance)
    return L1_star, L2_star, L3_star, L4_star

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
    colorsresult_csv = 'color_fixeddifference2.csv'
    with open('%s' % colorsresult_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([])

def write_to_csv(lab_color1, lab_color2, rgb1, rgb2, luminance_g1, luminance_g2, angular_velocity):
    """Write data to a CSV file."""
    file_exists = os.path.isfile('color_fixeddifference2.csv')
    with open('color_fixeddifference2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ['L value (g1)', 'Actual Luminance (g1)', 'RGB (g1)', 'Lab (g1)',
                 'L value (g2)', 'Actual Luminance (g2)', 'RGB (g2)', 'Lab (g2)', 'Final Angular Velocity'])

        # Convert the Lab values from numpy arrays to plain floats
        lab_color1 = (float(lab_color1[0]), lab_color1[1], lab_color1[2])
        lab_color2 = (float(lab_color2[0]), lab_color2[1], lab_color2[2])

        writer.writerow([lab_color1[0], luminance_g1, rgb1, lab_color1,
                         lab_color2[0], luminance_g2, rgb2, lab_color2,
                         format(angular_velocity, '.3f')])

def select_luminance_and_colors():
    # Step 1: Fixed luminance values
    luminance_g1 = 48
    luminance_g2 = 199

    # Step 2: Randomly pick colors for g1 and g2
    available_colors_g1 = ['color1', 'color2', 'color3', 'color4']
    available_colors_g2 = ['color2', 'color3', 'color4']

    chosen_color_g1 = random.choice(available_colors_g1)
    chosen_color_g2 = random.choice(available_colors_g2)

    # Step 3: Find their L* value, and corresponding a*, b* values
    def get_lab_values(chosen_color, luminance):
        if chosen_color == 'color1':
            L_star = f1(luminance)
            a_star = random.choice(df['a1*'])
            b_star = random.choice(df['b1*'])
        elif chosen_color == 'color2':
            L_star = f2(luminance)
            a_star = random.choice(df['a2*'])
            b_star = random.choice(df['b2*'])
        elif chosen_color == 'color3':
            L_star = f3(luminance)
            a_star = random.choice(df['a3*'])
            b_star = random.choice(df['b3*'])
        elif chosen_color == 'color4':
            L_star = f4(luminance)
            a_star = random.choice(df['a4*'])
            b_star = random.choice(df['b4*'])
        return (L_star, a_star, b_star)

    lab_color1 = get_lab_values(chosen_color_g1, luminance_g1)
    lab_color2 = get_lab_values(chosen_color_g2, luminance_g2)

    return lab_color1, lab_color2, luminance_g1, luminance_g2

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

    lab_color1, lab_color2, luminance_g1, luminance_g2 = select_luminance_and_colors()

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
                print("Color of g1 and g2 in CIELab space:")
                print("g1_lab:", lab_color1)
                print("g2_lab:", lab_color2)
                print("Final angular velocity:", format(angular_velocity, '.3f'), "degrees/second")
                write_blank_line_to_csv()
                write_to_csv(lab_color1, lab_color2, g1, g2, luminance_g1, luminance_g2, angular_velocity)
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
                    write_to_csv(lab_color1, lab_color2, g1, g2, luminance_g1, luminance_g2, angular_velocity)
                    write_blank_line_to_csv()

                    print("-----------------------------------")

                    # Generate new angular velocity
                    angular_velocity = random.choice(
                        [i * 0.1 for i in range(5, 21)] + [i * 0.1 for i in range(-20, -5)])
                    print("Initial angular velocity:", format(angular_velocity, '.3f'), "degrees/second")
                    # Select new luminance and colors
                    lab_color1, lab_color2, luminance_g1, luminance_g2 = select_luminance_and_colors()
                    g1 = lab_to_rgb(lab_color1)
                    g2 = lab_to_rgb(lab_color2)

                    # Redraw static patterns and special circle with the new colors
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

