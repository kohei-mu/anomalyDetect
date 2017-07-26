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


def parse_command_line():
	parser = argparse.ArgumentParser(description="help messages")
	group1 = parser.add_argument_group('Main options')
	group2 = parser.add_argument_group('additional options')

	group1.add_argument("-freq", dest="pvt_src", help="pivot-source phrase-table")
	group1.add_argument("-anFreq", dest="pvt_tgt", help="pivot-target phrase-table")
	group1.add_argument("-periods", dest="output", default="tmp_phrase-table", type=str, help="")
	group1.add_argument("-anomalyNum", dest="merged_output", default="merged_phrase-table", type=str, help="")
	group1.add_argument("-anomalyDirection", dest="norm_output", default="normalized_phrase-table", type=str, help="")
	group1.add_argument("-resamleFreq", dest="lex_output", default="final_phrase-table", type=str, help="")
	group1.add_argument("-tp", dest="tp", choices=[0, 1, 2, 3, 4, 5, 6], default=0, type=int, help="")

	group2.add_argument("-resampleHow", dest="disfile", type=str, help=")")
	group2.add_argument("-resampleHow", dest="tpnum", default=20, type=int, help="")
	return parser.parse_args()



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




