# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pythermalcomfort.models import set_tmp
from smt.sampling_methods import LHS
from smt.surrogate_models import KRG

# boundaries of the air and radiant temperatures
Tmin,Tmax=10,40 # air temperature
Trmin,Trmax=20,40 # air temperature
xlimits = np.array([[Tmin, Tmax], [Trmin, Trmax]])

#metamodel set up
nb_LHS = 100 # number of evaluations
# type of sampling 
sampling = LHS(xlimits=xlimits, criterion='c')
# sample data set
xt = sampling(nb_LHS)
yt=np.empty([nb_LHS]) # prepare array for filling

# air velocity (m/s) and relative humidity (%)
vair,hum=0.15, 55
for k in range(len(xt)):
	Ta,Tr,v,hum=xt[k,0], xt[k,1], vair, hum # put it in a readable way
	yt[k]=set_tmp(tdb=Ta, tr=Tr, v=v, rh=hum, met=1.2, clo=.5) # evaluate the function

# prepare the metamodel
sm = KRG(theta0=[1e-3], corr='abs_exp')
sm.set_training_values(xt, yt)
sm.train()  # --> this is the costly part

# nom compare with the proper model
num=10 # nb points for the comparison
meta_SET,SET=np.zeros((num,num)),np.zeros((num,num))
tdb=np.linspace(Tmin,Tmax,num)
tr=np.linspace(Trmin,Trmax,num)
dum=np.zeros([1,2])
for i,Tair in enumerate(tdb):
	for j,Trad in enumerate(tr):
		dum[0,0]=Tair
		dum[0,1]=Trad
		meta_SET[i,j]=sm.predict_values(dum)[0]
		SET[i,j]=set_tmp(tdb=Tair, tr=Trad, v=v, rh=hum, met=1.2, clo=.5)

erreur=round(np.mean(abs(meta_SET-SET)),2)

# now plotting
nb_contours=5

# original model
plt.subplot(131)
plt.contour(tdb, tr, SET, nb_contours, colors='black')
plt.pcolormesh(tdb, tr , SET, cmap=plt.get_cmap("RdGy_r"))
plt.title('Original SET')
plt.xlabel(r"$T_{air}$")
plt.xlabel(r"$T_{radiant}$")

# metamodel
plt.subplot(132)
plt.contour(tdb, tr, meta_SET, nb_contours, colors='black')
plt.pcolormesh(tdb, tr, meta_SET, cmap=plt.get_cmap("RdGy_r"))
plt.title('Metamodel SET')
plt.xlabel(r"$T_{air}$")

# difference of both methods
plt.subplot(133)
plt.contourf(tdb, tr, meta_SET-SET, nb_contours,cmap='viridis')
plt.xlabel(r"$T_{air}$")
strerreur=r"$\bar{\varepsilon}= $"+str(erreur)+" [K]"
plt.colorbar()
plt.title(strerreur)
plt.tight_layout()
