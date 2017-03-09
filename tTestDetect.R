func <- function(data,span, v1, v2){
  term <- seq(0, length(data)-span*2, by=span)
  result <- NULL
  tmp <- NULL
  p.val <- NULL
  for (i in term){
    train <- data[(i+1):(span+i)]
    test <- data[(span+i+1):(span*2+i)]
    t <- t.test(train, test, var.equal = F)
    p.val<-c(p.val,t$p.value)
    if (is.nan(t$p.value)){
      tmp <- cbind(test, class=1)
    }else if(t$p.value < v1  && t$p.value > v2 ){
      tmp <- cbind(test, class=2)
    }else{
      tmp <- cbind(test, class=1)
    }
    result <- rbind(result, tmp)
  }
  result <- data.frame(result, p.val)
  
  return(result)
}

obj <- function (param) {
  trg_level <- 96
  func_out <- func(data=o[,2], span = param[3], v1 = param[1], v2 = param[2])
  trg <- 1 - trg_level/100
  a.ratio <- length(which(func_out$class==2)) / length(func_out$class)
  resi <- abs(trg - a.ratio)
  return(resi)
}
ret  <-optim(c(1e-100, 1e-1000, 300),
             lower=c(1e-100, 1e-1000, 200), upper=c(0.1,0.1,500),
             obj,control = list(maxit = 10000),
             method = "L-BFGS-B")

result <- func(o[,2], ret$par[3], ret$par[1],ret$par[2])
plot(as.numeric(result[,1]), type="l",xlab = "time", ylab = "value")
points(which(result[,2]==2),cex=1,as.numeric(result[,1][which(result[,2]==2)]),col=2)
print(length(which(result$class==2))/length(result$class))
