x <- read.csv("indices_I101_1d_2016.csv", header = F)[,2]

#function to sigma range and class
sigmaCalculate <- function(term, n, input) {
  mat <- matrix(input, nrow=term)
  ret <- NULL
  for(i in 1:length(mat[,1])){
    row <- mat[i,]
    sd <- sd(row)
    mean <- mean(row)
    range_r <- mean + n * sd
    range_l <- mean - n * sd
    tmp <- c(range_r, range_l)
    ret <- rbind(ret,tmp)
  }
  sigma_ranges <- data.frame(right=ret[,1],left=ret[,2])
  
  term_counter <- 1
  ret_final <- NULL
  for(v in input){
    a_row <- data.frame(value=v, sigma_ranges[term_counter,])
    if(term_counter == term){
      term_counter <- 1
    }else{
      term_counter <- term_counter + 1
    }
    ret_final <- rbind(ret_final, a_row)
  }
  
  class <- NULL
  for(i in 1:nrow(ret_final)){
    row <- ret_final[i,]
    if(row[,1] > row[,2] || row[,1] < row[,3]){
      class_ <- 2
    }else{
      class_ <- 1
    }
    class <- c(class, class_)
  }
  result <- data.frame(ret_final, class)

  return(result)
}

#objective function for optimization
obj <- function (param) {
  #define anomaly ratio
  trg_level <- 95
  func_out <- sigmaCalculate(49,param,x)
  trg <- 1 - trg_level/100
  a.ratio <- length(which(func_out$class==2)) / length(func_out$class)
  #return residual
  resi <- abs(trg - a.ratio)
  return(resi)
}

#parameter optimization
ret  <-optim(optim(0.5, obj,control = list(maxit=100), method = "SANN")$par,
             lower=1, upper=4,
             obj,control = list(maxit = 100000),
             method = "L-BFGS-B")

#plot
result <- sigmaCalculate(49,ret$par,x)
plot(result$value,type="l",ylab = "value")
points(which(result$class==2), result$value[which(result$class==2)],col=2)
par(new=T)
plot(result$right,type="l", col=4,ylim=c(min(result$value), max(result$value)),ylab = "")
par(new=T)
plot(result$left,type="l", col=4,ylim=c(min(result$value), max(result$value)), ylab = "")
