x <- read.csv("C:/Users/kohei-mu/Downloads/indices_I101_1d_2016.csv", header = F)[,2]

sigmaCalculate <- function(sep, n, input) {
  mat <- matrix(input, nrow=sep)
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
  ranges <- data.frame(ret[,1],ret[,2])
  
  index <- 1
  ret_final <- NULL
  for(v in input){
    a_row <- c(v, ranges[index,])
    if(index == sep){
      index <- 1
    }else{
      index <- index + 1
    }
    ret_final <- rbind(ret_final, a_row)
  }

  return(ret_final)
}

