
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

	# Equation 1: d(theta1)/d(theta2) = omega1 / omega2
	dtheta1_dt = omega1
	dtheta2_dt = omega2

	# Equation 2: domega1/dtheta2
	domega1_dt = (
		-np.sin(delta_theta) * (omega1**2 * np.cos(delta_theta) + omega2**2)
		- (2 * np.sin(theta1) - np.sin(theta2) * np.cos(delta_theta))
	) / (omega2 * (1 + np.sin(delta_theta)**2))

	# Equation 3: domega2/dtheta2
	domega2_dt = (
		np.sin(delta_theta) * (omega1**2 + omega2**2 * np.cos(delta_theta))
		+ (np.sin(theta1) * np.cos(delta_theta) - 2 * np.sin(theta2))
	) / (omega2 * (1 + np.sin(delta_theta)**2))

	return [dtheta1_dt, domega1_dt, dtheta2_dt, domega2_dt]

# Event function to detect theta2 crossing zero
def theta2_crossing(t, y):
	theta2 = y[2]
	return np.sin(theta2/2)
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
num_conditions = 5  # Increase the number of initial conditions
max_events = 500  # Increase number of points per trajectory

# Generate initial conditions
initial_conditions = generate_initial_conditions(H_target, num_conditions)

# Plotting
plt.figure(figsize=(12, 8))

for y0 in initial_conditions:
	t_start = 0
	t_interval = 50 * 2 * np.pi  # Time interval for each integration step
	total_events = 0
	theta_vals = []
	omega_vals = []
	y_current = y0.copy()

	while total_events < max_events:
		t_end = t_start + t_interval
		sol = solve_ivp(
			equations, [t_start, t_end], y_current,
			events=theta2_crossing, dense_output=True
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

# plt.xlim([-20, 20])  # Adjust based on the range of omega values
# plt.ylim([-4*np.pi, 4*np.pi])  # Adjust based on the range of theta values

plt.title("Surface of Section for Various Initial Conditions")
plt.xlabel("ω")
plt.ylabel("θ")
plt.legend()
plt.grid(True)
plt.show()
