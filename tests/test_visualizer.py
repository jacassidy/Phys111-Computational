import os
import sys
import csv
import numpy as np

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ComputationalProject.visualizer import theta_to_positions, load_theta_series


def test_theta_to_positions_basic():
    theta_values = np.array([0.0, np.pi / 2, np.pi])
    x_pos, y_pos = theta_to_positions(theta_values, pivot=(0, 0), d=1.0)

    assert np.allclose(x_pos, [0.0, 1.0, 0.0])
    # y positions: pivot_y - d*cos(theta): cos(0)=1 -> 0-1=-1; cos(pi/2)=0 -> 0-0=0; cos(pi)=-1 -> 0-(-1)=1
    assert np.allclose(y_pos, [-1.0, 0.0, 1.0])


def test_load_theta_series(tmp_path):
    p = tmp_path / "temp_theta.csv"
    with open(p, "w") as f:
        f.write("Time,Theta,Theta Dot\n")
        f.write("0.0,0.0,0.0\n")
        f.write("1.0,1.5708,0.0\n")

    arr = load_theta_series(str(p))
    assert arr.shape == (2,)
    assert np.allclose(arr, [0.0, 1.5708])
