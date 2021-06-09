import numpy as np

class TensegrityRobot:
    def __init__(self, cables, rods, rest_lengths, stiffness_coef, nodes_position, active_nodes):
        if np.allclose(np.triu(cables),np.tril(cables).T) and cables.max()<=1:
            self.cables = cables
        else:
            raise ValueError("Cable matrix is not symmmetric")
        
        if np.allclose(np.triu(rods),np.tril(rods).T) and rods.max()<=1:
            self.rods = rods
        else:
            raise ValueError("Rod matrix is not symmmetric")
        
        self.connectivity = cables+rods

        if type(active_nodes) == None:
            self.active_nodes = np.arange(rods.shape[0]).T
        else:
            self.active_nodes = active_nodes


        self.rest_lengths = rest_lengths
        self.stiffness_coef = stiffness_coef
        self.nodes_position = nodes_position
    
    def getPotentialEnergy(self,nodes_position):
        """Calculation of potential energy"""
        P = 0
        for i in range(len(self.connectivity)):
            for j in range(self.connectivity.shape[1]):
                if self.connectivity[i][j] == 1:
                    ri_rj = nodes_position[i] - nodes_position[j]
                    P = P + (self.stiffness_coef[i][j] * (pow((np.linalg.norm(ri_rj) - self.rest_lengths[i][j]),2)))
        return P
        
    
