# eddes.github.io

A few tools and methods gathered along the way that might prove to be useful for people dealing with measured data, equations or teaching.
On the agenda: 

- [x]  data interpolation
- [x]  data resampling
- [x]  function integration
- [ ]  integration of interpolated data (yes.)
- [ ]  equation solving


# Data interpolation

In this section, we will use the solar spectrum data provided by the NREL called [ASTM AM 1.5](https://www.nrel.gov/grid/solar-resource/spectra-am1.5.html) and corresponding to ground level solar radiation, including the absorption of radiation by gases in the atmosphere.

The aim is to create an interpolation function in order to obtain the values at different abscissa <scipy.integrate>.
The main features of the code are here, pretty much straightforward with the comments:

```python
import pandas as pd # pandas will help reading the xls file
import scipy.interpolate # interpolation package 

# let us read the radiation data 
df = pd.read_excel('ASTMed.xls')
df['lambda']=df['lambda']/1000 # convert to micrometers
df['global']=df['global']*1000 # convert to W/m2/micrometer

# measured data
x = df['lambda'].values
y = df['global'].values
# create the interpolation function
fc_interp = scipy.interpolate.interp1d(x, y)
# compute the interpolated values (in this cas the exact ones)
interpolations= fc_interp(df['lambda'].values)

print("Radiation at 0.55 micrometers", fc_interp(0.55), 'W/m²/um')
```

That's about it, the rest is plotting!
You can [get the data](https://github.com/eddes/eddes.github.io/blob/main/ASTMed.xls) in .xls file format and the [code here](https://github.com/eddes/eddes.github.io/blob/main/interpolate_ASTM.py)

![Interpolated and measured data](/interp.png)

# Resampling data

It is often useful to resample data in the field of building physics. For instance if you have measured data at 1 hour interval and require a 10 minutes
Using the same procedure as above

```python
import numpy as np # numpy import for convenience

# measured data
x, y = df['lambda'].values, df['global'].values
# create the interpolation function
fc_interp = scipy.interpolate.interp1d(x, y)

#let us define a new interval every 0.5 micrometer
wavelengths=np.arange(min(x),max(x), 0.5)
# get the resampled radiation data
resampled_radiation = fc_interp(wavelengths)
```


# Numerical integration

Similarly to the previous example, let us now compute the black body radiation emitted by the sun over its spectrum.

```python
# Planck's emission law depending on wavelength x [micrometers] and temperature T [K]
def black_body_radiation(x,T):
	#a few constants
	h=6.62*10**(-34)
	k=1.3805*10**(-23)
	c=3*10**8
	C1= 3.74*10**(8) # um**4
	C2=1.43*10**4 # umK
	return C1*x**(-5)/(np.exp(C2/(x*T))-1)*((6.957*10**8)/(149.598*10**9))**2

k = np.arange(0.05, 50, 0.001) # wavelength range in micrometers
Tsun=5800 # K
#now  a little trick using Wien's law: 
lambda_m=2898/Tsun 
# ... indeed most of the energy of the black-body spectrum is comprised 
# between 0.5 and 5 lambda_max, hence no need for a larger integration range
E_sun= integrate.quad(lambda x: black_body_radiation(x,Tsun), 0.5*lambda_m, 5*lambda_m)[0]
print("radiation of the black body", E_sun, [W])
```

![Integrated black body spectrum](/M0k.png)

# Combine: Integrate your interpolated data

[under construction]

# Solve equations

[under construction]


## One unknown

## n unknown

