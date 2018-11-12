library(xts)
library(data.table)
library(psych)
library(stringr)
library(vegan)
library(dplyr)

path <- '/imp/'
setwd(path)
files <- list.files(path, pattern=".csv")
for(file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  dat <- t(df[,1:ncol(df)])
  #calsinki�@�ɂăN���X�^�����O
  #n~n+m�̊ԂœK���ȃN���X�^����߂�
  res<-cascadeKM(dat,2,10)
  
  #�K���ȃN���X�^���̊m�F
  best<-plot(res)
  frame()
  r<-best$x[,best$best.grps]
  num <- as.integer(unlist(strsplit(names(best$best.grps), " "))[1])
  
  graph_name <- paste(strsplit(file, "_imp.csv"), "_pearson", sep="")
  for (i in 1:num){
    #�����N���X�^��ɓ��������g���N�X
    a <- r[r==i]
    #df�����L���g���N�X�𒊏o
    d <- df[names(a)]
  
    #���ւ�m�F
    if (ncol(d) > 1){
      graph_name <- paste(strsplit(file, "_imp.csv"), i, sep=" : cluster")
      cor.plot(cor(d),numbers=T,main = graph_name, xlas=2)
    }
  }
}

