### eddes.github.io

On this page, a few tools and methods gathered along the way.
Might prove to be useful for people dealing with measured data, equations or teaching.


On the agenda:

- [x]  data interpolation
- [x]  data resampling
- [x]  function integration
- [x]  integration of interpolated data (yes.)
- [x]  equation solving
- [ ]  tips & tricks with `pyvista` (depending on the mood!)


## Data interpolation

In this section, we will use the solar spectrum data provided by the NREL called [ASTM AM 1.5](https://www.nrel.gov/grid/solar-resource/spectra-am1.5.html) and corresponding to ground level solar radiation, including the absorption of radiation by gases in the atmosphere.

The aim is to create an interpolation function in order to obtain the values at different abscissa `scipy.integrate`.
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

![Interpolated and measured data](/img/interp.png)

## Resampling data

It is often useful to resample data in the field of building physics. For instance if you have measured data at 1 hour interval and require a 10 minutes interval. No need to worry about creating your own interpolation routine: Using exactly the same procedure as above, you can proceed as follows.

```python
import numpy as np # numpy import for convenience

# measured data
x, y = df['lambda'].values, df['global'].values
# create the interpolation function
fc_interp = scipy.interpolate.interp1d(x, y)

#let us define a new interval every 0.5 micrometer between the bounds
wavelengths=np.arange(min(x),max(x), 0.5)
# get the resampled radiation data
resampled_radiation = fc_interp(wavelengths)
```
![Resampling data](/img/resamp.png)
	
_(looks weird, I know... usually you resample the other way around: with more data!)_
	
## Numerical integration

Life is beautiful since numerical integration was invented (even more since integration was made possible with less than 10 lines of code).
Using the same physical problem as the previous example, let us now compute the black body radiation emitted by the sun over its spectrum.

We will therefore use [Planck's law](https://en.wikipedia.org/wiki/Planck%27s_law) for the black body emission, which forms more than half the code required, as you can see for yourself below.

```python
import scipy.integrate as integrate # import the integration method

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

![Integrated black body spectrum](/img/M0k.png)

## Combine: Integrate your measured data

It is sometimes handy to integrate measured data (e.g. power over time &rarr; energy).
	
Imagine that for some reason, you want to compute the energy comprised in the ASTM solar data of the first example.
You can either do it directly in the .xls file provided, using the [rectangle integration method](https://en.wikipedia.org/wiki/Numerical_integration#Quadrature_rules_based_on_interpolating_functions), or follow the tutorial presented here.
	
You may have noticed that numerical integration requires a function to be integrated (e.g. `black_body_radiation()` in the script above).
Very handily, the interpolation function proposed in the previous section provides `fc_interp()` which allows to determine the value of the function for any abscissa (within the measured abscissa).

```python
import scipy.integrate as integrate #
E_sun= integrate.quad(lambda x: fc_interp(x), min(x), max(x))[0]
print("and the solar energy spectrum contains...", E_sun, " Watts!")
```
	
## Solving equations

Problems are much simpler when computers solve equations or systems of equations for us.
You will find two examples below to kick-start your code.
	
### Computing the wet bulb temperature (one unknown)

The equation of the wet-bulb temperature is defined in function of itself
<img src="https://latex.codecogs.com/svg.latex?\Large&space;T_{wb}= T_a + \frac{p_v-p_{vs}(T_w)}{C_p(p - p_{vs}(T_w)} \times 0.622 \times (L_v - 2.65 T)" title="T_{wb}= T_a + \frac{p_v-p_{vs}(T_w)}{C_p(p - p_{vs}(T_w)} \times 0.622 \times (L_v - 2.65 T)" />

A simple way to solve this (complicated) equation it is to create a function in the form `Twb-f(Twb)=0` and to ask the specialised procedure `fsolve` to do it for us:

```python
import numpy as np # for generic math/array operations
from scipy.optimize import fsolve # queen of solving procedures

# a function for the vapour pressure at saturation pvs(T)
def pvs(T):
	a,b=0.07252,0.0002881
	c,d=0.00000079,611
	return d * np.exp(a*T -b*np.power(T,2) + c*np.power(T,3))

# the function that will allow finding Twb depending on temperature T and vapour pressure pv
def fc_Twb(Twb, T, pv):
	Cp, p, Lv = 1006, 101325, 2400*1e3
	return - Twb +T+ (pv-pvs(Twb))/(Cp*(p-pvs(Twb)))*0.622*(Lv-2.65*T)

# let's define the temperature and vapour pressure conditions
Ta = 40 # air dry bulb temperature
pv=0.3*pvs(Ta) # let us go for 30% relative humidity

# initial guess for the solution
Twb_guess = Ta-10 # usually Twet-bulb is on the left of Tdry

# solving with fsolve (note the first argument is the unknown and the others are given separately)
# compute the wet-bulb temperature:
Twb = fsolve(fc_Twb, Twb_guess, args=(Ta, pv))
print("wet bulb temperature", Twb)

```
### A cool example with _n_ unknowns
	
[under construction]

