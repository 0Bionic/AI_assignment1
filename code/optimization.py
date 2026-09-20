import math
import random

import matplotlib.pyplot as plt


def f_booth(x, y) -> float:
    return (x + 2 * y - 7) ** 2 + (2 * x + y - 5) ** 2


def f_himmelblau(x, y) -> float:
    return (x**2 + y - 11) ** 2 + (x + y**2 - 7) ** 2


def f_griewank(x, y) -> float:
    return (1 + (x**2 + y**2) / 4000) - (math.cos(x) * math.cos(y / math.sqrt(2)))


def returnWithinBound(value, min_val, max_val):
    # Makes sure the values remain in the given range
    return max(min_val, min(value, max_val))


def optimise(N, temp, K, function, minBound, maxBound, minimizing=True):
    """
    N is the neighbourhood size
    T is the starting temperature, reduced by 0.1 after K iterations
    K is the number of iterations to run for a given temperature
    """
    current_x = random.uniform(minBound, maxBound)
    current_y = random.uniform(minBound, maxBound)

    best_x, best_y = current_x, current_y
    # fix here - hassan
    best_f = function(current_x, current_y)

    # Lists to store the history for plotting
    history_x = []
    history_y = []
    history_f = []

    # Use 1e-5 instead of 0 to avoid floating point issues when subtracting 0.1
    while temp > 1e-5:
        for i in range(K):
            step_x = random.uniform(-N, N)
            step_y = random.uniform(-N, N)

            trial_x = returnWithinBound(current_x + step_x, minBound, maxBound)
            trial_y = returnWithinBound(current_y + step_y, minBound, maxBound)

            current_f = function(current_x, current_y)
            trial_f = function(trial_x, trial_y)

            if minimizing:
                delta = current_f - trial_f
            else:
                delta = trial_f - current_f

            if delta > 0:
                current_x, current_y = trial_x, trial_y

                if (minimizing and trial_f < best_f) or (
                    not minimizing and trial_f > best_f
                ):
                    best_x, best_y = trial_x, trial_y
                    best_f = trial_f
            else:
                m = math.exp(delta / temp)
                p = random.random()
                if p < m:
                    current_x, current_y = trial_x, trial_y

            # Record the state at each step
            history_x.append(current_x)
            history_y.append(current_y)
            history_f.append(function(current_x, current_y))

        # Decaying by 0.1 (fix)
        temp -= 0.1

    return best_x, best_y, best_f, history_x, history_y, history_f


def plot_graphs(history_x, history_y, history_f, title):
    """
    Plots the tracked values of x, y, and f matching the sample PDF style.
    """
    iterations = range(len(history_x))

    plt.figure(figsize=(8, 6))

    # Top Subplot: Objective Function (f)
    plt.subplot(2, 1, 1)
    plt.plot(
        iterations, history_f, color="red", marker=".", linestyle="-", label="Objective"
    )
    plt.title(f"Simulated Annealing - {title}")
    plt.legend(loc="lower right")

    # Variables (x and y)
    plt.subplot(2, 1, 2)
    # x uses a blue solid line with dots, y uses a green dashed line
    plt.plot(iterations, history_x, color="blue", marker=".", linestyle="-", label="x")
    plt.plot(iterations, history_y, color="green", linestyle="--", label="y")
    plt.legend(loc="upper right")

    plt.tight_layout()
    plt.show()


def main():
    neighbourhoodSize = 0.5
    startingTemperature = 1.0
    iterations = 100
    print("--- Booth Function ---")
    # Minimization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_booth, -10, 10, True
    )
    print(f"Minima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Booth Function (Minimization)")

    # Maximization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_booth, -10, 10, False
    )
    print(f"Maxima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Booth Function (Maximization)")

    print("\n--- Himmelblau Function ---")
    # Minimization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_himmelblau, -5, 5, True
    )
    print(f"Minima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Himmelblau Function (Minimization)")

    # Maximization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_himmelblau, -5, 5, False
    )
    print(f"Maxima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Himmelblau Function (Maximization)")

    print("\n--- Griewank Function ---")
    # Minimization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_griewank, -30, 30, True
    )
    print(f"Minima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Griewank Function (Minimization)")

    # Maximization
    best_x, best_y, best_f, hx, hy, hf = optimise(
        neighbourhoodSize, startingTemperature, iterations, f_griewank, -30, 30, False
    )
    print(f"Maxima: x = {best_x:.4f}, y = {best_y:.4f}, f(x,y) = {best_f:.4f}")
    plot_graphs(hx, hy, hf, "Griewank Function (Maximization)")


if __name__ == "__main__":
    main()
