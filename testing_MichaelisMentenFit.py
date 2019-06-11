# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:20:25 2019

W Le Pang's initial code, found here: https://gist.github.com/wleepang/4680860

Edited by Maddy Scott
"""

import numpy as np
from lmfit import minimize, Parameters

s = np.float_(np.linspace(0,1201,20))
v = np.round(120*s/(171+s) + np.random.uniform(size=20), 2)

def residual(p, x, data):
    vmax = p['vmax'].value
    km = p['km'].value
    model = vmax * x / (km + x)
    return (data - model)

p = Parameters()
p.add('vmax', value=1., min=0.)
p.add('km', value=1., min=0.)

out = minimize(residual, p, args=(s, v))

plot(s, v, 'bo')

ss = np.float_(np.linspace(0,1201, 90))
y = p['vmax'].value * ss / (p['km'].value + ss)
plot(ss, y, 'r-')

