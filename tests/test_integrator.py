import os
import sys
import numpy as np

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ComputationalProject.integrator import compute_pendulum_trajectory


def test_compute_pendulum_trajectory_shapes_and_finite():
    times, theta_values, theta_dot_values = compute_pendulum_trajectory(
        x0=1.0, omega=2.0, theta0=0.1, theta_dot0=0.0, N_periods=4
    )

    assert len(times) == 5  # N_periods + 1 samples at multiples of 2*pi
    assert theta_values.shape == theta_dot_values.shape == (5,)
    assert np.all(np.isfinite(theta_values))
    assert np.all(np.isfinite(theta_dot_values))
