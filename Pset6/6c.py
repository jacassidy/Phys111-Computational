import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
g = 9.81  # Gravity (m/s^2)
L1 = L2 = 1.0  # Length of both pendulums (m)
m1 = m2 = 1.0  # Mass of both pendulums (kg)

# Hamiltonian function to compute total energy
def hamiltonian(theta1, theta2, omega1, omega2):
    delta_theta = theta2 - theta1
    H = (1/2) * (m1 + m2) * L1**2 * omega1**2 + \
        (1/2) * m2 * L2**2 * omega2**2 + \
        m2 * L1 * L2 * omega1 * omega2 * np.cos(delta_theta) - \
        (m1 + m2) * g * L1 * np.cos(theta1) - \
        m2 * g * L2 * np.cos(theta2)
    return H

# System of equations for the double pendulum
def equations(t, y):
    theta1, omega1, theta2, omega2 = y
    delta_theta = theta2 - theta1

    denom1 = (m1 + m2) * L1 - m2 * L1 * np.cos(delta_theta)**2
    denom2 = (L2 / L1) * denom1

    domega1_dt = (m2 * L1 * omega1**2 * np.sin(delta_theta) * np.cos(delta_theta) +
                  m2 * g * np.sin(theta2) * np.cos(delta_theta) +
                  m2 * L2 * omega2**2 * np.sin(delta_theta) -
                  (m1 + m2) * g * np.sin(theta1)) / denom1

    domega2_dt = (-m2 * L2 * omega2**2 * np.sin(delta_theta) * np.cos(delta_theta) +
                  (m1 + m2) * (g * np.sin(theta1) * np.cos(delta_theta) -
                  L1 * omega1**2 * np.sin(delta_theta) -
                  g * np.sin(theta2))) / denom2

    return [omega1, domega1_dt, omega2, domega2_dt]

# Event function to detect theta2 crossing zero
def theta2_crossing(t, y):
    theta2 = y[2]
    return theta2
theta2_crossing.direction = 1  # Positive crossing only
theta2_crossing.terminal = False

# Generate initial conditions with H = 1
def generate_initial_conditions(H_target, num_conditions):
    initial_conditions = []
    for _ in range(num_conditions):
        theta1 = np.random.uniform(-np.pi, np.pi)
        theta2 = np.random.uniform(-np.pi, np.pi)
        omega1 = np.random.uniform(-3, 3)  # Increased range for omega1

        delta_theta = theta1 - theta2
        A = (1/2) * m2 * L2**2
        B = m2 * L1 * L2 * omega1 * np.cos(delta_theta)
        C = (1/2) * (m1 + m2) * L1**2 * omega1**2 - \
            (m1 + m2) * g * L1 * np.cos(theta1) - \
            m2 * g * L2 * np.cos(theta2) - H_target

        discriminant = B**2 - 4 * A * C
        if discriminant < 0:
            continue
        omega2 = np.random.choice([(-B + np.sqrt(discriminant)) / (2 * A),
                                   (-B - np.sqrt(discriminant)) / (2 * A)])
        initial_conditions.append([theta1, omega1, theta2, omega2])
    return initial_conditions

# Parameters
H_target = 1.0
num_conditions = 10  # Increase the number of initial conditions
max_events = 1000  # Increase number of points per trajectory
t_span = [0, 5000]  # Longer integration time

# Generate initial conditions
initial_conditions = generate_initial_conditions(H_target, num_conditions)

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

for idx, y0 in enumerate(initial_conditions):
    sol = solve_ivp(equations, t_span, y0, events=theta2_crossing, dense_output=True, max_step=0.05)
    events = sol.y_events[0]

    theta1_vals = [e[0] for e in events[:max_events]]
    omega1_vals = [e[1] for e in events[:max_events]]

    ax.scatter(omega1_vals, theta1_vals, s=1, label=f"Trajectory {idx+1}")

# Autoscale the plot to fit all points
# ax.relim()  # Recompute the limits based on the data
# ax.autoscale_view()

ax.set_title("Poincaré Section of the Double Pendulum at θ₂ = 0")
ax.set_xlabel("ω₁")
ax.set_ylabel("θ₁")
ax.legend()
ax.grid(True)

plt.show()
