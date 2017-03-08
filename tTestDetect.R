func <- function(data,span, v1, v2){
  term <- seq(0, length(data)-span*2, by=span)
  result <- NULL
  tmp <- NULL
  
  for (i in term){
    train <- data[(i+1):(span+i)]
    test <- data[(span+i+1):(span*2+i)]
    t <- t.test(train, test, var.equal = F)
    print(t$p.value)
    if(t$p.value < v1  && t$p.value > v2){
      tmp <- cbind(test, class=2)
    }else{
      tmp <- cbind(test, class=1)
    }
    result <- rbind(result, tmp)
  }
  return(result)
}
result <- func(ww, 100, 1e-100,7e-320)

plot(as.numeric(result[,1]), type="l", col=result[,2], main="demo data",xlab = "time", ylab = "value")
points(which(result[,2]==2),cex=0.5,as.numeric(result[which(result[,2]==2)]),col=2)
