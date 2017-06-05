# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 09:09:50 2017

@author: muramatsu
"""

# -*- coding: utf-
import matplotlib.pyplot as plt
import changefinder
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as stt
from skopt import gp_minimize
from skopt.plots import plot_convergence
import seaborn as sns
import math

#input data
df = pd.read_csv("indices_I101.csv",header=None)[1]
tmp =  np.array(df)

pcf = stt.pacf(tmp)
lag = np.argsort(np.absolute(pcf))[::-1][1]

#function to calculate change score
def scoreCalculate(r,smooth):
    cf = changefinder.ChangeFinder(r=r, order=lag, smooth=smooth)
    ret = []
    for i in tmp:
        score = math.exp(cf.update(i))
        ret.append(score)
    return ret
    
    
#function to optimize
def func(params):
    r,smooth = params
    return np.var(scoreCalculate(r, smooth))

#parameter bounds
dimensions  = [(0.1, 0.5),   
          (3,100),
]     

#minimize variance of change score
res_gp = gp_minimize(func, dimensions, n_calls=10, random_state=0,n_random_starts=10)
print(res_gp.x)

#change score with best param
score = scoreCalculate(res_gp.x[0],res_gp.x[1])

#plot result
fig = plt.figure(figsize=(13, 7))
ax = fig.add_subplot(111)
ax.plot(score)
ax2 = ax.twinx()
ax2.plot(tmp,'r')
plt.show()

#convergence
plot_convergence(res_gp)
#density of change score
sns.distplot(score, hist=False)

#output change score as csv
pd.DataFrame(score).to_csv("score.csv")
