import numpy as np

class Track:

    def __init__(self,distance,curvature):

        self.distance = np.array(distance, dtype = float)
        self.curvature = np.array(curvature, dtype=float)

    @classmethod
    def from_csv(cls,filename):

        data = np.loadtxt(filename,delimiter=",",skiprows = 1)

        distance = data[:,0]
        curvature = data[:,1]

        return cls(distance,curvature)