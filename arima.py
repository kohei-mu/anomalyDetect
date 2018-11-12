# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 09:33:50 2018

@author: muramatsu
"""

import numpy as np
from statsmodels.tsa import arima_model
from statsmodels.tsa import stattools
from statsmodels.tsa import statespace
import matplotlib.pyplot as plt
import pandas as pd


df =  pd.read_csv("test.csv", header=None, index_col=0)

learning_start_date = "2017-12-02 04:40:00"
learning_finish_date = "2018-02-24 09:30:00"
forecast_period = 1000
confidence_interval = [(100-int(i))/100 for i in "75,95".split(",")]

train = np.array(df.loc[learning_start_date:learning_finish_date,1])

import time
##############################################
start = time.time()
results=arima_model.ARIMA(train,order = [2,2,2]).fit(maxiter=25,start_ar_lags=2)
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


outdf = pd.DataFrame()
cnt = 0
for i in confidence_interval:
    ret = results.forecast(steps=forecast_period, alpha=i)

    ci_lo = np.array([j[0] for j in ret[2]])
    ci_hi = np.array([j[1] for j in ret[2]])
    ci = int(100 - (i * 100))
    
    if cnt == 0:
        pre = ret[0]
        tmpdf = pd.DataFrame({"pre":pre,"lo"+str(ci):ci_lo,"hi"+str(ci):ci_hi})
    else:
        tmpdf = pd.DataFrame({"lo"+str(ci):ci_lo,"hi"+str(ci):ci_hi})
        
    outdf = pd.concat([tmpdf, outdf], axis=1)    
    cnt += 1

"""
plt.figure(figsize=(13, 7))
for h in outdf.columns:
    print(h)
    plt.plot(outdf[h], label=str(h))
plt.legend(loc='best',fontsize=18)
"""

origin = np.array(df.iloc[:,0])
a=np.array(outdf["pre"])
predicted=np.concatenate([train,a],axis=0)
lo = np.array(outdf["lo95"])
ci_lo = np.concatenate([train,lo],axis=0)
hi = np.array(outdf["hi95"])
ci_hi = np.concatenate([train,hi],axis=0)

lo2 = np.array(outdf["lo75"])
ci_lo2 = np.concatenate([train,lo2],axis=0)
hi2 = np.array(outdf["hi75"])
ci_hi2 = np.concatenate([train,hi2],axis=0)

plt.figure(figsize=(13, 7))
plt.plot(origin, label="original")
plt.plot(predicted, label="predicted")
plt.plot(ci_lo, label="lo95")
plt.plot(ci_hi, label="hi95")
plt.plot(ci_lo2, label="lo75")
plt.plot(ci_hi2, label="hi75")
plt.legend(loc='best',fontsize=18)

################################

"""
outdf = pd.DataFrame()
ret = results.forecast(steps=forecast_period, alpha=0.05)
pre = ret[0]
ci_lo = np.array([i[0] for i in ret[2]])
ci_hi = np.array([i[1] for i in ret[2]])
outdf = pd.DataFrame({"pre":pre,"lo":ci_lo,"hi":ci_hi})

for h in outdf.columns:
    print(h)
    plt.plot(outdf[h], label=str(h))
plt.legend()
"""

################################


