# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:11:58 2017

@author: muramatsu
"""

import numpy as np
import pandas as pd
from datetime import datetime


def make_data(freq,periods):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx=pd.date_range(now,freq=freq,periods=periods)

    x = np.linspace(0, 100, num=periods)
    np.random.seed(1234)
    pi2 = 2.*np.pi
    value = 1.0*np.sin(0.1*pi2*x) + 1.0*np.cos(1.*pi2*x) + 0.5*np.random.randn(x.size)
    
    df = pd.DataFrame({"val":value},index=idx).cumsum()
    return df￼
#df= make_data("5T",288)
#plot_func(df)

def make_anomaly(periods, num, direction):
    start = np.random.randint(periods)
    end = start + num
    if direction == "pos":
        
    elif direction == "neg":
        

def resample_time(df, freq, how="mean"):
    if how == "last":
        df = df.resample(freq).last()
    elif how == "sum":
        df = df.resample(freq).sum()
    else:
        df = df.resample(freq).mean()
        
    return df
#df=resample_time(df,"5T","mean")

def missing_value(df, how):
    #indexer=np.random.randint(4,size=30)==1
    #df.loc[indexer]=np.nan
    if how == "interpolate":
        df=df.interpolate()
    elif how == "drop":
        df=df.dropna()
    else:
        df=df.fillna(df.mean())
        #bfill : backward
        #ffill : forward
    return df
#df = missing_value(df,"interpolate")

def plot_func(df):
    df.plot()


start = np.random.randint(30)
end = start + 10

df.loc[start:end]=0

if direction == "pos":
    
elif direction == "neg":
        


