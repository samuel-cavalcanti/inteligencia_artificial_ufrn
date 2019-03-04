from individuals import Individuals ,np
class GeneticAlgorithm:
    _mutation_rate = 0.03

    _k = 0.75
    def __init__(self,population,fitness_function):

      self.population =population
      self.fitness_function = fitness_function
      self._evaluatePopulation(self.population)
     
      self.best_individuals = self._getBestIndividuals(population)
      self.best_individuals.wasChosen = False
     
   

    def _selectParents(self, n_parents):
      parents = list()

      #torneiro  (Mitchell 1997) 
      for i in range(n_parents):
        best , worse  = self._selectRandomIndividuals(n_parents)
     
        if np.random.uniform(0,1) < self._k: # k = 0.75
          parents.append(best)
        else:
          parents.append(worse)
  
    
      return parents

    

    def _selectRandomIndividuals(self,number_individuals):
      individuals_list = list()
      size_population = len(self.population)

      for i in range(number_individuals):
        individuals_list.append( self.population[np.random.randint(0,size_population)])
      

      best_individuals = self._getBestIndividuals(individuals_list)
      
      worse_individuals = self._getWorseIndividuals(individuals_list)

      best_individuals.wasChosen = False
      worse_individuals.wasChosen = False

      return best_individuals ,worse_individuals




    def _evaluatePopulation(self,population):
       for individuals in population:
        individuals.score = self.fitness_function(individuals.chromosome)
        
        
        
         
         

    def _getBestIndividuals(self,population):
        best_individuals = population[0]
        best_score =  float("inf")

        for individuals in population:
          
          if not individuals.wasChosen and individuals.score < best_score:
            best_individuals = individuals
            best_score = individuals.score
            
        best_individuals.wasChosen = True

        return best_individuals

    def _getWorseIndividuals(self,population):
      worse_indindividuals = population[0]
      worse_score = - float("inf")

      for individuals in population:
          if not individuals.wasChosen and individuals.score > worse_score:
            worse_indindividuals = individuals
            worse_score = individuals.score
            
      worse_indindividuals.wasChosen = True

      return worse_indindividuals


    
    def oneStep(self):
      parents = self._selectParents(int(len(self.population)*2/3))

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

    def _generateChildrens(self,parents):
      childrens = list()
     
      i = 0
      while i < len(parents) -1 :
        child_1 ,child_2 = self._Crossover(parents[i],parents[i+1] )     
        childrens.extend([self._Mutate(child_1),self._Mutate(child_2)])
        i +=2
        
      
      return childrens
    

    def _replace(self,childrens):
      

      self.population.extend(childrens)
      
      worse_individuals_list = list()

      for i in range(len(childrens)):
       worse_individuals_list.append(self._getWorseIndividuals(self.population))
      
      for worse in worse_individuals_list:
        self.population.remove(worse)
     
      import time

    

     

    def _Mutate(self, children):
      
      if np.random.uniform(0,1) < self._mutation_rate:
          self._mutating(children)
      
      return children
      
      
    def _Crossover(self,father,mother):
      increment = int(father.chromosome.size /5)
      if increment == 0:
         increment = int(father.chromosome.size /2)


      end_point = increment
      child_1_chromosome = np.zeros(shape=father.chromosome.size,dtype=int)

      child_2_chromosome = np.zeros(shape=father.chromosome.size,dtype=int)

      switch = True

      for i in range(father.chromosome.size):
          if switch:
            child_1_chromosome[i] = father.chromosome[i]
            child_2_chromosome[i] = mother.chromosome[i]
          else:
            child_1_chromosome[i] = mother.chromosome[i]
            child_2_chromosome[i] = father.chromosome[i]
          
          if i +1 == end_point:
            end_point +=increment
            switch = not switch

      return Individuals.numpy(child_1_chromosome) , Individuals.numpy(child_2_chromosome)

    def _mutating(self, child):
      for i in range(int(child.chromosome.size/5 +1)):
        child.chromosome[ np.random.randint(0,child.chromosome.size) ] = np.random.randint(0,6)
      
    