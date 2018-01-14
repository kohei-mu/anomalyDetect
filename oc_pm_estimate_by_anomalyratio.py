# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 21:33:29 2017

@author: kohei-mu
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import svm
from skopt import gp_minimize
from skopt.plots import plot_convergence

df = pd.read_csv("C:/Users/kohei-mu/Documents/indices_I101.csv").iloc[:,1:]
tmp =  np.array(df).reshape(-4 , 4) #sk-learnの入力はnumpy.arrayのため変換
#2メトリクスの場合→tmp =  np.array(df).reshape(-2 , 2)
#3メトリクスの場合→tmp =  np.array(df).reshape(-3 , 3)

#function to calculate anomaly
def oneClass(nu,gamma):
    clf = svm.OneClassSVM(nu=nu,kernel="rbf",gamma=gamma)
    clf.fit(tmp)    
    score = clf.decision_function(tmp)
    return score
    
#function to optimize
def func(params):
    nu, gamma =params
    ret = oneClass(nu,gamma)
    score = abs(ret)
    anomalies = sum(score[229:232]) + sum(score[238:242])
    normals = sum(score[0:229]) + sum(score[232:238]) + sum(score[242:])
    ratio = float(anomalies / normals)
    return ratio

#parameter bounds
dimensions  = [(0.000001, 0.01),   
          (0.00000000001,0.01)]     

#minimize variance of change score
res_gp = gp_minimize(func, dimensions, n_calls=150, random_state=0,n_random_starts=50)

func_return = oneClass(res_gp.x[0], res_gp.x[1])
#print(float(len(np.where(func_return==-1)[0])) / len(func_return))


_clf = svm.OneClassSVM(nu=res_gp.x[0],kernel="rbf",gamma=res_gp.x[1])
_clf.fit(tmp)    
ans = _clf.predict(tmp)

retPan=pd.DataFrame(ans)
result=pd.concat([df, retPan], axis=1)

#plot result
fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111)
ax.plot(tmp)
xIndex=np.where(ans==-1)[0]
yIndex=tmp[xIndex]
plt.plot(xIndex, yIndex, 'o',color="r")
plt.show()


fig = plt.figure(figsize=(8, 5))
plt.plot(func_return)





