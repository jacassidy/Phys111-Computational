"""ARCHIVED: duplicate variant of the double pendulum script.

Use `6c.py` or `partcatt4.py` for canonical simulations. This file is
kept for reference and will not be run by the Makefile.
"""

import sys
print('This is an archived file — original content is copied into Pset6/archive/')
sys.exit(0)

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

    # Derivatives of theta1 and theta2
    dtheta1_dt = omega1
    dtheta2_dt = omega2

    # Derivatives of omega1 and omega2
    domega1_dt = (
        -np.sin(delta_theta) * (omega1**2 * np.cos(delta_theta) + omega2**2)
        - (2 * np.sin(theta1) - np.sin(theta2) * np.cos(delta_theta))
    ) / (omega2 * (1 + np.sin(delta_theta)**2))

    domega2_dt = (
        np.sin(delta_theta) * (omega1**2 + omega2**2 * np.cos(delta_theta))
        + (np.sin(theta1) * np.cos(delta_theta) - 2 * np.sin(theta2))
    ) / (omega2 * (1 + np.sin(delta_theta)**2))

    return [dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt]

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
        else:
            omega2 = np.random.choice([(-B + np.sqrt(discriminant)) / (2 * A),
                                    (-B - np.sqrt(discriminant)) / (2 * A)])
            initial_conditions.append([theta1, omega1, theta2, omega2])
    return initial_conditions

# Parameters
H_target = 1.0
num_conditions = 5  # Number of initial conditions
t_span = [0, 2 * np.pi]  # Integrate over one period (2π)
num_points = 500  # Number of points to sample during the integration

# Generate initial conditions
initial_conditions = generate_initial_conditions(H_target, num_conditions)

# Plotting
plt.figure(figsize=(12, 8))

for y0 in initial_conditions:
    # Integrate the system over the time span [0, 2π]
    sol = solve_ivp(
        equations, t_span, y0, t_eval=np.linspace(t_span[0], t_span[1], num_points),
        dense_output=True
    )

    # Extract theta1 and omega1 values from the solution
    theta1_vals = sol.y[0]
    omega1_vals = sol.y[1]

    # Plot the results
    plt.plot(omega1_vals, theta1_vals, lw=0.8, label=f"θ₀={y0[0]:.2f}, ω₀={y0[1]:.2f}")

# Adjust plot limits if needed
# plt.xlim([-5, 5])
# plt.ylim([-4 * np.pi, 4 * np.pi])

# Plot labels and grid
plt.title("Phase Plot of θ₁ vs ω₁ over One Period")
plt.xlabel("ω₁")
plt.ylabel("θ₁")
plt.legend()
plt.grid(True)
plt.show()
