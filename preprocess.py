# -*- coding: utf-8 -*-
#/usr/bin/env python

"""
Created on Fri Jul 21 16:11:58 2017

@author: muramatsu
"""

import argparse
import numpy as np
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.fftpack import fft
from scipy.signal import blackman
import statsmodels.tsa.stattools as stt


parser = argparse.ArgumentParser(description="help messages")
group1 = parser.add_argument_group('Main options')
group2 = parser.add_argument_group('additional options')
group1.add_argument("-freq", dest="freq", default="5T", type=str, help="time frequency of data")
group1.add_argument("-periods", dest="prd", default=288, type=int, help="periods of data(data points)")
group1.add_argument("-anomaNum", dest="amN", default=10, type=int, help="anomaly points")
group1.add_argument("-anomaDirect", dest="amD", choices=["pos","neg"], default="pos", type=str, help="anomaly direction")
group1.add_argument("-resFreq", dest="rsF", default="5T", type=str, help="resampling frequency")
group1.add_argument("-in", dest="in", type=str, help="input csv")
group1.add_argument("-out", dest="out", type=str, help="output csv")
group1.add_argument("-save", dest="save", type=bool, default=False, choices=[True, False], help="save plots")

group2.add_argument("-resHow", dest="rsH", type=str, default="mean", choices=["sum","mean","median","max","min","last","first"],help="how to resampling")
group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
group2.add_argument("-input_header",dest="inH", type=int, default=0, choices=[0,-1], help="input header option")
group2.add_argument("-crosstab",dest="cross", type=bool, default=False, choices=[True, False], help="calculate crosstab")
args=parser.parse_args()

    
def make_data(freq,periods):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx=pd.date_range(now,freq=freq,periods=periods)
    x = np.linspace(0, 100, num=periods)
    np.random.seed(1234)
    pi2 = 2.*np.pi
    value = 1.0*np.sin(0.1*pi2*x) + 1.0*np.cos(1.*pi2*x) + 0.5*np.random.randn(x.size)
    
    value2 = 2.0*np.sin(0.1*pi2*x) + 3.0*np.cos(1.*pi2*x) + 0.6*np.random.randn(x.size)
    
    df=pd.DataFrame({"val":value,"val2":value2},index=idx)
    return df
    
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
    elif how == "first":
        df = df.resample(freq).first()
    elif how == "sum":
        df = df.resample(freq).sum()
    elif how == "median":
        df = df.resample(freq).median()
    elif how == "max":
        df = df.resample(freq).max()
    elif how == "min":
        df = df.resample(freq).min()        
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

#get lags
def slide_window(df, num):
    return df.shift(num)

def file_reader(csv, header=0):
    df=pd.read_csv(csv,header=header)
    if df.isnull().any().sum() > 0:
        df = missing_value(df)
    return df
    
def file_writer(df, out_name):
    df.to_csv(out_name,index_label=["TimeStamp"])

def index_convert(df):
    index = df.index
    k=[]
    for i in index:
        j = "T".join(str(i).split(" ")) + "+09:00"
        k.append(j)
    df.index = k
    return df


def plot_fig(df, save=False):    
    fig=sns.PairGrid(df, diag_sharey=False)
    fig.map_lower(sns.kdeplot, cmap="Blues_d")
    fig.map_upper(plt.scatter)
    fig.map_diag(sns.distplot)
    if save==True:fig.savefig("pairplot.png")

    #plot jointplot
    if len(df.columns) == 2:
        fig = plt.figure()
        sns.jointplot(x=df.columns.values[0] ,y=df.columns.values[1], data=df);
        if save == True: fig.savefig("joint_plot.png")

    #plot kde joitplot
        fig = plt.figure()
        sns.jointplot(x=df.columns.values[0] ,y=df.columns.values[1] ,kind="kde", data=df);
        if save == True: fig.savefig("joint_kde_plot.png")
        
    #calculate acf, pcf
    acf, pcf = calc_pacf(df)
    ma = calc_ma(df)
    
    #calcularw return
    ret = calc_return(df)
    
    for i in range(len(df.columns)):
        #plot distribution
        fig = plt.figure()
        sns.distplot(df.iloc[:,i])
        if save==True:fig.savefig("dist_plot"+str(i)+".png")

        #plot series
        fig = plt.figure()
        df.iloc[:,i].plot()
        #plot moving average
        ma[i].plot(c='r')
        if save==True:fig.savefig("series_plot"+str(i)+".png")


        #plot acf
        fig = plt.figure()
        plt.bar(range(len(acf[i])), acf[i], width = 0.3)
        if save==True:fig.savefig("acf_plot"+str(i)+".png")

        #plot pcf
        fig = plt.figure()
        plt.bar(range(len(pcf[i])), pcf[i], width = 0.3)
        if save==True:fig.savefig("pcf_plot"+str(i)+".png")
        
        #plot fft
        fig = plt.figure()
        f = calc_fft(df.iloc[:,i])
        plt.plot(f[1], f[0])
        if save==True:fig.savefig("fft_plot"+str(i)+".png")
        
        #plot return value_i - value_i2
        fig = plt.figure()
        ret[i].plot()
        if save==True:fig.savefig("return_plot"+str(i)+".png")
        

def calc_return(df):
    rets = []
    for i in  range(len(df.columns)):
        ret = df.iloc[:,i].pct_change().dropna()
        rets.append(ret)
    
    return rets

def calc_pacf(df):
    acfs = []
    pcfs = []
    for i in range(len(df.columns)):
        acf = stt.acf(df.iloc[:,i])
        acfs.append(acf)
        
        pcf = stt.pacf(df.iloc[:,i])
        pcfs.append(pcf)
    
    return acfs, pcfs

def calc_ma(df):
    mas = []
    for i in range(len(df.columns)):
        ma = pd.Series.rolling(df.iloc[:,i], window=3, center=True).mean()
        mas.append(ma)
    return mas

def data_understand(df, cross=False, r="row", c="col"):
    print df.describe()
    
    if cross == True:
        crosstab = pd.pivot_table(rows=r, cols=c, aggfunc=[len])
        print crosstab

def calc_fft(df):
    # Number of sample points
    N = len(df)
    # sample spacing
    T = 1.0 / N * 1.5
   # x = np.linspace(0.0, N*T, N)
   ##window function
    w = blackman(N)
    y = df
    yf = 2.0/N * np.abs(fft(y*w)[0:N//2])
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    return yf, xf


df=make_data("5t",288)



