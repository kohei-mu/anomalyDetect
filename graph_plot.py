# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 09:36:16 2017

@author: kohei-mu
"""


import argparse
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.fftpack import fft
from scipy.signal import blackman
import statsmodels.tsa.stattools as stt


def parse_command_line():
    parser = argparse.ArgumentParser(description="help messages")
    group1 = parser.add_argument_group('Main options')
    group2 = parser.add_argument_group('additional options')
    
    group1.add_argument("-in", dest="in_csv", type=str, help="input csv")
    group1.add_argument("-out", dest="out_csv", type=str, help="output csv")
    group1.add_argument("-save", dest="save", type=bool, default=False, choices=[True, False], help="save plots")
    
    group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
    group2.add_argument("-input_header",dest="inH", type=int, default=0, choices=[0,-1], help="input header option")
    group2.add_argument("-crosstab",dest="cross", type=bool, default=False, choices=[True, False], help="calculate crosstab")
    return parser.parse_args()

def missing_value(df):
    #indexer=np.random.randint(4,size=30)==1
    #df.loc[indexer]=np.nan
    how  = args.msH
    if how == "interpolate":
        df=df.interpolate()
    elif how == "drop":
        df=df.dropna()
    else:
        df=df.fillna(df.mean())
        #bfill : backward
        #ffill : forward
    return df

def file_reader(csv):
    df=pd.read_csv(csv,header=args.inH)
    if df.isnull().any().sum() > 0:
        df = missing_value(df)
    return df

def plot_fig(df):    
    fig=sns.PairGrid(df, diag_sharey=False)
    plt.subplots_adjust(top=0.9)
    fig.fig.suptitle("Distribution")
    fig.map_lower(sns.kdeplot, cmap="Blues_d")
    fig.map_upper(plt.scatter)
    fig.map_diag(sns.distplot)
    if args.save:fig.savefig("pairplot.png")

    #plot kde joitplot
    fig = plt.figure()
    g=sns.jointplot(x=df.columns.values[0] ,y=df.columns.values[1] ,kind="kde", data=df)
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle("Kernel Distribution Estimation")
    if args.save: fig.savefig("joint_kde_plot.png")

    #plot correlation matrix
    fig = plt.figure()
    fig.suptitle("Correlation Matrix")
    sns.heatmap(df.corr().as_matrix(), annot=True,cmap='Blues')
    if args.save: fig.savefig("corr_matrix_plot.png")
        
    #calculate acf, pcf
    acf, pcf = calc_pacf(df)
    ma = calc_ma(df)
    
    #calcularw return
    ret = calc_return(df)
    
    for i in range(len(df.columns)):
        #plot distribution
        fig = plt.figure()
        sns.distplot(df.iloc[:,i])
        plt.title("Histgram - "+df.columns[i])
        if args.save:fig.savefig("dist_plot_"+df.columns[i]+".png")

        #plot series
        fig = plt.figure()
        df.iloc[:,i].plot()
        #plot moving average
        ma[i].plot(c='r')
        plt.title("Row data & Moving average - "+df.columns[i])
        if args.save:fig.savefig("series_plot_"+df.columns[i]+".png")


        #plot acf
        fig = plt.figure()
        plt.bar(range(len(acf[i])), acf[i], width = 0.3)
        plt.title("Auto Correlation Function - "+df.columns[i])
        if args.save:fig.savefig("acf_plot_"+df.columns[i]+".png")

        #plot pcf
        fig = plt.figure()
        plt.bar(range(len(pcf[i])), pcf[i], width = 0.3)
        plt.title("Partial Auto Correlation Function - "+df.columns[i])
        if args.save:fig.savefig("pcf_plot_"+df.columns[i]+".png")
        
        #plot fft
        fig = plt.figure()
        f = calc_fft(df.iloc[:,i])
        plt.plot(f[1], f[0])
        plt.title("Fast Fourier Transform - "+df.columns[i])
        if args.save:fig.savefig("fft_plot_"+df.columns[i]+".png")
        
        #plot return value_i - value_i2
        fig = plt.figure()
        ret[i].plot()
        plt.title("Return - "+df.columns[i])
        if args.save:fig.savefig("return_plot_"+df.columns[i]+".png")
        

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

def data_understand(df, r="row", c="col"):
    print df.describe()
    
    if args.cross:
        crosstab = pd.pivot_table(df,values,index, columns,aggfunc=[np.sum])        
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


if __name__ == "__main__":
    args = parse_command_line()
    if args.in_csv:
        df = file_reader(args.in_csv)
    
    plot_fig(df)
    data_understand(df)




