# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import fsolve

# view factors for opposite and adjacent faces in a cube
Fadj, Fopp=0.200044, 0.199824
# view factors matrix
Fij=np.zeros((6,6))
# fill the matrix
for i in range(6):
    for j in range(6):
        # adjacent faces
        if not i==j:
            Fij[i,j]=Fadj
        # opposed faces 0-5 / 1-2 / 3-4
        for z in [(0,5), (1,2), (3,4)]:
            a,b=z
            if (i==a and j==b) or (i==b) and (j==a):
                Fij[i,j]=Fopp

def fc_radiosity(J, T, Fij):
    sigma,epsilon = 5.67*1e-8, 0.9
    return -J + sigma*epsilon*T**4 + (1-epsilon)*np.dot(Fij,J)

# the faces are at +10C...
T=np.ones(6)*(10)
# ... the bottow at -10C
T[0]=-10
# convert the array to Kelvin
T=T+273.15

# initial values for Ji
J_init=np.ones(6)*100
# solve for Ji
J=fsolve(fc_radiosity, J_init, args=(T, Fij))
print("Radiosities [W/m2]", J)

#total incident radiation per face
E=np.dot(Fij,J)
print("Total radiation ", E)

# compute the fictitious radiant temperature for each face
sigma= 5.67*1e-8
Tr=(E/sigma)**0.25
print("Radiant temperatures ", Tr-273.15)