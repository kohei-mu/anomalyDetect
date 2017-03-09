data <- as.numeric(o[,1])

func <- function(sigma,nu, train, test){
  train_ <- data.frame(train, class=1)
  model <- ksvm(x=class~.,
                data=train_,
                type = "one-svc",   
                kernel = "rbfdot",      
                kpar=list(sigma=sigma),
                nu=nu, 
                cross=5 ,    
                prob.model = TRUE 
  )
  
  x.data.outlier <- predict(model, test)
  cluster <- ifelse(x.data.outlier==TRUE, 1, 2)
  x.result <- data.frame(test, cluster) 
  return(x.result)
}

obj <- function(param){
  trg_level <- 99.9
  trg <- 1 - trg_level/100
  func_out <- func(sigma=param[1], nu=param[2], train=data, test=data)
  a.ratio <- length(which(func_out$cluster==2)) / length(func_out$cluster)
  resi <- abs(trg - a.ratio)
  return(resi)
}

ret  <-optim(c(0.5, 0.01),
             lower=c(0.1, 0.0005), upper=c(0.9,0.1),
             obj,control = list(maxit = 500),
             method = "L-BFGS-B")

result <- func(ret$par[1],ret$par[2],data,data)
plot(result[,1], type="l", xlab="time", ylab="value")
points(which(result[,2]==2),cex=1, result[,1][which(result[,2]==2)],col=2)
print(length(which(result$cluster==2))/length(result$cluster))

