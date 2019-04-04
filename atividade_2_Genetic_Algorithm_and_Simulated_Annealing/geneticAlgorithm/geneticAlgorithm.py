from .individuals import Individuals, np
from multiprocessing.pool import Pool
from multiprocessing import cpu_count

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class GeneticAlgorithm:
    __mutation_rate = 0.05
    __k = 0.75

    def __init__(self, size_population, interval, type_individual, fitness_function, minimization=True):

        self._minimization_problem = minimization
        self.__interval = np.array(interval)
        self._population = self._generateRandomPopulation(size_population, type_individual)

        self.fitness_function = fitness_function
        self._evaluatePopulation(self._population)

        if minimization:
            self.best_individuals = self._getMinScoreIndividual(self._population)
        else:
            self.best_individuals = self._getMaxScoreIndividual(self._population)

        self.best_individuals.wasChosen = False

    def _generateRandomPopulation(self, size_population, type_individual):
        population = list()

        if type_individual == float and type(self.__interval) == np.ndarray:
            for i in range(size_population):
                population.append(Individuals.numpy(self._gerateRandom_Sample()))

        else:
            raise NotImplementedError

        return population

    def _removeLastDim(self, shape):
        new_shape = list(shape)
        new_shape.remove(new_shape[-1])
        return tuple(new_shape)

    def _getIntevalSize(self):
        new_size = 1
        for size in self._removeLastDim(self.__interval.shape):
            new_size *= size
        return new_size

    def _gerateRandom_Sample(self):
        new_size = self._getIntevalSize()
        new_shape = self._removeLastDim(self.__interval.shape)

        interval = self.__interval.reshape(new_size, 2)

        random_sample = list()

        for limit in interval:
            random_sample.append(np.random.uniform(np.min(limit), np.max(limit)))

        return np.array(random_sample).reshape(new_shape)

    def _selectParents(self, n_parents):
        parents = list()

        # torneiro  (Mitchell 1997)
        for i in range(n_parents):
            best, worse = self._selectRandomIndividuals(n_parents)

            if np.random.uniform(0, 1) < self.__k:  # k = 0.75
                parents.append(best)
            else:
                parents.append(worse)

        return parents

    def _selectRandomIndividuals(self, number_individuals):
        individuals_list = list()
        size_population = len(self._population)

        for i in range(number_individuals):
            individuals_list.append(self._population[np.random.randint(0, size_population)])

        if self._minimization_problem:
            best_individuals = self._getMinScoreIndividual(individuals_list)
            worse_individuals = self._getMaxScoreIndividual(individuals_list)
        else:
            best_individuals = self._getMaxScoreIndividual(individuals_list)
            worse_individuals = self._getMinScoreIndividual(individuals_list)

        best_individuals.wasChosen = False
        worse_individuals.wasChosen = False

        return best_individuals, worse_individuals

    def _evaluatePopulation(self, population):
        # max_threads = int(cpu_count() - 1)
        # size = len(population)
        #
        # for i in range(1, max_threads + 1):
        #     pool = Pool(max_threads)
        #     chromosome_list = [individuals.chromosome for individuals in
        #                        population[int((i - 1) * size / 3):int(i * size / 3)]]
        #     scores = pool.map(self.fitness_function, chromosome_list)
        #
        #     for score, individual in zip(scores, [individuals for individuals in
        #                                           population[int((i - 1) * size / 3):int(i * size / 3)]]):
        #         individual.score = score
        #
        #     pool.close()
        #     pool.join()
        # single thread
        for individual in population:
            individual.score = self.fitness_function(individual.chromosome)
            print("{} z:{}".format(individual.chromosome,individual.score))


    def _getMinScoreIndividual(self, population):

        min_score_individual = population[0]
        min_score = float("inf")

        for individuals in population:

            if not individuals.wasChosen and individuals.score < min_score:
                min_score_individual = individuals
                min_score = individuals.score

        min_score_individual.wasChosen = True

        return min_score_individual

    def _getMaxScoreIndividual(self, population):

        max_score_individual = population[0]
        max_score = - float("inf")

        for individuals in population:
            if not individuals.wasChosen and individuals.score > max_score:
                max_score_individual = individuals
                max_score = individuals.score

        max_score_individual.wasChosen = True

        return max_score_individual

    def oneStep(self):
        parents = self._selectParents(int(len(self._population) * 2 / 3))

        childrens = self._generateChildrens(parents)

        self._evaluatePopulation(childrens)

        if self._minimization_problem:
            best_children = self._getMinScoreIndividual(childrens)
        else:
            best_children = self._getMaxScoreIndividual(childrens)

        best_children.wasChosen = False

        self._replace(childrens)

        return best_children

    def execute(self):

        while self._variancePopulation() > 0.00001:

            best_children = self.oneStep()

            # self._plotIndividuals() concertar


            if self._minimization_problem:
                if best_children.score < self.best_individuals.score:
                    self.best_individuals = best_children
            else:
                if best_children.score > self.best_individuals.score:
                    self.best_individuals = best_children

        return self.best_individuals

    def print(self):

        for individual in self._population:
            print("score: {} , chormosome: {}".format(individual.score, individual.chromosome))

    def populationToCSV(self, fileName):

        save_list = np.array([individual.chormosome for individual in self._population])

        np.savetxt(fileName, save_list, delimiter=",")

    def _generateChildrens(self, parents):
        childrens = list()

        i = 0
        while i < len(parents) - 1:
            child_1, child_2 = self._Crossover(parents[i], parents[i + 1])
            childrens.extend([self._Mutate(child_1), self._Mutate(child_2)])
            i += 2

        return childrens

    def _replace(self, childrens):

        self._population.extend(childrens)
        n_childrens = len(childrens)

        if self._minimization_problem:
            self._remove_by_max_score(n_childrens)
        else:
            self._remove_by_min_score(n_childrens)

    def _remove_by_max_score(self, n_childrens):
        for i in range(n_childrens):
            worse = self._getMaxScoreIndividual(self._population)
            self._population.remove(worse)

    def _remove_by_min_score(self, n_childrens):
        for i in range(n_childrens):
            worse = self._getMinScoreIndividual(self._population)
            self._population.remove(worse)

    def _Mutate(self, children):

        if np.random.uniform(0, 1) < self.__mutation_rate:
            self._mutating(children)

        return children

    def _Crossover(self, father, mother):
        size = len(father.chromosome)

        increment = int(size / 5)
        if increment == 0:
            increment = int(size / 2)

        end_point = increment
        child_1_chromosome = np.zeros(shape=father.chromosome.shape, dtype=father.chromosome.dtype)

        child_2_chromosome = np.zeros(shape=father.chromosome.shape, dtype=father.chromosome.dtype)

        switch = True

        for i in range(size):
            if switch:
                child_1_chromosome[i] = father.chromosome[i]
                child_2_chromosome[i] = mother.chromosome[i]
            else:
                child_1_chromosome[i] = mother.chromosome[i]
                child_2_chromosome[i] = father.chromosome[i]

            if i + 1 == end_point:
                end_point += increment
                switch = not switch

        return Individuals.numpy(child_1_chromosome), Individuals.numpy(child_2_chromosome)

    def _mutating(self, child):

        for i in range(int(child.chromosome.size / 5 + 1)):
            self._mutateChromosome(child)

    def _sumOrSubtract(self):
        if np.random.uniform(0, 1) < 0.5:
            return -1
        else:
            return 1

    def _mutateChromosome(self, child):

        index = np.random.randint(0, child.chromosome.size)

        new_size = self._getIntevalSize()

        interval = self.__interval.reshape(new_size, 2)

        temp_shape = child.chromosome.reshape((child.chromosome.size,))

        new_value = np.random.uniform(np.min(interval[index]), np.max(interval[index]))

        temp_shape[index] = new_value

        child.chromosome = temp_shape.reshape(child.chromosome.shape)

    def _variancePopulation(self):
        return np.array([individual.chromosome for individual in self._population]).var()

    # plot for rastring
    def _plotIndividuals(self):
        self._createGraph()
        plt.ion()
        
        x = list()
        y = list()
        z = list()
        for individual in self._population:
            x.append(individual.chromosome[0])
            y.append(individual.chromosome[1])
            z.append(self.fitness_function(individual.chromosome))

        plt.plot(x,y,z,'or')

        plt.show()
       

    def _createGraph(self):
        x = np.arange(-5.12,5.12 ,0.05)
        y = np.arange(-5.12, 5.12,0.05)
        z = np.array([self.fitness_function([i,i]) for i in x ] )

        x, y = np.meshgrid(x, y)
        z , z = np.meshgrid(z,z)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_wireframe(x, y, z, rstride=10, cstride=10)
   
  