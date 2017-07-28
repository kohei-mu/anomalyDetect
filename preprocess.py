# -*- coding: utf-8 -*-
#/usr/bin/env python

"""
Created on Fri Jul 21 16:11:58 2017

@author: muramatsu
"""

import sys
import argparse
import numpy as np
import pandas as pd
from datetime import datetime


parser = argparse.ArgumentParser(description="help messages")
group1 = parser.add_argument_group('Main options')
group2 = parser.add_argument_group('additional options')
group1.add_argument("-freq", dest="freq", default="5T", type=str, help="time frequency of data")
group1.add_argument("-periods", dest="prd", default=288, type=int, help="periods of data(data points)")
group1.add_argument("-anomaNum", dest="amN", default=10, type=int, help="anomaly points")
group1.add_argument("-anomaDirect", dest="amD", choices=["pos","neg"], default="pos", type=str, help="anomaly direction")
group1.add_argument("-resFreq", dest="rsF", default="5T", type=str, help="resampling frequency")

group2.add_argument("-resHow", dest="rsH", type=str, default="mean", help="how to resampling")
group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
args=parser.parse_args()


def plot_func(df):
    df.plot()
    
def make_data(freq,periods):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx=pd.date_range(now,freq=freq,periods=periods)
    x = np.linspace(0, 100, num=periods)
    np.random.seed(1234)
    pi2 = 2.*np.pi
    value = 1.0*np.sin(0.1*pi2*x) + 1.0*np.cos(1.*pi2*x) + 0.5*np.random.randn(x.size)
    
    df=pd.DataFrame({"val":value},index=idx)
    return df
    
#df= make_data("5T",288)
#plot_func(df)

def make_anomaly(df, periods, num, direction):
    start = np.random.randint(periods)
    end = start + num
    print df.iloc[start], df.iloc[end]
    if direction == "pos":
        df["val"].iloc[start:end] = float(df.max()) * 10
    elif direction == "neg":
        if float(df.min()) < 0:
            df["val"].iloc[start:end] = float(df.min()) * 10
        else:
            df["val"].iloc[start:end] = float(df.min()) / 10
    return df
#df = make_anomaly(df, 288, 20, "neg")
#plot_func(df)
    
def resample_time(df, freq, how="mean"):
    if how == "last":
        df = df.resample(freq).last()
    elif how == "sum":
        df = df.resample(freq).sum()
    else:#mean
        df = df.resample(freq).mean()
        
    return df
#df=resample_time(df,"10T","mean")
#plot_func(df)

def missing_value(df, how="interpolate"):
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

