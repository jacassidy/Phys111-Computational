import numpy as np
import sympy as sp

# Define symbolic variable for w^2
w2 = sp.symbols('w2')

# System parameters
M_val = 1  # Mass of the cart
m = 0.1    # Mass of the pendulum
l = 0.0155 # Length of the pendulum
k = 158    # Spring constant
g = 9.81   # Gravitational acceleration

# K matrix (stiffness matrix)
K = np.array([[M_val + m, m],
              [m, m]], dtype=float)

# M matrix (mass matrix)
M = np.array([[k, 0],
              [0, -m * g / l]], dtype=float)

# Convert K and M to SymPy matrices
K_sym = sp.Matrix(K)
M_sym = sp.Matrix(M)

# Compute the matrix (K - w^2 * M)
A = K_sym - w2 * M_sym

# Compute the determinant of (K - w^2 * M)
determinant = A.det()
print("Characteristic equation (determinant):")
sp.pprint(determinant)

# Solve the equation determinant = 0 for w^2
w2_solutions = sp.solve(determinant, w2)

# Convert the solutions to numerical values
w2_values = [sol.evalf() for sol in w2_solutions]

print("\nEigenvalues (w^2):")
for i, w2_val in enumerate(w2_values):
    print(f"w^2_{i+1} = {w2_val}")

# For each eigenvalue, compute the eigenvector
print("\nCorresponding eigenvectors:")
for i, w2_val in enumerate(w2_values):
    # Substitute w^2 into (K - w^2 * M)
    A_sub = A.subs(w2, w2_val)

    # Compute the null space of (K - w^2 * M)
    null_space = A_sub.nullspace()

    if null_space:
        eigenvector = null_space[0]
        print(f"\nEigenvector corresponding to w^2_{i+1}:")
        sp.pprint(eigenvector / eigenvector.norm())  # Normalized eigenvector
    else:
        print(f"\nNo eigenvector found for w^2_{i+1}")
