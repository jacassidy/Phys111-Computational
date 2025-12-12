import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import csv
import math

x0 = 1
omega = 2

theta0 = np.pi                      # x0 = 1 omega = 2 theta dot = 0 barrier = * 3.9626375/5
theta_dot0 = 2.5
y0 = [theta0, theta_dot0]

def pendulum_ode(t, y):
    theta = y[0]
    theta_dot = y[1]
    numerator = (
        np.sin(theta) * (g - theta_dot * omega * x0 * np.cos(t))
        + omega * x0 * (omega * np.cos(theta) * np.sin(t) + np.cos(t) * np.sin(theta))
    )
    theta_double_dot = numerator / d
    return [theta_dot, theta_double_dot]

d = 1.0
g = 9.81

N_periods = 500
t_start = 0
t_end = 2 * np.pi * N_periods

n_values = np.arange(0, N_periods + 1)
t_mark = 2 * np.pi * n_values

sol = solve_ivp(
    pendulum_ode,
    [t_start, t_end],
    y0,
    t_eval=t_mark,
    method='RK45',
    rtol=1e-8,
    atol=1e-8
)

theta_values = sol.y[0]
theta_dot_values = sol.y[1]
times = sol.t

plt.figure(figsize=(12, 6))
#np.fmod(theta_values, 2* np.pi)
plt.scatter(theta_values, theta_dot_values, color='red', zorder=5)
plt.title(f'Phase-Space: x0 = {x0:.4f}, omega = {omega:.4f}, θ0 = {theta0:.8f}, θ̇0 = {theta_dot0:.4f}')
plt.xlabel('Theta (rad)')
plt.ylabel('Theta_dot (rad/s)')
plt.grid(True)
plt.show()

print("Theta (rad)\tTheta_dot (rad/s)")

for t, theta, theta_dot in zip(times, theta_values, theta_dot_values):
    print(f"{theta:.4f}\t\t{theta_dot:.4f}")

    # Specify the filename
filename = 'theta_theta_dot.csv'

# Write to a CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['Theta', 'Theta Dot'])
    
    # Write the data
    for t, theta, theta_dot in zip(times, theta_values, theta_dot_values):
        writer.writerow([f"{theta:.4f}", f"{theta_dot:.4f}"])


