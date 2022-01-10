# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from pythermalcomfort.models import set_tmp
from SALib.plotting.morris import horizontal_bar_plot, covariance_plot
from SALib.analyze import morris
from SALib.sample.morris import sample


# Define the model inputs
problem = {
    'num_vars': 4, # nb variables
    'names': [r'$T_a$', r'$T_r$', 'v', 'RH'], # variables names
    'bounds': [[10,40], # les limites de chacune (borne min/max)
               [10,40],
               [0.1,1],
               [10,90]]
}
# generate samples
N_repetitions=50 # number of repetitions/trajectorie
num_vars=problem['num_vars']
print("Total evaluations ", N_repetitions*(num_vars+1))
# prepare evaluations
param_values= sample(problem, N_evaluations, num_levels=4) # num_levels/(2*(num_levels-1))
Nmax=max(np.shape(param_values)) # values as output

# the call looks like
# set_tmp(tdb=Tair, tr=Trad, v=v, rh=hum, met=1.2, clo=.5)
# so let's create the arrays for metabolic rate and clothing:
array_met=np.ones(len(param_values))*1.2
array_clo=np.ones(len(param_values))*0.5
# ... and stack them to the param_values matrix
param_values_with_metclo=np.hstack([param_values, array_met[:,None],array_clo[:,None]])

# prepare the output array
Y=np.ones((Nmax)) 
# do the function evaluation
for i,p in enumerate(param_values_with_metclo):
	Y[i]= set_tmp(*p)

# Perform analysis (une fois qu'on a tous les resultats dans le vecteur Y)
Si = morris.analyze(problem, param_values, Y, conf_level=0.95,print_to_console=True, num_levels=4)

fig, (ax1, ax2) = plt.subplots(1, 2)
horizontal_bar_plot(ax1, Si,{}, sortby='mu_star', unit=r" (°C SET)")
covariance_plot(ax2, Si, {}, unit=r" (°C SET)")
plt.show()
