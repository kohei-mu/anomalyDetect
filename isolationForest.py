# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:04:16 2017

@author: kohei-mu
"""

from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import time
import seaborn as sns

rng = np.random.RandomState(42)
data = load_iris()

x=data.data
y=data.target
x_outliers = rng.uniform(low=-4, high=4, size=(x.shape[0], x.shape[1]))

x_train, x_test, y_train, y_test = train_test_split( x, y, test_size=0.2, random_state=0)


#n_estimators : int, optional (default=100)
#max_samples : int or float, optional (default=”auto”)
#contamination : float in (0., 0.5), optional (default=0.1)
#max_features : int or float, optional (default=1.0)
#bootstrap : boolean, optional (default=False)

for param in [0.001,  0.005, 0.1,  0.5]:
    clf = IsolationForest(max_features=1.0,
                          bootstrap=False,
                          contamination=param,
                          n_estimators=100,
                          max_samples='auto',
                          random_state=None,
                          verbose=0)

    start = time.time()
    tp_list=[]
    tn_list=[]
    for i in range(100):
        clf.fit(x_train)
        y_pred_train = clf.predict(x_train)
        y_pred_test = clf.predict(x_test)
        y_pred_outliers = clf.predict(x_outliers)
        
        #print(y_pred_test)
        j=sum([i==1  for i in y_pred_test])
        tp=float(j)/len(y_pred_test)
        tp_list.append(tp)
        
        #print(y_pred_outliers)
        k=sum([i==-1  for i in y_pred_outliers])    
        tn=float(k)/len(y_pred_outliers)
        tn_list.append(tn)
    elapsed_time = time.time() - start
    
    print("test param : " + str(param))
    print("average tp : " + str(np.mean(tp_list)))
    print("average tn : " + str(np.mean(tn_list)))
    print ("elapsed_time : {0}".format(elapsed_time) + "[sec]")
    print("\n")
    
    

#######################

for p in [0.5, 0.1,0.001,0.0001]:
    clf = IsolationForest(max_features=1.0,
                              bootstrap=False,
                              contamination=p,
                              n_estimators=100,
                              max_samples='auto',
                              random_state=None,
                              verbose=0)
    clf.fit(x_train)
    train_score = clf.decision_function(x_train)
    y_pred_train = clf.predict(x_train)
    
    
#    fig = plt.figure()
#    plt.plot(x_train)
#    fig = plt.figure()
#    plt.plot(train_score)
    fig = plt.figure()
    sns.distplot(train_score)




