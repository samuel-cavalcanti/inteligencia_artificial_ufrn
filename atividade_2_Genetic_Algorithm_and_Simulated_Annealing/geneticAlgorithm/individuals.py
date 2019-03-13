import numpy as np
class Individuals:
    score =0
    wasChosen = False

  
    def __init__(self, size_chromosome = None,rand_value_max= None,rand_value_min= None,type_value= None):
        if type_value is int:    
             self.chromosome = np.random.randint(rand_value_min,rand_value_max,size_chromosome) 
        elif type_value is float:
            self.chromosome =  (rand_value_max - rand_value_min) * np.random.rand(size_chromosome) + rand_value_min
        elif type_value is None:
            self.chromosome = None
        else:
            raise NotImplementedError
   
    @staticmethod
    def numpy(array):
        
       if type(array) is np.ndarray:
          i  = Individuals()
          i.chromosome = array
          return i
       else:
          raise NotImplementedError

    def save(self, fileName):
        np.save(fileName,self.chromosome)
        pass

    def load(self,fileName):
        self.chromosome=np.load(fileName)