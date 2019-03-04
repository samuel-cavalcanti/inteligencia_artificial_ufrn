from geneticAlgorithm import np ,Individuals ,GeneticAlgorithm


def rastrigin(X):
    A = 10  
    return A*len(X) + np.sum([(x**2 - A * np.cos(2 * np.pi * x)) for x in X])


def InitializePopulation(size_population):
    population = list()
    # env.observation_space.n
    for i  in range(size_population):
        population.append(Individuals(2,5000,-5000,float))

    return population


if __name__ == '__main__':
    population = InitializePopulation (5)
    

    
    ga = GeneticAlgorithm(population,rastrigin)

    solution = ga.execute()
    it = 0
    while solution.score > 0:
        solution = ga.execute()
        it+=1
        print("solution",solution.score,"it",it)
    
    print("Finish!")
    print("solution",solution.score,"it",it)
    print("solutionVector",solution.chromosome)

    pass