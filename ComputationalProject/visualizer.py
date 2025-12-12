"""Visualizer for pendulum theta values saved to CSV.

This module provides utility functions to convert theta series to screen
positions (which makes it testable), plus a small pygame-based animation
launcher that runs only when executed as a script.
"""

import csv
from typing import Sequence, Tuple

import numpy as np


def load_theta_series(csv_file: str) -> np.ndarray:
    """Load theta values from a CSV created by the integrator.

    Expects header (Time, Theta, Theta Dot) and returns a 1D numpy array of theta values.
    """
    theta_values = []
    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header
        for row in reader:
            # CSV format: Time, Theta, Theta Dot
            theta_values.append(float(row[1]))
    return np.array(theta_values)


def theta_to_positions(theta_values: Sequence[float], pivot: Tuple[int, int], d: float) -> Tuple[np.ndarray, np.ndarray]:
    """Convert theta values (radians, theta=0 up) to screen x,y positions.

    Returns two numpy arrays (x_positions, y_positions).
    """
    pivot_x, pivot_y = pivot
    theta_arr = np.asarray(theta_values)
    x_positions = pivot_x + d * np.sin(theta_arr)
    y_positions = pivot_y - d * np.cos(theta_arr)
    return x_positions, y_positions


if __name__ == "__main__":
    # Minimal pygame-based launcher kept behind __main__ so importing this
    # module remains side-effect free and testable.
    import pygame
    import argparse

    parser = argparse.ArgumentParser(description="Animate pendulum theta series from CSV")
    parser.add_argument("csv_file", help="CSV file (Time,Theta,Theta Dot)")
    parser.add_argument("--duration", type=float, default=20.0, help="Total duration of animation in seconds")
    parser.add_argument("--d", type=float, default=200.0, help="Pendulum rod length in pixels")
    parser.add_argument("--x0", type=int, default=300, help="Half-width of horizontal guide line in pixels")
    parser.add_argument("--screen", type=int, nargs=2, default=[800, 600], help="Screen size W H")
    parser.add_argument("--fps", type=int, default=60, help="Target frame rate")

    args = parser.parse_args()

    theta_values = load_theta_series(args.csv_file)
    total_frames = len(theta_values)
    frame_rate = max(1, int(total_frames / args.duration))
    frame_step = max(1, frame_rate // args.fps)

    pygame.init()
    screen = pygame.display.set_mode(tuple(args.screen))
    pygame.display.set_caption("Pendulum Visualization")
    clock = pygame.time.Clock()

    pivot = (args.screen[0] // 2, args.screen[1] // 2)
    x_positions, y_positions = theta_to_positions(theta_values, pivot, args.d)

    WHITE = (255, 255, 255)
    LIGHT_GREY = (200, 200, 200)
    BLUE = (50, 50, 200)

    running = True
    frame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        pygame.draw.line(screen, LIGHT_GREY, (pivot[0] - args.x0, pivot[1]), (pivot[0] + args.x0, pivot[1]), 2)

        pendulum_x = x_positions[frame]
        pendulum_y = y_positions[frame]
        pygame.draw.line(screen, BLUE, pivot, (pendulum_x, pendulum_y), 4)
        pygame.draw.circle(screen, BLUE, (int(pendulum_x), int(pendulum_y)), 10)

        pygame.display.flip()

        frame += frame_step
        if frame >= len(x_positions):
            running = False
            frame = 0

        clock.tick(args.fps)

    pygame.quit()
