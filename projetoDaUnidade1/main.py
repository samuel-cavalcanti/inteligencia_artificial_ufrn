from geneticAlgorithm import Individuals ,GeneticAlgorithm
import numpy as np
import matplotlib.pyplot as plt

def rastrigin(X):
    A = 10  
    return A*len(X) + np.sum([(x**2 - A * np.cos(2 * np.pi * x)) for x in X])


def InitializePopulation(size_population,ndim,limit_value):
    population = list()
 
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
       
    
   
    return it , np.array(all_score)

def benckmarkAG(n=30,plot_best_score=False):
    total_it = list()
    total_score = list()
    for i in range(n):
        it , score = executeAG()
        total_it.append(it)
        total_score.append(score)
    
    total_it = np.array(total_it)
    best_score_index = total_it.argmin()

    if plot_best_score:
        plt.plot(total_score[best_score_index])
        plt.ylabel("Best Individual")
        plt.xlabel("iteration")
        plt.title("Best Result")
        plt.savefig("gráficos/Rastrigin_Por_Interacao.png",)
        plt.show()

        
    #/home/samuel/Documents/Repositories/atividades_IA/projetoDaUnidade1/gráficos
    return total_it.mean() , total_it.std()


if __name__ == '__main__':
    # mean , std = benckmarkAG(n=100,plot_best_score=True)
    # print("mean:",mean,"std:",std) # mean: 3315.01 std: 1028.5962521320014

    pass