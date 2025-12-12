import numpy as np
from scipy.linalg import eig

# System parameters
M_val = 1  # Mass of the cart
m = 0.1    # Mass of the pendulum
l = 0.0155 # Length of the pendulum
k = 158    # Spring constant
g = 9.81   # Gravitational acceleration

# K matrix (stiffness matrix)
K = np.array([[M_val + m, m],
              [m, m]])

# M matrix (mass matrix)=
M = np.array([[k, 0],
              [0, -m * g / l]])

# Solve the generalized eigenvalue problem K * x = (w^2) * M * x
eigenvalues, eigenvectors = eig(K, M)

# Extract the real part of the eigenvalues (w^2)
w_squared = np.real(eigenvalues)

# Display the results
print("Eigenvalues (w^2) where determinant of (K - w^2 * M) is zero:")
for i, w2 in enumerate(w_squared):
    print(f"w^2_{i+1} = {w2}")

print("\nCorresponding generalized eigenvectors:")
for i, vector in enumerate(eigenvectors.T):
    print(f"\nEigenvector corresponding to w^2_{i+1}:")
    print(vector)
