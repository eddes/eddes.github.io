# eddes.github.io

A few tools and methods gathered along the way that might prove to be useful for others.


# Data interpolation

In this section, we will use the solar spectrum data provided by the NREL called [ASTM AM 1.5](https://www.nrel.gov/grid/solar-resource/spectra-am1.5.html) an corresponding to ground level solar radiation, including absorption of radiation by gases in the atmosphere.


```python

import pandas as pd
import scipy.interpolate # package d'interpolation

df = pd.read_excel('ASTMed.xls')
df['lambda']=df['lambda']/1000 # convert to micrometers
df['global']=df['global']*1000 # convert to W/m2/micrometer

# measured data
x = df['lambda'].values
y = df['global'].values
# create the interpolation function
fc_interp = scipy.interpolate.interp1d(x, y)
interpolations= fc_interp(df['lambda'].values)
```

That'is about it!

![Interpolated and measured data](/interp.png)


You can [get the data](https://github.com/eddes/eddes.github.io/blob/main/ASTMed.xls) in .xls file format and the [code here](https://github.com/eddes/eddes.github.io/blob/main/interpolate_ASTM.py)

# Compute a numerical integral 

Similarly to the previous example.

# Combine: Integrate your interpolated data

[under construction]

# Solve equations

[under construction]


## One unknown

## n unknown

