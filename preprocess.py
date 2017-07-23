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
    df = pd.DataFrame({"val":np.random.randn(periods)},index=idx).cumsum()
    return df
#df= make_data("3T",50)

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


start = np.random.randint(30)
end = start + 10

df.loc[start:end]=0

if direction == "pos":
    
elif direction == "neg":
        

