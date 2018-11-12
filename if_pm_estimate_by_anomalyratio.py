# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 21:33:29 2017

@author: kohei-mu
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from skopt import gp_minimize
#from skopt.plots import plot_convergence

_df = pd.read_csv("test.csv")
df = pd.concat(_df["a"],_df["b"],_df["c"],_df["d"]],axis=1)


col_num = len(df.iloc[1,])
tmp =  np.array(df).reshape(-col_num , col_num) #sk-learnの入力はnumpy.arrayのため変換

tr = tmp[0:3601]
te = tmp[3601:]

#function to calculate anomaly
def isolation(n_estimators, contamination, bootstrap):
    clf =IsolationForest(n_estimators=n_estimators,contamination=contamination,bootstrap=bootstrap)
    clf.fit(tr)    
    score = clf.decision_function(te)
    return score
    
#function to optimize
def func(params):
    n_estimators, contamination, bootstrap  =params
    ret = isolation(n_estimators, contamination, bootstrap)
    score = abs(ret)
    
    anomalies = sum(score[307:314]) + sum(score[407:415]) +  sum(score[507:512]) + sum(score[607:612]) 
    normals = sum(score[0:307]) + sum(score[314:407]) + sum(score[415:507]) + sum(score[512:607]) + sum(score[612:])
    
    ratio = float(-anomalies / normals)
    return ratio

#parameter bounds
dimensions  = [(100, 200),   
          (0.000001,0.001),
          (True, False)]

#n_estimators, contamination, bootstrap

#minimize variance of change score
if_res_gp = gp_minimize(func, dimensions, n_calls=300, random_state=0,n_random_starts=50)

func_return = isolation(n_estimators=if_res_gp.x[0], contamination=if_res_gp.x[1], bootstrap=if_res_gp.x[2])

_clf=IsolationForest(n_estimators=if_res_gp.x[0], contamination=if_res_gp.x[1], bootstrap=if_res_gp.x[2])
_clf.fit(te)    
ans = _clf.predict(te)

#plot result
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111)
ax.plot(te)
xIndex=np.where(ans==-1)[0]
yIndex=te[xIndex]
plt.plot(xIndex, yIndex, 'o',color="r")
plt.show()


fig = plt.figure(figsize=(12, 8))
plt.plot(func_return)
fig = plt.figure(figsize=(12, 8))
plt.plot(te)




