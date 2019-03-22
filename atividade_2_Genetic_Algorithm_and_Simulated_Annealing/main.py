from geneticAlgorithm import GeneticAlgorithm
from simulatedAnnealing import SimulatedAnnealing, AtomicState

import numpy as np
import matplotlib.pyplot as plt


def rastrigin(X):
    A = 10
    return A * len(X) + np.sum([(x ** 2 - A * np.cos(2 * np.pi * x)) for x in X])


def InitializeInterval(size):
    interval = list()

    for i in range(size):
        interval.append([-5.12, 5.12])

    return interval


def executeAG(size_population=5):
    interval = InitializeInterval(2)
    ga = GeneticAlgorithm(size_population, interval, type(interval[0][0]), rastrigin)
    solution = ga.execute()
    all_score = [solution.score]
    it = 0
    all_it = [it]

    while solution.score > 0:
        solution = ga.execute()
        it += 1
        all_it.append(it)
        all_score.append(solution.score)

    return it, np.array(all_score)


def executeSA(debug=True):
    interval = [[-5.12, 5.12], [-5.12, 5.12]]
    sa = SimulatedAnnealing(rastrigin, interval, float)

    return sa.execute(0, debug=debug)


def plot(title, xlabel, ylabel, filename, array):
    plt.plot(array)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.savefig(filename)
    plt.show()


def benckmarkAG(n=30, plot_best_score=False):
    total_it = list()
    total_score = list()
    for i in range(n):
        it, score = executeAG(size_population=100)
        total_it.append(it)
        total_score.append(score)

    total_it = np.array(total_it)
    best_score_index = total_it.argmin()

    if plot_best_score:
        plot("Best Result", "iteration", "Best Individual", "gráficos/Rastrigin_Por_Interacao.png",
             total_score[best_score_index])

    return total_it.mean(), total_it.std()


def benckmarkSA(n=30, plot_best_score=False):
    total_it = list()
    total_solutions = list()
    for i in range(n):
        it, solutions, best_solution = executeSA(debug=True)
        total_it.append(it)
        total_solutions.append(solutions)

    best_score_index = np.argmin(total_it)

    if plot_best_score:
        plot("Best Result", "iteration", "Best Solution", "gráficos/recozimentoSimulado.png",
             total_solutions[best_score_index])

    return np.mean(total_it), np.std(total_it)


if __name__ == '__main__':
    # mean, std = benckmarkAG(n=5, plot_best_score=True)
    # print("mean:", mean, "std:", std)  # mean: 3315.01 std: 1028.5962521320014

    mean, std = benckmarkSA(n=5, plot_best_score=True)
    print("mean:", mean, "std:", std)

    pass
