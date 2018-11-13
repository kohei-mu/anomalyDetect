# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import changefinder
import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as stt
from skopt import gp_minimize
from skopt.plots import plot_convergence
import seaborn as sns
import math

train_data = np.array(pd.read_csv("toy.csv")["val0"])

pcf = stt.pacf(train_data)
plt.bar(range(len(pcf)), pcf, width = 0.3)
plt.show()
lag = np.argsort(np.absolute(pcf))[::-1][1]

#function to calculate change score
def scoreCalculate(r, smooth):
    cf = changefinder.ChangeFinder(r=r, order=lag, smooth=smooth)
    ret = []
    for i in train_data:
        score = math.exp(cf.update(i))
        ret.append(score)
    return ret
    
#function to optimize
def func(params):
    r, smooth = params
    return np.var(scoreCalculate(r, smooth))

#parameter bounds
dimensions  = [(0.01, 0.1),
            (3,50),
]     

#minimize variance of change score
res_gp = gp_minimize(func, dimensions, n_calls=200, random_state=0)
print(res_gp.x)

#change score with best param
score = scoreCalculate(res_gp.x[0], res_gp.x[1])

#plot result
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111)
ax.plot(score, label="anomaly score")
ax2 = ax.twinx()
ax2.plot(train_data, 'r', label="original data")
plt.legend(loc='best', fontsize=18)
plt.title("anomaly detection result by change finder")
plt.show()


