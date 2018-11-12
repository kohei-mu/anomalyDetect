# -*- coding: utf-8 -*-
#/usr/bin/env python

"""
Created on Fri Jul 21 16:11:58 2017

@author: kohei-mu
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

#### argparse options ####
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
group2.add_argument("-i_conv",dest="i_convert", type=bool, default=False, choices=[True, False], help="conert timestamp index(yyyy-mm-dd'T'hh:MM:DD+09:00)")
args=parser.parse_args()
########

#make demo data
def make_data(freq,periods, ncol=1):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx = pd.date_range(now,freq=freq,periods=periods)
    x = np.linspace(0, 100, num=periods)
    pi2 = 2.*np.pi    
    valDic = {}
    for i in range(ncol):
        value = np.random.randint(10)*np.sin(0.1*pi2*x) +np.random.randint(10)*np.cos(1.*pi2*x) +  np.random.rand(1)*np.random.randn(x.size)
        inx = "val" + str(i)
        valDic[inx] = value    
    df = pd.DataFrame(valDic,index=idx)
    
    return df

def make_anomaly(df, periods, num, direction, trg_col=[]):
    start = np.random.randint(periods)
    end = start + num

    if trg_col == []:trg_col = df.columns
    for i in trg_col:
        if direction == "pos":
            df[i].iloc[start:end] = float(df[i].max()) * 10
        elif direction == "neg":
            if float(df[i].min()) < 0:
                df[i].iloc[start:end] = float(df[i].min()) * 10
            else:
                df[i].iloc[start:end] = float(df[i].min()) / 10
    return df
    
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

def missing_value(df, how="interpolate"):
    if how == "interpolate": #fill na by using linear interpolate
        df = df.interpolate()
    elif how == "drop": #drop na
        df = df.dropna()
    else:
        df = df.fillna(df.mean()) #fill na with mean value
    return df

def slide_window(df, num):
    return df.shift(num)

def file_reader(csv, header=0):
    df = pd.read_csv(csv,header=header)
    if df.isnull().any().sum() > 0:#if na is in the df
        df = missing_value(df)
    return df

def file_writer(df, out_name, i_convert=False):
    if i_convert:df = index_convert(df)
    df.to_csv(out_name,index_label=["TimeStamp"])

#convert timestamp format into yyyy/mm/ddTHH:mm:ss
def index_convert(df):
    index = df.index
    converted_index = []
    for i in index:
        j = "T".join(str(i).split(" ")) + "+09:00"
        converted_index.append(j)
    df.index = converted_index
    return df


def plot_fig(df, save=False):    
    fig=sns.PairGrid(df, diag_sharey=False)
    plt.subplots_adjust(top=0.9)
    fig.fig.suptitle("Distribution")
    fig.map_lower(sns.kdeplot, cmap="Blues_d")
    fig.map_upper(plt.scatter)
    fig.map_diag(sns.distplot)
    if save == True: fig.savefig("pairplot.png")

    #plot kde joitplot
    fig = plt.figure()
    g =sns.jointplot(x=df.columns.values[0] ,y=df.columns.values[1] ,kind="kde", data=df)
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("Kernel Distribution Estimation")
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
        plt.title("Histgram - " + df.columns[i])
        if save == True: fig.savefig("dist_plot_" + df.columns[i] + ".png")

        #plot series
        fig = plt.figure()
        df.iloc[:,i].plot()
        #plot moving average
        ma[i].plot(c='r')
        plt.title("Row data & Moving average - " + df.columns[i])
        if save == True: fig.savefig("series_plot_" + df.columns[i] + ".png")


        #plot acf
        fig = plt.figure()
        plt.bar(range(len(acf[i])), acf[i], width = 0.3)
        plt.title("Auto Correlation Function - " + df.columns[i])
        if save == True: fig.savefig("acf_plot_" + df.columns[i]+".png")

        #plot pcf
        fig = plt.figure()
        plt.bar(range(len(pcf[i])), pcf[i], width = 0.3)
        plt.title("Partial Auto Correlation Function - " + df.columns[i])
        if save == True: fig.savefig("pcf_plot_" + df.columns[i] + ".png")
        
        #plot fft
        fig = plt.figure()
        f = calc_fft(df.iloc[:,i])
        plt.plot(f[1], f[0])
        plt.title("Fast Fourier Transform - " + df.columns[i])
        if save == True: fig.savefig("fft_plot_" + df.columns[i] + ".png")
        
        #plot return value_i - value_i2
        fig = plt.figure()
        ret[i].plot()
        plt.title("Return - " + df.columns[i])
        if save == True: fig.savefig("return_plot_" + df.columns[i] + ".png")
        
# get diff
def calc_return(df):
    rets = []
    for i in  range(len(df.columns)):
        ret = df.iloc[:,i].pct_change().dropna()
        rets.append(ret)
    
    return rets

# get acf and partial acf
def calc_pacf(df):
    acfs = []
    pcfs = []
    for i in range(len(df.columns)):
        acf = stt.acf(df.iloc[:,i])
        acfs.append(acf)
        
        pcf = stt.pacf(df.iloc[:,i])
        pcfs.append(pcf)
    
    return acfs, pcfs

# get moving average
def calc_ma(df):
    mas = []
    for i in range(len(df.columns)):
        ma = pd.Series.rolling(df.iloc[:,i], window=3, center=True).mean()
        mas.append(ma)
    return mas

def data_understand(df, cross=False, r="row", c="col"):
    print(df.describe())
    if cross == True:
        crosstab = pd.pivot_table(df,values,index, columns,aggfunc=[np.sum])        
        print(crosstab)

def calc_fft(df):
    # Number of sample points
    N = len(df)
    # sample spacing
    T = 1.0 / N * 1.5
   ##window function
    w = blackman(N)
    y = df
    yf = 2.0/N * np.abs(fft(y*w)[0:N//2])
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    return yf, xf

if __name__ == "__main__":
    df = make_data("5t",288, 2)
    df = make_anomaly(df, 288, 3, "pos")
    plot_fig(df,"false")

