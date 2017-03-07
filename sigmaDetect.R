x <- read.csv("indices_I101_1d_2016.csv", header = F)[,2]

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

ret <- sigmaCalculate(49,1,x)
plot(ret$value,type="l",ylab = "value")
points(which(ret$class==2), ret$value[which(ret$class==2)],col=2)
par(new=T)
plot(ret$right,type="l", col=4,ylim=c(min(ret$value), max(ret$value)),ylab = "")
par(new=T)
plot(ret$left,type="l", col=4,ylim=c(min(ret$value), max(ret$value)), ylab = "")