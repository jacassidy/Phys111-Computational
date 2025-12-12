import pygame
import csv
import numpy as np

# Parameters
csv_file = 'theta_theta_dot.csv'  # Input CSV file
gif_duration = 20  # Duration of the animation in seconds
d = 200  # Length of the pendulum rod in pixels
x0 = 300  # Length of the horizontal grey line in pixels
screen_size = (800, 600)  # Screen resolution
fps = 100  # Frames per second for the animation

# Colors
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
BLUE = (50, 50, 200)

# Read the CSV file
times = []
theta_values = []

with open(csv_file, mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header
    for row in reader:
        theta_values.append(float(row[0]))

# Calculate frame rate and total frames
total_frames = len(theta_values)
frame_rate = total_frames / gif_duration
frame_step = max(1, int(frame_rate / fps))  # Step to match desired FPS

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Pendulum Visualization")
clock = pygame.time.Clock()

# Pendulum pivot point (moved to the middle of the screen)
pivot_x = screen_size[0] // 2
pivot_y = screen_size[1] // 2

# Correct pendulum positions (theta = 0 is straight up)
x_positions = [pivot_x + d * np.sin(theta) for theta in theta_values]
y_positions = [pivot_y - d * np.cos(theta) for theta in theta_values]  # Subtract because y increases downwards

# Animation loop
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grey horizontal line
    pygame.draw.line(screen, LIGHT_GREY, (pivot_x - x0, pivot_y), (pivot_x + x0, pivot_y), 2)

    # Draw the pendulum rod
    pendulum_x = x_positions[frame]
    pendulum_y = y_positions[frame]
    pygame.draw.line(screen, BLUE, (pivot_x, pivot_y), (pendulum_x, pendulum_y), 4)

    # Draw the pendulum bob
    pygame.draw.circle(screen, BLUE, (int(pendulum_x), int(pendulum_y)), 10)

    # Update the frame
    pygame.display.flip()

    # Advance the frame with the desired step
    frame += frame_step
    if frame >= len(x_positions):
        running = False
        frame = 0  # Loop the animation

    # Cap the frame rate
    clock.tick(fps)

pygame.quit()
