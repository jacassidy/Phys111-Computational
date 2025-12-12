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
        omega1 = np.random.uniform(-3, 3)

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
num_conditions = 1  # Number of initial conditions
n_periods = 500  # Number of periods of 2*pi to integrate over
t_span = [0, n_periods * 2 * np.pi]  # Integration range over multiple 2*pi

# Generate time points that are multiples of 2*pi
t_eval = np.linspace(0, n_periods * 2 * np.pi, n_periods + 1)  # +1 to include final point

custom_conditions = [
    [0.07631665138194496, 1.8710595719374388, 1.2587309323019882, np.float64(5.66717583497082)],
    [-0.304198885511492, 0.8899719830642365, 0.36456813055000364, np.float64(6.829845818564733)],
    [-0.823881223714715, -1.324646220874196, -1.4448605001938697, np.float64(6.441528145270578)],
    [0.35578420861064497, 2.6837214233724183, -0.9908559397593715, np.float64(-6.5534712888715205)],
    [-1.4860308183079447, -2.4352890400436147, 0.8556197807738692, np.float64(-4.73089853468153)],
    [0.3206373864808669, -1.1895619150325352, 1.0719624024790668, np.float64(-5.95358557718188)],
    [0.495115642243321, 1.7143881072358396, 0.7224131630937448, np.float64(5.269347916759773)]

]

# Generate initial conditions
# initial_conditions = generate_initial_conditions(H_target, num_conditions)
initial_conditions = custom_conditions

# Plotting
plt.figure(figsize=(12, 8))


for y0 in initial_conditions:
    # Integrate the system over the specified time span with desired t_eval
    sol = solve_ivp(
        equations, t_span, y0, t_eval=t_eval, dense_output=True
    )

    # Extract theta1 and omega1 values from the solution
    theta1_vals = sol.y[0]
    omega1_vals = sol.y[1]

    # Plot the results
    plt.plot(theta1_vals, omega1_vals, lw=0.8, label=f"θ₀={y0[0]:.2f}, ω₀={y0[1]:.2f}")

# Adjust plot limits if needed
# plt.xlim([-5, 5])
# plt.ylim([-4 * np.pi, 4 * np.pi])

# Plot labels and grid
print(initial_conditions)

plt.title("Phase Plot of θ₁ vs ω₁ over Multiple Periods")
plt.ylabel("ω₁")
plt.xlabel("θ₁")
plt.legend()
plt.grid(True)
import os

figdir = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(figdir, exist_ok=True)
figpath = os.path.join(figdir, "partcatt4.png")
plt.savefig(figpath, dpi=200, bbox_inches='tight')
print(f"Saved figure to {figpath}")
plt.close()
