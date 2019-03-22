import numpy as np


class AtomicState:

    def __init__(self, size_tensor=1, rand_value_max=1, rand_value_min=0, type_tensor=None):
        if type_tensor is int:
            self.__features_tensor = np.random.randint(rand_value_min, rand_value_max, size_tensor)
        elif type_tensor is float:
            self.__features_tensor = np.random.rand(size_tensor) * (rand_value_max - rand_value_min) + rand_value_min
        elif type_tensor is None:
            self.__features_tensor = None
        else:
            raise NotImplementedError
        pass

    def getSize(self):
        return self.__features_tensor.size

    def getTensor(self):
        return self.__features_tensor

    @staticmethod
    def numpy(array):
        if type(array) is np.ndarray:
            i = AtomicState()
            i.__features_tensor = array
            return i
        else:
            raise NotImplementedError
