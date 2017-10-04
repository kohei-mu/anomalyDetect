# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 09:15:44 2017

@author: kohei-mu
"""
import argparse
import numpy as np
import pandas as pd
from datetime import datetime


def parse_command_line():
    parser = argparse.ArgumentParser(description="help messages")
    group1 = parser.add_argument_group('Main options')
    group2 = parser.add_argument_group('additional options')
    
    group1.add_argument("-freq", dest="freq", default="5T", type=str, help="time frequency of data")
    group1.add_argument("-periods", dest="prd", default=288, type=int, help="periods of data(data points)")
    group1.add_argument("-ncol", dest="ncol", default=1, type=int, help="number of columns")
    group1.add_argument("-anom", dest="anom", type=bool,default=False, help="make anomaly flag")
    group1.add_argument("-anomaNum", dest="amN", default=10, type=int, help="anomaly points")
    group1.add_argument("-anomaDirect", dest="amD", choices=["pos","neg"], default="pos", type=str, help="anomaly direction")
    group1.add_argument("-trg_cols", dest="trg_cols", default="", type=str, help="anomaly target cols seperated " "##col1 col2 col3 ....")
    group1.add_argument("-in", dest="in_csv", type=str, help="input csv")
    group1.add_argument("-out", dest="out_csv", type=str, help="output csv")
    
    group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
    group2.add_argument("-input_header",dest="inH", type=int, default=0, choices=[0,-1], help="input header option")
    group2.add_argument("-i_conv",dest="i_convert", type=bool, default=False, choices=[True, False], help="conert timestamp index(yyyy-mm-dd'T'hh:MM:DD+09:00)")
    return parser.parse_args()


def make_data(freq,periods):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx=pd.date_range(now,freq=args.freq,periods=args.prd)
    x = np.linspace(0, 100, num=args.prd)
    pi2 = 2.*np.pi    
    valDic = {}
    for i in range(args.ncol):
        value = np.random.randint(10)*np.sin(0.1*pi2*x) +np.random.randint(10)*np.cos(1.*pi2*x) +  np.random.rand(1)*np.random.randn(x.size)
        inx = "val" + str(i)
        valDic[inx] = value    
    df=pd.DataFrame(valDic,index=idx)
    
    return df

def make_anomaly(df):
    start = np.random.randint(args.prd)
    end = start + args.amN
    #print df.iloc[start], df.iloc[end]    

    if args.trg_col == "":
        trg_cols = df.columns
    else:
        trg_cols = args.trg_cols.split("")
    
    for i in trg_cols:
        if args.amD == "pos":
            df[i].iloc[start:end] = float(df[i].max()) * 10
        elif args.amD == "neg":
            if float(df[i].min()) < 0:
                df[i].iloc[start:end] = float(df[i].min()) * 10
            else:
                df[i].iloc[start:end] = float(df[i].min()) / 10
    return df

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
    
def file_writer(df):
    if args.i_convert:df = index_convert(df)
    df.to_csv(args.out_csv,index_label=["TimeStamp"])

def index_convert(df):
    index = df.index
    k=[]
    for i in index:
        j = "T".join(str(i).split(" ")) + "+09:00"
        k.append(j)
    df.index = k
    return df



if __name__ == "__main__":
    args = parse_command_line()
    
    if args.in_csv:
        df = file_reader(args.in_csv)
    
    df=make_data()
    
    if args.anom:    
        df = make_anomaly(df)

    if args.out_csv:
        file_writer(df)
    

