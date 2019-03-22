from .individuals import Individuals, np


class GeneticAlgorithm:
    __mutation_rate = 0.03

    __k = 0.75

    def __init__(self, size_population, interval, type_individual, fitness_function):

        self.__interval = interval
        self.__population = self._generateRandomPopulation(size_population, interval, type_individual)

        self.fitness_function = fitness_function
        self._evaluatePopulation(self.__population)

        self.best_individuals = self._getBestIndividuals(self.__population)
        self.best_individuals.wasChosen = False

    def _generateRandomPopulation(self, size_population, interval, type_individual):
        if type_individual is float and np.array(interval).ndim == 2:
            population = list()

            for i in range(size_population):
                random_sample = list()
                for limit in interval:
                    random_sample.append(np.random.uniform(min(limit), max(limit)))

                population.append(Individuals.numpy(np.array(random_sample)))
        else:
            raise NotImplementedError

        return population

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
        size_population = len(self.__population)

        for i in range(number_individuals):
            individuals_list.append(self.__population[np.random.randint(0, size_population)])

        best_individuals = self._getBestIndividuals(individuals_list)

        worse_individuals = self._getWorseIndividuals(individuals_list)

        best_individuals.wasChosen = False
        worse_individuals.wasChosen = False

        return best_individuals, worse_individuals

    def _evaluatePopulation(self, population):
        for individuals in population:
            individuals.score = self.fitness_function(individuals.chromosome)

    def _getBestIndividuals(self, population):
        best_individuals = population[0]
        best_score = float("inf")

        for individuals in population:

            if not individuals.wasChosen and individuals.score < best_score:
                best_individuals = individuals
                best_score = individuals.score

        best_individuals.wasChosen = True

        return best_individuals

    def _getWorseIndividuals(self, population):
        worse_indindividuals = population[0]
        worse_score = - float("inf")

        for individuals in population:
            if not individuals.wasChosen and individuals.score > worse_score:
                worse_indindividuals = individuals
                worse_score = individuals.score

        worse_indindividuals.wasChosen = True

        return worse_indindividuals

    def oneStep(self):
        parents = self._selectParents(int(len(self.__population) * 2 / 3))

        childrens = self._generateChildrens(parents)

        self._evaluatePopulation(childrens)

        best_children = self._getBestIndividuals(childrens)

        best_children.wasChosen = False

        self._replace(childrens)

        return best_children

    def execute(self):

        best_children = self.oneStep()

        if best_children.score < self.best_individuals.score:
            self.best_individuals = best_children

        return self.best_individuals

    def _generateChildrens(self, parents):
        childrens = list()

        i = 0
        while i < len(parents) - 1:
            child_1, child_2 = self._Crossover(parents[i], parents[i + 1])
            childrens.extend([self._Mutate(child_1), self._Mutate(child_2)])
            i += 2

        return childrens

    def _replace(self, childrens):

        self.__population.extend(childrens)

        for i in range(len(childrens)):
            worse = self._getWorseIndividuals(self.__population)
            self.__population.remove(worse)

    def _Mutate(self, children):

        if np.random.uniform(0, 1) < self.__mutation_rate:
            self._mutating(children)

        return children

    def _Crossover(self, father, mother):
        increment = int(father.chromosome.size / 5)
        if increment == 0:
            increment = int(father.chromosome.size / 2)

        end_point = increment
        child_1_chromosome = np.zeros(shape=father.chromosome.size, dtype=father.chromosome.dtype)

        child_2_chromosome = np.zeros(shape=father.chromosome.size, dtype=father.chromosome.dtype)

        switch = True

        for i in range(father.chromosome.size):
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
        best, worse = self._selectRandomIndividuals(len(self.__population))

        max_value = best.chromosome.max()
        min_value = worse.chromosome.min()

        for i in range(int(child.chromosome.size / 5 + 1)):
            self._mutateChromosome(child.chromosome, max_value, min_value)

    def _sumOrSubtract(self):
        if np.random.uniform(0, 1) < 0.5:
            return -1
        else:
            return 1

    def _mutateChromosome(self, chromosome, max_value, min_value):

        index = np.random.randint(0, chromosome.size)

        operation = self._sumOrSubtract()
        new_value = (max_value * np.random.rand() + min_value) * operation + chromosome[index]

        while new_value > max(self.__interval[index]) or new_value < min(self.__interval[index]):
            operation = self._sumOrSubtract()
            new_value = (max_value * np.random.rand() + min_value) * operation + chromosome[index]

        chromosome[index] = new_value
