library(e1071)


df <- read.csv("test.csv", header=FALSE)
tmp1 <-df$V2[2000:nrow(df)]
tmp2 <- df$V3[2000:nrow(df)]

plot(df$V2, type="l")
plot(df$V3, type="l")
plot(tmp1, type="l")
plot(tmp2, type="l")
d <- data.frame(x=tmp1, y=tmp2)


d.svm <- svm(x=d, y=NULL, type='one-classification', kernel='radial', gamma=0.2, nu=0.15)
px <- seq(0,1,0.1)
py <- seq(2,6,0.1)
pgrid <- expand.grid(px,py)
names(pgrid) <- names(d)
pred <- predict(d.svm, newdata=pgrid)
pred.num <- as.integer(pred)
plot(d, pch=19, cex=0.5, xlim=c(0,1), ylim=c(2,6), xlab='', ylab='',main="")
par(new=T)
contour(px, py, array(pred.num, dim=c(length(px),length(py))), levels=0.5, labels = '', xlim=c(0,1), ylim=c(2,6), lwd=5, col='red')
#legend("topleft", legend=c("�?離�?�?"),col=c("red"),pch=15,cex=1)


################################
tmp1 <-df$V6/10
tmp2 <- df$V3/10

train1 <- tmp1[1:3000]
train2 <- tmp2[1:3000]

test1 <- tmp1[3001:length(tmp1)]
test2 <- tmp2[3001:length(tmp2)]

d <- data.frame(x=train1, y=train2)
d_te <- data.frame(x=test1, y=test2)

d.svm <- svm(x=d, y=NULL, type='one-classification', kernel='radial', gamma=0.01, nu=0.1)


px <- seq(0,1.5,0.01)
py <- seq(0,1.5,0.01)



pgrid <- expand.grid(px,py)
names(pgrid) <- names(d)
pred <- predict(d.svm, newdata=pgrid)
pred.num <- as.integer(pred)
plot(d, pch=19, cex=0.5, xlim=c(0,1.5), ylim=c(0,1.5), xlab='', ylab='',main="")
par(new=T)
contour(px, py, array(pred.num, dim=c(length(px),length(py))), levels=0.5, labels = '', xlim=c(0,1.5), ylim=c(0,1.5), lwd=5, col='red')
#legend("topleft", legend=c("�?離�?�?"),col=c("red"),pch=15,cex=1)


##################################################

df <- read.csv("test.csv", header=TRUE)
tmp1 <-df["rxpadi"][,1]/10
tmp2 <- df["rxpadr"][,1]/10
d <- data.frame(x=tmp1, y=tmp2)


d.svm <- svm(x=d, y=NULL, type='one-classification', kernel='radial', gamma=0.01, nu=0.003)
px <- seq(0,2.5,0.01)
py <- seq(0,2.5,0.01)
pgrid <- expand.grid(px,py)
names(pgrid) <- names(d)
pred <- predict(d.svm, newdata=pgrid)
pred.num <- as.integer(pred)
plot(d, pch=19, cex=0.5, xlim=c(0,2.5), ylim=c(0,2.5), xlab='rxpadi', ylab='rxpadr',main="常時一定�?�波形")
par(new=T)
contour(px, py, array(pred.num, dim=c(length(px),length(py))), levels=0.5, labels = '', xlim=c(0,2.5), ylim=c(0,2.5), lwd=5, col='red')
legend("topleft", legend=c("�?離�?�?"),col=c("red"),pch=15,cex=1)

#################

df <- read.csv("test.csv", header=TRUE)
tmp1 <-df["ucdavis3"][,1]/1000000
tmp2 <- df["ucdavis6"][,1]/1000000
d <- data.frame(x=tmp1, y=tmp2)

d.svm <- svm(x=d, y=NULL, type='one-classification', kernel='radial', gamma=0.2, nu=0.015)
px <- seq(0,6,0.01)
py <- seq(0,6,0.01)
pgrid <- expand.grid(px,py)
names(pgrid) <- names(d)
pred <- predict(d.svm, newdata=pgrid)
pred.num <- as.integer(pred)
plot(d, pch=19, cex=0.5, xlim=c(0,6), ylim=c(0,6), xlab='ucdavis3', ylab='ucdavis6',main="�?離�?界（学習期間１ヶ月間?�?")
par(new=T)
contour(px, py, array(pred.num, dim=c(length(px),length(py))), levels=0.5, labels = '', xlim=c(0,6), ylim=c(0,6), lwd=5, col='red')
legend("topleft", legend=c("�?離�?�?"),col=c("red"),pch=15,cex=1)





###########################################
library(kernlab)

df <- read.csv("test.csv", header=FALSE)

tmp1 <-df$V6
tmp2 <- df$V3

train1 <- tmp1[2000:3500]
plot(train1, type="l", main="train1")
test1 <- tmp1[3501:length(tmp1)]
plot(test1, type="l", main="test1")

train2 <- tmp2[2000:3500]
plot(train12, type="l", main="train12")
test2 <- tmp2[3501:length(tmp2)]
plot(test2, type="l", main="test2")

train <- data.frame(x=train1, class=1)
test <- data.frame(x=test1, class=1)

train <- data.frame(x=train1, y=train2, class=1)
test <- data.frame(x=test1,y=test2, class=1)

tmp.svm <- ksvm(x=class~., data=train ,type="one-svc",kernel="rbfdot",kpar=list(sigma=0.001),nu=0.05)

tmp.outlier <- predict(tmp.svm, newdata=test)
cluster <- ifelse(tmp.outlier==TRUE, 1, 2)
tmp.result <- data.frame(test ,cluster)
plot(tmp.result$x,tmp.result$y, type="p", col=tmp.result$cluster,lwd=1)

tmp <- data.frame(val1=tmp.result$x,val2=tmp.result$y, cluster=tmp.result$cluster)
train.tmp <- train
names(train.tmp) <- names(tmp)
train.tmp$cluster <- 8
ret <- rbind(train.tmp,tmp)
plot(ret$val1, type="o", col=ret$cluster,lwd=1)
plot(ret$val2, type="o", col=ret$cluster,lwd=1)
plot(ret$val1, ret$val2, type="p", col=ret$cluster,lwd=1)


original <- data.frame(val1=tmp1[1:2000], val2=tmp2[1:2000])
original$cluster <- 3
ret <- rbind(original, train.tmp,tmp)
plot(ret$val1, type="o", col=ret$cluster,lwd=1)
plot(ret$val2, type="o", col=ret$cluster,lwd=1)
plot(ret$val1, ret$val2, type="p", col=ret$cluster,lwd=1)

