from geneticAlgorithm import np ,Individuals ,GeneticAlgorithm
import matplotlib.pyplot as plt

def rastrigin(X):
    A = 10  
    return A*len(X) + np.sum([(x**2 - A * np.cos(2 * np.pi * x)) for x in X])


def InitializePopulation(size_population,ndim,limit_value):
    population = list()
    # env.observation_space.n
    for i  in range(size_population):
        population.append(Individuals(ndim,limit_value,-limit_value,float))

    return population

def executeAG(size_population=5,ndim=2,limit_value=5000):
    population = InitializePopulation(size_population=5,ndim=2,limit_value=5000)
    ga = GeneticAlgorithm(population,rastrigin)
    solution = ga.execute()
    all_score = [solution.score]
    it = 0
    all_it = [it]

    while solution.score > 0:
        solution = ga.execute()
        it+=1
        all_it.append(it)
        all_score.append(solution.score)
    
   
    return  np.array(all_it) , np.array(all_score)


if __name__ == '__main__':
    total_it = list()
    total_score = list()
    for i in range(30):
     list_it, list_score =  executeAG()
     total_it.append(list_it)
     total_score.append(list_score)

    total_it = np.array(total_it)
    total_score = np.array(total_score)


    print(total_it[:,-1].mean())
    print(total_it[:,-1])

    # plt.plot(all_it,all_score)
    # plt.ylabel("rastrigin")
    # plt.xlabel("iteration")
    # plt.show()

 
    pass