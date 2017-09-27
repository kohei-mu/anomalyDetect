# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 09:29:56 2017

@author: kohei-mu
"""

import argparse
import pandas as pd


def parse_command_line():
    parser = argparse.ArgumentParser(description="help messages")
    group1 = parser.add_argument_group('Main options')
    group2 = parser.add_argument_group('additional options')
    
    group1.add_argument("-resFreq", dest="rsF", default="5T", type=str, help="resampling frequency")
    group1.add_argument("-in", dest="in_csv", type=str, help="input csv")
    group1.add_argument("-out", dest="out_csv", type=str, help="output csv")
    group2.add_argument("-input_header",dest="inH", type=int, default=0, choices=[0,-1], help="input header option")
    group2.add_argument("-resHow", dest="rsH", type=str, default="mean", choices=["sum","mean","median","max","min","last","first"],help="how to resampling")
    group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
    group2.add_argument("-i_conv",dest="i_convert", type=bool, default=False, choices=[True, False], help="conert timestamp index(yyyy-mm-dd'T'hh:MM:DD+09:00)")
    return parser.parse_args()


def resample_time(df):
    how = args.rsH
    freq = args.rsF
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
    
    df = resample_time(df)   
    
    if args.out_csv:
        file_writer(df)
    
    
