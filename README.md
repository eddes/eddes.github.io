# eddes.github.io

A few tools and methods gathered along the way that might prove to be useful for others.
On the agenda: 

- [x] data interpolation
- [x] function integration
- [ ] integration of interpolated data (yes.)
- [ ]  equation solving


# Data interpolation

In this section, we will use the solar spectrum data provided by the NREL called [ASTM AM 1.5](https://www.nrel.gov/grid/solar-resource/spectra-am1.5.html) and corresponding to ground level solar radiation, including the absorption of radiation by gases in the atmosphere.

The aim is to create an interpolation function in order to obtain the values at different abscissa <scipy.integrate>.
The main features of the code are here, pretty much straightforward with the comments:

```python
import pandas as pd #for reading the xls file
import scipy.interpolate # interpolation package 

# let us read the file
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
```

That'is about it, the rest is plotting!
You can [get the data](https://github.com/eddes/eddes.github.io/blob/main/ASTMed.xls) in .xls file format and the [code here](https://github.com/eddes/eddes.github.io/blob/main/interpolate_ASTM.py)

![Interpolated and measured data](/interp.png)


# Compute a numerical integral 

Similarly to the previous example, let us now compute the black body radiation emitted by the sun over its spectrum.

```python
# the 
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
# ... indeed the energy of the black-body spectrum is comprised between 0.5 and 5 lambda_max
E_sun= integrate.quad(lambda x: black_body_radiation(x,Tsun), 0.1*lambda_m, 10*lambda_m)[0]
print("radiation of the black body", E_sun, [W])
```

![Integrated black body spectrum](/Mk0.png)

# Combine: Integrate your interpolated data

[under construction]

# Solve equations

[under construction]


## One unknown

## n unknown

