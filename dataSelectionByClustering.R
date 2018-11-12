library(xts)
library(data.table)
library(psych)
library(stringr)
library(vegan)
library(dplyr)


df <- read.csv("test.csv", header=TRUE)
#apply(df[,2:ncol(df)], 2, summary)

time <- df[1]

########## calinski way
dat <- t(df[,2:ncol(df)])
res<-cascadeKM(dat,2,8)

best<-plot(res)
frame()
r<-best$x[,best$best.grps]
num <- as.integer(unlist(strsplit(names(best$best.grps), " "))[1])

for (i in 1:num){
  a <- r[r==i]
  d <- cbind(time, df[names(a)])
  lab=paste(paste("cluster",i,":"), name, "")
  if (ncol(d) > 2){
    cor.plot(cor(d[,2:ncol(d)]),numbers=T,main = i)
  }
  x <- as.xts(read.zoo(d))
  colnames(x) <- names(d)[2:length(names(d))]
  
  plot.zoo(x,plot.type = "multiple",main =i,xaxt="n", xlab = "time",ylab=names(x))
}

#all
cor.plot(cor(df[,2:ncol(df)]),numbers=T,main = "all")


#tree
dat <- t(df[,2:ncol(df)])
dist<-dist(dat)
hc <- hclust(dist)
plot(hc,main=paste("clustering result"),xlab="")

cluster_cut <- 15

cluster <- cutree(hc, k=cluster_cut) 
#cluster <- cutree(hc, k=3) 
cluster <- factor(cluster)

for (i in 1:cluster_cut){
  a<-cluster[cluster==i]
  d <- cbind(time, df[names(a)])
  #lab=paste(paste("cluster",i,":"), name, "")
  if (ncol(d) > 2){
    cor.plot(cor(d[,2:ncol(d)]),numbers=T,main = i)
  }
  x <- as.xts(read.zoo(d))
  colnames(x) <- names(d)[2:length(names(d))]
  
  plot.zoo(x, plot.type = "multiple",main =i,xaxt="n", xlab = "time",ylab=names(x))
}



