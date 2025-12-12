import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
g = 9.81  # acceleration due to gravity (m/s^2)
L = 1.0   # length of the pendulum (m)

# System of equations
def system(t, y):
    theta, omega, theta2 = y
    dtheta_dt = omega
    domega_dt = np.sin(theta2) - (g / L) * np.sin(theta)
    dtheta2_dt = 1.0  # theta2 increases linearly with time
    return [dtheta_dt, domega_dt, dtheta2_dt]

# Event function to detect when theta2 crosses multiples of 2*pi
def theta2_event(t, y):
    theta, omega, theta2 = y
    return np.sin(theta2 / 2)
theta2_event.direction = 1  # Detect zero crossings with positive slope
theta2_event.terminal = False  # Continue integration after event is found

# Initial conditions to explore
initial_conditions = [
    [0.0, 0.0, 0.0],
    [0.1, 0.0, 0.0],
    [0.0, 0.1, 0.0],
    [0.2, -0.1, 0.0],
    [np.pi / 4, 0.0, 0.0],
    [0.0, 0.0, 1.0],  # Different theta2 initial condition
]

# Plotting
plt.figure(figsize=(12, 8))

for y0 in initial_conditions:
    t_start = 0
    t_interval = 50 * 2 * np.pi  # Time interval for each integration step
    max_events = 500  # Number of points to collect per initial condition
    total_events = 0
    theta_vals = []
    omega_vals = []
    y_current = y0.copy()
    
    while total_events < max_events:
        t_end = t_start + t_interval
        sol = solve_ivp(
            system, [t_start, t_end], y_current,
            events=theta2_event, dense_output=True
        )
        events = sol.y_events[0]
        
        if events.size > 0:
            theta_vals.extend(events[:, 0])
            omega_vals.extend(events[:, 1])
            total_events = len(theta_vals)
        
        # Prepare for next iteration
        t_start = sol.t[-1]
        y_current = sol.y[:, -1]
        
        # Break if no events are found to prevent infinite loop
        if events.size == 0:
            break

    # Limit to 500 points
    theta_vals = theta_vals[:max_events]
    omega_vals = omega_vals[:max_events]
    plt.scatter(omega_vals, theta_vals, s=1, label=f"θ₀={y0[0]}, ω₀={y0[1]}")
    
plt.title("Surface of Section for Various Initial Conditions")
plt.xlabel("ω")
plt.ylabel("θ")
plt.legend()
plt.grid(True)
plt.show()
