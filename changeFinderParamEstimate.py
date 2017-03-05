# -*- coding: utf-
import matplotlib.pyplot as plt
import changefinder
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as stt
from skopt import gp_minimize

df = pd.read_csv("indices_I101.csv",header=None)[1]
tmp =  np.array(df)

pcf = stt.pacf(tmp)
lag = np.argsort(np.absolute(pcf))[::-1][1]
def func(params):
    r,smooth = params
    cf = changefinder.ChangeFinder(r=r, order=lag, smooth=smooth)
    ret = []
    for i in tmp:
        score = cf.update(i)
        ret.append(score)
    return np.var(ret)
    
dimensions  = [(0.01, 0.3),                          
          (3,50),   
]     

res_gp = gp_minimize(func, dimensions, n_calls=100, random_state=0)
"Best score=%.4f" % res_gp.fun


