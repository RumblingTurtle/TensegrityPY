import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

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
        
        if not np.all(self.connectivity[np.nonzero(self.connectivity)]==1):
            raise ValueError("Connectivity matrix has duplicate entries in rods and cables")

        if type(active_nodes) == None:
            self.active_nodes = np.arange(np.count_nonzero(np.triu(rods))).T
        else:
            self.active_nodes = active_nodes


        self.rest_lengths = rest_lengths
        self.stiffness_coef = stiffness_coef
        self.nodes_position = nodes_position
    
    def getPotentialEnergy(self,nodes_position):
        """Calculation of potential energy"""
        P = 0
        for i in range(len(self.connectivity)):
            for j in range(len(self.connectivity)):
                if self.connectivity[i][j] == 1 and i>=j:
                    ri_rj = nodes_position[i] - nodes_position[j]
                    P = P + (self.stiffness_coef[i][j] * (pow((np.linalg.norm(ri_rj) - self.rest_lengths[i][j]),2)))
        return P
    
    def draw(self):
    
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        def drawCylinder(a,b,radius):
            v = b - a

            mag = np.linalg.norm(v)
            
            v /= mag

            not_v = np.array([1, 0, 0])
            if (v == not_v).all():
                not_v = np.array([0, 1, 0])

            n1 = np.cross(v, not_v)
            n1 /= np.linalg.norm(n1)
            
            n2 = np.cross(v, n1)
            
            t = np.linspace(0, mag, 10)
            theta = np.linspace(0, 2 * np.pi, 10)

            t, theta = np.meshgrid(t, theta)

            X, Y, Z = [a[i] + v[i] * t + radius * np.sin(theta) * n1[i] + radius * np.cos(theta) * n2[i] for i in range(3)]

            ax.plot_surface(X, Y, Z)

        for i in range(len(self.connectivity)):
            for j in range(len(self.connectivity)):
                
                if i>=j:
                    if self.cables[i][j]==1:
                        ax.plot(*zip(self.nodes_position[i],self.nodes_position[j]), color = 'black')

                    if self.rods[i][j]==1:
                        print("Rod")
                        ax.plot(*zip(self.nodes_position[i],self.nodes_position[j]), color = 'red')
                        drawCylinder(self.nodes_position[i],self.nodes_position[j],0.02)
                        
        plt.show()

    
