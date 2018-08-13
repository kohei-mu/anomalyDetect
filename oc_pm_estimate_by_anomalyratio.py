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
#from skopt.plots import plot_convergence

#df = pd.read_csv("C:/Users/muramatsu/Documents/data/qt/case5/n7/n7_sim_all_processed.csv").iloc[:,1:]
#df = pd.read_csv("C:/Users/muramatsu/Documents/data/qt/case5/n7/n7_sim_all_processed_long_2w.csv").iloc[:,1:]
#df = pd.read_csv("C:/Users/muramatsu/Documents/data/qt/case5/n7/n7_sim_all_processed_long_4m.csv").iloc[:,1:]

#case2 n_ca 2w fixed
#_df = pd.read_csv("C:/Users/muramatsu/Documents/data/qt/qt20171208/case2/csv/impulse_input/anomalyPoint2/n_ca_fixed/n-cadns011_processed_fixed_long_2w_2.csv")
#df = pd.concat([_df["ucdavis3"], _df["ucdavis5"], _df["ucdavis7"],_df["ucdavis12"], _df["netIfOutEth1Bytes"]],axis=1)


#case2 n_ca 2w fixed
_df = pd.read_csv("C:/Users/muramatsu/Documents/data/qt/case2_20180126/n_ca_long_2w.csv")
df = pd.concat([_df["ucdavis3"],_df["ucdavis5"],_df["ucdavis7"],_df["systemCpuUtilCounterAll"]],axis=1)





col_num = len(df.iloc[1,])
tmp =  np.array(df).reshape(-col_num , col_num) #sk-learnの入力はnumpy.arrayのため変換
#2メトリクスの場合→tmp =  np.array(df).reshape(-2 , 2)
#3メトリクスの場合→tmp =  np.array(df).reshape(-3 , 3)

#n7 default
#tr = tmp[0:1751]
#te = tmp[1751:]

#n7 2w
#tr = tmp[0:3501]
#te = tmp[3501:]

#case2 n_ca default
#tr = tmp[0:1201]
#te = tmp[1201:]


#case2 n_ca 2w
#tr = tmp[0:3601]
#te = tmp[3601:]

#case2 n_ca 1m
#tr = tmp[0:8405]
#te = tmp[8405:]


#case2 n_co 2w
#tr = tmp[0:3602]
#te = tmp[3602:]

#case2 n_co 1m
#tr = tmp[0:8406]
#te = tmp[8406:]

#case2 n_ca 2w fixed
#tr = tmp[0:3601]
#te = tmp[3601:]

#n_ca 2w
tr = tmp[0:3601]
te = tmp[3601:]

#function to calculate anomaly
def oneClass(nu,gamma):
    clf = svm.OneClassSVM(nu=nu,kernel="rbf",gamma=gamma)
    clf.fit(tr)    
    score = clf.decision_function(te)
    return score
    
#function to optimize
def func(params):
    nu, gamma  =params
    ret = oneClass(nu,gamma)
    score = abs(ret)
    #score = [x**2 for x in ret]
    #score = ret
    
    #n7 default
    #anomalies = sum(score[88:95]) + sum(score[172:180]) +  sum(score[220:225]) + sum(score[376:381]) 
    #normals = sum(score[0:88]) + sum(score[95:172]) + sum(score[180:220]) + sum(score[225:376]) + sum(score[381:])  
    
    #n7 2w
    #anomalies = sum(score[89:96]) + sum(score[173:181]) +  sum(score[221:226]) + sum(score[377:382]) 
    #normals = sum(score[0:89]) + sum(score[96:173]) + sum(score[181:221]) + sum(score[226:377]) + sum(score[382:]) 

    
    #case2 n_ca 2w
    #anomalies = sum(score[309:315]) + sum(score[409:417]) +  sum(score[509:514]) + sum(score[609:614]) 
    #normals = sum(score[0:309]) + sum(score[315:409]) + sum(score[417:509]) + sum(score[514:609]) + sum(score[614:])
    
    
    #case2 n_ca 1m
    #anomalies = sum(score[309:316]) + sum(score[409:417]) +  sum(score[509:514]) + sum(score[609:614]) 
    #normals = sum(score[0:309]) + sum(score[316:409]) + sum(score[417:509]) + sum(score[514:609]) + sum(score[614:])
    
    #case2 n_co 2w
    #anomalies = sum(score[308:315]) + sum(score[408:416]) +  sum(score[508:513]) + sum(score[608:613]) 
    #normals = sum(score[0:308]) + sum(score[315:408]) + sum(score[416:508]) + sum(score[513:608]) + sum(score[613:])
    
     #case2 n_co 1m
    #anomalies = sum(score[308:315]) + sum(score[408:416]) +  sum(score[508:513]) + sum(score[608:613]) 
    #normals = sum(score[0:308]) + sum(score[315:408]) + sum(score[416:508]) + sum(score[513:608]) + sum(score[613:])

    
    #case2 n_ca 2w fixed
    anomalies = sum(score[307:314]) + sum(score[407:415]) +  sum(score[507:512]) + sum(score[607:612]) 
    normals = sum(score[0:307]) + sum(score[314:407]) + sum(score[415:507]) + sum(score[512:607]) + sum(score[612:])
    

    
    
    ratio = float(-anomalies / normals)
    return ratio

#parameter bounds
dimensions  = [(0.000001, 0.00001),   
          (0.00000001,0.1)]

#nu, gamma, kernel,coef0 ,degree    

#minimize variance of change score
oc_res_gp = gp_minimize(func, dimensions, n_calls=100, random_state=0,n_random_starts=1)

func_return = oneClass(oc_res_gp.x[0], oc_res_gp.x[1])
#print(float(len(np.where(func_return==-1)[0])) / len(func_return))


_clf=svm.OneClassSVM(nu=oc_res_gp.x[0],gamma=oc_res_gp.x[1], kernel="rbf")
_clf.fit(te)    
ans = _clf.predict(te)

#retPan=pd.DataFrame(ans)
#result=pd.concat([tmp, retPan], axis=1)

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




