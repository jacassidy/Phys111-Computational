import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp

# Define the functions
def f(x):
    return x * np.tanh(x)

def g(x):
    return x**2 / (1 + x)

def parta():
    
    # Generate x values over the interval [0, 5]
    x = np.linspace(0, 5, 400)

    # Compute the y values for f(x) and g(x)
    y_f = f(x)
    y_g = g(x)

    # Plot the functions
    plt.plot(x, y_f, label=r'$f(x) = x \tanh(x)$')
    plt.plot(x, y_g, label=r'$g(x) = \frac{x^2}{1 + x}$', linestyle='--')

    # Labeling the plot
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of f(x) and g(x) over [0, 5]')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()


def partb():
    # Define the equation f(x) - g(x) - 1/2 = 0
    def equation(x):
        return f(x) - g(x) - 1/2

    # Initial guess for the solution
    x0 = 1.0

    # Find the root of the equation
    solution = fsolve(equation, x0)

    print(f'The solution to f(x) - g(x) = 1/2 is x = {solution[0]:.4f}')


def partc():
    # Define the system of differential equations
    def system(t, y):
        x, v = y
        dxdt = v
        dvdt = t**2 - x**2
        return [dxdt, dvdt]

    # Time range and initial conditions
    t_span = [-10, 10]
    y0 = [0, 0.5]  # x(0) = 0, v(0) = 0.5

    # Solve the system of ODEs
    sol = solve_ivp(system, t_span, y0, t_eval=np.linspace(-10, 10, 400))

    # Plot the solution for x(t)
    plt.plot(sol.t, sol.y[0], label=r'$x(t)$')

    # Labeling the plot
    plt.xlabel('t')
    plt.ylabel('x(t)')
    plt.title(r'Solution of $\ddot{x} + x^2 = t^2$ with $x(0) = 0$, $\dot{x}(0) = 0.5$')
    plt.grid(True)

    # Show the plot
    plt.show()

parta()
partb()
partc()
