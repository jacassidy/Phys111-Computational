import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
g = 9.81  # acceleration due to gravity (m/s^2)
L = 1.0   # length of the pendulum (m)

# System of equations
def system(t, y):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = np.sin(t) - (g / L) * np.sin(theta)
    return [dtheta_dt, domega_dt]

# Time span
t_start = 0
t_end = 10
t_eval = np.linspace(t_start, t_end, 1000)

# Initial conditions to explore
initial_conditions = [
    [0.0, 0.0],
    [0.1, 0.0],
    [0.0, 0.1],
    [0.2, -0.1],
    [np.pi / 4, 0.0],
]

# Plotting
plt.figure(figsize=(12, 8))

for y0 in initial_conditions:
    sol = solve_ivp(system, [t_start, t_end], y0, t_eval=t_eval)
    theta = sol.y[0]
    plt.plot(sol.t, theta, label=f"θ₀={y0[0]}, ω₀={y0[1]}")

plt.title("Dynamics of the System for Various Initial Conditions")
plt.xlabel("Time (s)")
plt.ylabel("θ (radians)")
plt.legend()
plt.grid(True)
import os

figdir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(figdir, exist_ok=True)
figpath = os.path.join(figdir, "Pset6a.png")
plt.savefig(figpath, dpi=200, bbox_inches='tight')
print(f"Saved figure to {figpath}")
plt.close()
