# -*- coding: utf-8 -*-

import numpy as np
from statsmodels.tsa import arima_model
from statsmodels.tsa import stattools
from statsmodels.tsa import statespace
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("toy.csv", index_col=0)["val1"]

learning_start_date = "2017-10-08 18:34:33"
learning_finish_date = "2017-10-09 18:29:33"
forecast_period = 200
confidence_interval = [(100-int(i))/100 for i in "75,95".split(",")]

train_data = df.loc[learning_start_date:learning_finish_date]
model = arima_model.ARIMA(train_data, order = [2,2,2]).fit(maxiter=100, start_ar_lags=2)

outdf = pd.DataFrame()
cnt = 0
for i in confidence_interval:
    ret = model.forecast(steps=forecast_period, alpha=i)
    ci_lo = np.array([j[0] for j in ret[2]])
    ci_hi = np.array([j[1] for j in ret[2]])
    ci = int(100 - (i * 100))
    
    if cnt == 0:#全ての結果をプロット
        pre = ret[0]
        tmpdf = pd.DataFrame({"pre":pre, "lo"+str(ci):ci_lo, "hi"+str(ci):ci_hi})
    else:#信頼区間のみをプロット
        tmpdf = pd.DataFrame({"lo"+str(ci):ci_lo, "hi"+str(ci):ci_hi})
        
    outdf = pd.concat([tmpdf, outdf], axis=1)    
    cnt += 1

origin = np.array(df)
pre = np.array(outdf["pre"])
predicted = np.concatenate([train_data, pre], axis=0)
lo95 = np.array(outdf["lo95"])
ci_lo95 = np.concatenate([train_data, lo95], axis=0)
hi95 = np.array(outdf["hi95"])
ci_hi95 = np.concatenate([train_data, hi95], axis=0)
lo75 = np.array(outdf["lo75"])
ci_lo75 = np.concatenate([train_data, lo75], axis=0)
hi75 = np.array(outdf["hi75"])
ci_hi75 = np.concatenate([train_data, hi75], axis=0)

plt.figure(figsize=(10, 7))
plt.plot(predicted, label="predicted")
plt.plot(ci_lo95, label="lo95")
plt.plot(ci_hi95, label="hi95")
plt.plot(ci_lo75, label="lo75")
plt.plot(ci_hi75, label="hi75")
plt.plot(origin, label="original")
plt.legend(loc='best', fontsize=18)
plt.title("ARIMA predicted - period: " + str(forecast_period))
plt.show()
