# -*- coding: utf-8 -*-
import pandas as pd
import scipy.interpolate # package d'interpolation
import matplotlib.pyplot as plt


# 
df = pd.read_excel('ASTMed.xls')
df['lambda']=df['lambda']/1000 # convert to micrometers
df['global']=df['global']*1000 # convert to W/m2/micrometer

# measured data
x = df['lambda'].values
y = df['global'].values
# create the interpolation function
fc_interp = scipy.interpolate.interp1d(x, y)
interpolations= fc_interp(df['lambda'].values)

#plot
fig, ax1 = plt.subplots()
color2,color1= 'gold','yellow'
ax1.set_xlabel(r'$\lambda\,\,[\mu m]$')
ax1.set_ylabel(r'$M^0_\lambda \,\,[W/(m^2.\mu m)]$')

ax1.grid('on', which='major', axis='x',zorder=1)
ax1.grid('on', which='major', axis='y',zorder=1)
ax1.grid(color='grey', linestyle='-.', linewidth=0.25, alpha=0.5)
ax1.set_yscale('symlog')
ax1.set_xscale('log')

ax1.plot(df['lambda'].values, interpolations, color=color1, label='interpolated')
ax1.fill_between(df['lambda'].values, df['global'].values,zorder=2,alpha=0.2,color=color2,label='data')
plt.legend()
plt.tight_layout()
