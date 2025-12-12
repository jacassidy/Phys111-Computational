import numpy as np
from scipy.integrate import solve_ivp


def pendulum_ode_factory(x0, omega, d=1.0, g=9.81):
    """Return an ODE function f(t, y) that computes the pendulum acceleration.

    The returned function uses outer-scope x0, omega, d, and g to compute the
    second derivative. It's written to be compatible with scipy.integrate.solve_ivp.
    """
    def pendulum_ode(t, y):
        theta = y[0]
        theta_dot = y[1]

        numerator = (
            np.sin(theta) * (g - theta_dot * omega * x0 * np.cos(t))
            + omega * x0 * (omega * np.cos(theta) * np.sin(t) + np.cos(t) * np.sin(theta))
        )
        theta_double_dot = numerator / d
        return [theta_dot, theta_double_dot]

    return pendulum_ode


def compute_pendulum_trajectory(
    x0=1.0,
    omega=2.0,
    theta0=np.pi,
    theta_dot0=2.5,
    d=1.0,
    g=9.81,
    N_periods=10,
    t_start=0.0,
    t_eval=None,
    solver_method="RK45",
    rtol=1e-8,
    atol=1e-8,
):
    """Compute pendulum trajectory using solve_ivp and return (times, theta_values, theta_dot_values).

    If t_eval is None, samples once per 2*pi period similar to earlier scripts.
    """
    y0 = [theta0, theta_dot0]

    if t_eval is None:
        t_end = 2 * np.pi * N_periods
        n_values = np.arange(0, N_periods + 1)
        t_eval = 2 * np.pi * n_values
    else:
        t_end = float(t_eval[-1])

    ode = pendulum_ode_factory(x0=x0, omega=omega, d=d, g=g)

    sol = solve_ivp(
        ode,
        [t_start, t_end],
        y0,
        t_eval=t_eval,
        method=solver_method,
        rtol=rtol,
        atol=atol,
    )

    theta_values = sol.y[0]
    theta_dot_values = sol.y[1]
    times = sol.t

    return times, theta_values, theta_dot_values


def save_trajectory_to_csv(filename, times, theta_values, theta_dot_values, fmt="{:.4f}"):
    """Save theta & theta_dot to a CSV file with header (Time, Theta, Theta_dot).

    This writes values to disk using the given fmt string for formatting numbers.
    """
    import csv

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time", "Theta", "Theta Dot"])
        for t, th, thd in zip(times, theta_values, theta_dot_values):
            writer.writerow([fmt.format(t), fmt.format(th), fmt.format(thd)])


__all__ = ["compute_pendulum_trajectory", "save_trajectory_to_csv"]
