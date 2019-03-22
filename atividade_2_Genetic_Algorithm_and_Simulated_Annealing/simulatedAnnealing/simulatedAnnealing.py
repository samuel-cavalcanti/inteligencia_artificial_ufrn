import numpy as np
from .atomicState import AtomicState


class SimulatedAnnealing:

    def __init__(self, cost_function, interval, type_atom, t=100, r=0.999, k=50, t_min=1e-6):
        self.__cost = cost_function
        self.__t = t
        self.__r = r
        self.__k = k
        self.__t_min = t_min
        self.__interval = interval

        self.best_solution = self._generateAtom(interval, type_atom)
        self.__current_solution = self.best_solution
        self.__best_energy = cost_function(self.best_solution.getTensor())

    def _generateAtom(self, interval, type_atom):

        if type_atom is float and np.array(interval).ndim == 2:

            random_state = list()
            for limit in interval:
                random_state.append(np.random.uniform(min(limit), max(limit)))

        else:
            raise NotImplementedError

        return AtomicState.numpy(np.array(random_state))

    def oneStep(self):
        current_energy = self.__cost(self.__current_solution.getTensor())
        neighbours = self._generateNeighbours()

        for i in range(self.__k):
            neighbour = self._getRandomNeighbour(neighbours)

            neighbour_energy = self.__cost(neighbour.getTensor())

            delta = neighbour_energy - current_energy

            if delta <= 0 or np.exp(-delta / self.__t) > np.random.rand():
                current_energy = neighbour_energy
                self.__current_solution = neighbour

                if current_energy < self.__best_energy:
                    self.__best_energy = current_energy
                    self.best_solution = neighbour

        return self.__current_solution

    def execute(self, energy=-float("inf"), debug=False):
        if debug:
            n_steps = 0
            all_solutions = list()
        while self.__t > self.__t_min and self.__best_energy > energy:
            self.oneStep()
            self.__t *= self.__r
            if debug:
                n_steps += 1
                all_solutions.append(self.__best_energy)

        if debug:
            return n_steps, all_solutions, self.best_solution

        return n_steps, self.best_solution

    def _getRandomNeighbour(self, neighbours):
        size = len(neighbours)
        return neighbours[np.random.randint(0, size)]

    def _generateNeighbours(self):
        tensor = self.__current_solution.getTensor()
        max_energy = tensor.max()
        min_energy = tensor.min()

        neighbours = list()

        for i in range(self.__k):
            neighbours.append(self._generateNeighbour(max_energy, min_energy, tensor))
            # print(neighbours[i].getTensor())

        return neighbours

    def _generateNeighbour(self, rand_value_max, rand_value_min, tensor):
        if self.best_solution.getTensor().dtype is np.dtype("float"):
            return AtomicState.numpy(self._generateRandomTensor(rand_value_max, rand_value_min, tensor))
        else:
            raise NotImplementedError

    def _generateRandomTensor(self, rand_value_max, rand_value_min, current_tensor):
        random_tensor = list()

        for limit, current_tensor_value in zip(self.__interval, current_tensor):
            random_tensor.append(self._generateRandomValue(limit, current_tensor_value, rand_value_max, rand_value_min))

        return np.array(random_tensor)

    def _generateRandomValue(self, limit, current_tensor_value, rand_value_max, rand_value_min):

        random_value = np.random.uniform(low=rand_value_min, high=rand_value_max)
        random_value = random_value * self._sumOrSubtract() + current_tensor_value
        while random_value > max(limit) or random_value < min(limit):
            random_value = np.random.uniform(low=rand_value_min,
                                             high=rand_value_max) * self._sumOrSubtract() + current_tensor_value

        return random_value

    def _sumOrSubtract(self):
        if np.random.uniform(0, 1) < 0.5:
            return -1
        else:
            return 1
