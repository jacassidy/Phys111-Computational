"""Produce a static pendulum PNG using theta values from CSV.

This script uses the same helper functions as the pygame visualizer, but
creates a matplotlib figure (headless-friendly) for CI / make consumption.
"""

import argparse
import os

import matplotlib.pyplot as plt

from ComputationalProject.visualizer import load_theta_series, theta_to_positions


def main():
    parser = argparse.ArgumentParser(description="Save a static pendulum visualization from a theta CSV")
    parser.add_argument("csv_file", help="CSV file (Time,Theta,Theta Dot)")
    parser.add_argument("--out", default="figures/pendulum_static.png", help="Output PNG path")
    parser.add_argument("--d", type=float, default=200.0, help="Pendulum rod length in pixels")
    parser.add_argument("--pivot", type=float, nargs=2, default=[300, 300], help="Pivot location X Y")

    args = parser.parse_args()

    theta_values = load_theta_series(args.csv_file)
    pivot = (int(args.pivot[0]), int(args.pivot[1]))
    x, y = theta_to_positions(theta_values, pivot, args.d)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # Plot the trajectory of the bob on a white background
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, "-o", markersize=3, linewidth=1, color="tab:blue")
    plt.title("Pendulum bob trajectory")
    plt.axis("equal")
    plt.gca().invert_yaxis()  # Keep the same coordinate system as the visualizer
    plt.xlabel("x (px)")
    plt.ylabel("y (px)")
    plt.grid(True)
    plt.savefig(args.out, dpi=200, bbox_inches="tight")
    print(f"Saved static pendulum snapshot to {args.out}")


if __name__ == "__main__":
    main()
