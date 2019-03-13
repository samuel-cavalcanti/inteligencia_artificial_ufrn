import numpy as np
from .atomicState import AtomicState
class SimulatedAnnealing:

    def __init__(self,cost_function,s0,t=100 ,r=0.999 ,k=50,t_min =1e-6):
        self._cost = cost_function
        self._t = t
        self._r = r
        self._k = k
        self._t_min = t_min
        self.best_solution = s0
        self._current_solution = s0
        self._best_energy = cost_function(s0.getTensor())




    def oneStep(self):
        current_energy = self._cost(self._current_solution.getTensor())
        neighbours = self._generateNeighbours()

        for i in range(self._k):
            neighbour = self._getRandomNeighbour(neighbours)

            neighbour_energy = self._cost(neighbour.getTensor())

            delta =  neighbour_energy - current_energy 

            if delta <= 0 or np.exp(-delta/self._t) > np.random.rand():
                current_energy = neighbour_energy
                self._current_solution = neighbour

                if current_energy <  self._best_energy:
                    self._best_energy = current_energy
                    self.best_solution = neighbour

        return self._current_solution


    def execute(self, energy = -float("inf"), debug = False):
        if debug: 
          n_steps = 0
          all_solutions = list()
        while self._t > self._t_min and self._best_energy > energy:
            self.oneStep()
            self._t *= self._r
            if debug:
                n_steps +=1
                all_solutions.append(self._best_energy)

        if debug:
            return n_steps, all_solutions , self.best_solution

        
        return n_steps, self.best_solution


    def _getRandomNeighbour(self,neighbours):
        size = len(neighbours)
        return neighbours[np.random.randint(0,size)]


    def _generateNeighbour(self,rand_value_max,rand_value_min,tensor):
        randomTensor = np.random.rand(tensor.size) * (rand_value_max -rand_value_min)  + rand_value_min 
        
        randomTensor *= self._sumOrSubtract()

        if self.best_solution.getTensor().dtype is np.dtype("float"):
            return AtomicState.numpy( tensor + randomTensor  )
        else:
            raise NotImplementedError
        

    def _generateNeighbours(self):
        tensor = self._current_solution.getTensor()
        max_energy = tensor.max() 
        min_energy = tensor.min() 
        neighbours = list()

        for i in range( self._k ):
            neighbours.append( self._generateNeighbour(max_energy,min_energy,tensor) )
          

        return neighbours

    def _sumOrSubtract(self):
        if np.random.uniform(0,1) < 0.5:
            return -1
        else:
            return 1
