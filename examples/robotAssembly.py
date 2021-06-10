from TensegrityPY import TensegrityRobot
import numpy as np
from scipy.optimize import minimize

n = 12

"""Cables Configuration"""
cables = np.zeros((n,n))
cables[0][4] = 1
cables[0][5] = 1
cables[0][8] = 1
cables[0][10] = 1

cables[2][4] = 1
cables[2][5] = 1
cables[2][9] = 1
cables[2][11] = 1

cables[1][6] = 1
cables[1][7] = 1
cables[1][8] = 1
cables[1][10] = 1

cables[3][6] = 1
cables[3][7] = 1
cables[3][9] = 1
cables[3][11] = 1


cables[6][8] = 1
cables[6][9] = 1

cables[4][8] = 1
cables[4][9] = 1

cables[7][10] = 1
cables[7][11] = 1

cables[5][10] = 1
cables[5][11] = 1


"""radiusods Configuration"""
rods = np.zeros((n,n))

rods[0][1] = 1
rods[2][3] = 1
rods[4][5] = 1
rods[6][7] = 1
rods[8][9] = 1
rods[10][11] = 1


cables = cables + cables.T
rods = rods + rods.T
connectivity = rods + cables
active_nodes = np.arange(12)

l_cables = cables * 0.25
l_rods = rods * 0.5
rest_lengths = l_cables + l_rods

mu_cables = cables * 10
mu_rods = rods * 100
stiffness_coef = mu_cables + mu_rods

nodes_position1 = [[-0.5, -0.5,  0.5, 0.5],
                   [0, 0, 0, 0],
                   [-1, 1, -1, 1]]
                
nodes_position2 = [[0, 0, 0, 0],
                   [-1, 1, -1, 1],
                   [-0.5, -0.5, 0.5, 0.5]]
                
nodes_position3 = [[-1, 1, -1, 1],
                   [-0.5, -0.5, 0.5, 0.5],
                   [0, 0, 0, 0]]     

nodes_position  = np.hstack((nodes_position1, nodes_position2, nodes_position3)).T*0.5

robot = TensegrityRobot(cables, rods, rest_lengths, stiffness_coef, nodes_position, active_nodes)

next_step = minimize(robot.getPotentialEnergy, robot.nodes_position[robot.active_nodes]).x

next_step = np.reshape(next_step, (3, n))

print("\nNext stable position of the robot:\n")
for i in range(next_step.shape[1]):
    print("Node {}: ".format(i)+str(next_step[:,i]))

robot.nodes_position = next_step.T
robot.draw()