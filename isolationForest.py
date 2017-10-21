# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:04:16 2017

@author: kohei-mu
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import seaborn as sns
from sklearn import datasets
from sklearn.model_selection import GridSearchCV



datasets=datasets.load_iris()
features = datasets.data
targets = datasets.target

clf = IsolationForest(max_features=1.0,
                      bootstrap=False,
                      contamination=0.001,
                      n_estimators=100,
                      max_samples='auto',
                      random_state=None,
                      verbose=0)

params = {
        'contamination': np.arange(0.0005,0.001,0.0001),
        'n_estimators':np.arange(50,100,10),
        'bootstrap':[True, False]
    }

g = GridSearchCV(
    clf, 
    params,
    cv=3, 
    scoring='accuracy',
    n_jobs=10,
    refit=True)
g.fit(features, targets)

print(g.best_params_)
print(g.best_score_)

score = g.decision_function(features)

fig = plt.figure()
plt.plot(features,label="raw data")
plt.legend()

fig = plt.figure()
plt.plot(score,label="best score")
plt.legend()



#######################




for p in [10,50,100,200,300]:
    clf = IsolationForest(max_features=1.0,
                              bootstrap=False,
                              contamination=0.001,
                              n_estimators=p,
                              max_samples='auto',
                              random_state=None,
                              verbose=0)
    clf.fit(features)
    train_score = clf.decision_function(features)
    y_pred_train = clf.predict(features)
    
#    fig = plt.figure()
#    plt.plot(x_train)

    fig = plt.figure()
    plt.plot(train_score,label=str(p))
    plt.legend()
    
    fig = plt.figure()
    sns.distplot(train_score,label=str(p))
    plt.legend()













