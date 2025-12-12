"""Small CLI to compute a pendulum trajectory and optionally plot/save results.

This script keeps the original behavior but calls into the canonical
`ComputationalProject.integrator.compute_pendulum_trajectory` function so
we don't duplicate numerical logic across scripts.
"""

from ComputationalProject.integrator import compute_pendulum_trajectory, save_trajectory_to_csv
import matplotlib.pyplot as plt
import argparse


def main():
    parser = argparse.ArgumentParser(description="Compute a driven pendulum trajectory and optionally plot/save it.")
    parser.add_argument("--x0", type=float, default=1.0, help="x0 parameter")
    parser.add_argument("--omega", type=float, default=2.0, help="omega driving frequency")
    parser.add_argument("--theta0", type=float, default=3.141592653589793, help="Initial theta")
    parser.add_argument("--theta_dot0", type=float, default=2.5, help="Initial theta dot")
    parser.add_argument("--periods", type=int, default=50, help="Number of 2*pi periods to simulate")
    parser.add_argument("--save", type=str, default="theta_theta_dot.csv", help="CSV filename to write results")
    parser.add_argument("--plot", action="store_true", help="Show a phase-space plot")

    args = parser.parse_args()

    times, theta_values, theta_dot_values = compute_pendulum_trajectory(
        x0=args.x0,
        omega=args.omega,
        theta0=args.theta0,
        theta_dot0=args.theta_dot0,
        N_periods=args.periods,
    )

    save_trajectory_to_csv(args.save, times, theta_values, theta_dot_values)

    print(f"Written {len(times)} points to {args.save}")

    if args.plot:
        plt.figure(figsize=(10, 6))
        plt.scatter(theta_values, theta_dot_values, color="red", s=8)
        plt.title(f"Phase-Space: x0={args.x0}, omega={args.omega}, theta0={args.theta0}, theta_dot0={args.theta_dot0}")
        plt.xlabel("Theta (rad)")
        plt.ylabel("Theta_dot (rad/s)")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    main()
