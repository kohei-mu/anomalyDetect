library(colorednoise)

get_cus <- function(df) {
  cuct <- df[grep("CU_X|CU_Z|CT_X|CT_Z", names(df))]
  cu_x <- cuct[["CU_X"]]
  cu_z <- cuct[["CU_Z"]]
  ret <- list(cu_x, cu_z)
  return(ret)
}
get_fft <- function(met) {
  c <- fft(met)
  c_fft <- Mod(c)[1:round(length(c)/2)] * 2/ length(c)
  c_len <- length(c_fft)
  
  return(c_fft)
}
get_cf <- function(c_fft, period){
  first <-  1
  cn <- 0
  n <- seq(period+1,length(c_fft), period)
  cf_index <- c()
  for (i in n){
    c <- cn * period
    target <- c_fft[first:i]
    max_index <- which(target == max(target)) + c
    cf_index <- c(cf_index, max_index)
    first <- i
    cn <- cn + 1
  }
  return(cf_index)
}
get_random <- function(met){
  sin_random <- met
  white <- raw_noise(timesteps = length(met), mu = 0, sigma = 15, phi = 0)
  sin_random <- met + white
  #write into csv
  #write.csv(sin_random, "random.csv", quote=FALSE, row.names=FALSE)
  return(sin_random)
}
get_sideband <- function(met, cf_index, c_fft){
  sin_sideBand <- met
  m_index <- cf_index[c_fft[cf_index]==max(c_fft[cf_index])]
  for(i in c(-20, 20, -30, 30)){
    n <- c_fft[m_index] / 3
    x <- seq(0, (m_index + i) * 2 * pi, length=length(met))
    sin_tmp <- sin(x)
    #wave composition
    sin_sideBand <- sin_sideBand + n*sin_tmp
  }
  #write.csv(sin_sideBand, "sideband.csv", quote=FALSE, row.names=FALSE)
  return(sin_sideBand)
}
plt <- function(metName, met, c_fft, cf_index, sin_random, c_random_fft, sin_sideband, c_sideBand_fft){
  #metName : CU_X, CU_Z
  m_index <- cf_index[c_fft[cf_index]==max(c_fft[cf_index])]
  path <- '/20180216/'
  
  #original
  png(paste(path, paste(metName,"_original.png", sep=""), sep=""), width = 1000, height = 800)
  plot(met, type="l", main=paste(metName," original", sep=""), ylab="value", xlab="time")
  dev.off()
  
  png(paste(path, paste(metName,"_original_fft.png",sep=""), sep=""), width = 1000, height = 800)
  plot(c_fft,type="l", main=paste(metName," FFT(original)",sep=""), xlab="", ylab="", xlim=c(0, length(c_fft)), ylim=c(0, max(c_fft)))
  par(new=T)
  plot(cf_index,c_fft[cf_index],col=2, xlab="freq(1/1000 Hz)", ylab="", xlim=c(0, length(c_fft)), ylim=c(0, max(c_fft)), lwd=1)
  for (index in cf_index){
    text(index, c_fft[index], index , cex = 1,lwd=2) 
  }
  dev.off()
  
  png(paste(path, paste(metName,"_original_fft_zoom.png", sep=""), sep=""), width = 1000, height = 800)
  plot(c_fft[m_index-10:m_index+240],type="l", main=paste(metName," FFT(original) zoom", sep=""),xlab="freq(1/1000 Hz)", ylab="")
  dev.off()
  
  #random
  png(paste(path, paste(metName,"_random.png",sep=""), sep=""), width = 1000, height = 800)
  plot(sin_random, type="l", main=paste(metName," random",sep=""), xlab="time", ylab="value")
  dev.off()
  
  png(paste(path, paste(metName,"_random_fft.png",sep=""), sep=""), width = 1000, height = 800)
  plot(c_random_fft, type="l", main=paste(metName," FFT(random)",sep=""), ylab="", xlab = "" , xlim=c(0, length(c_random_fft)), ylim=c(0, max(c_random_fft)))
  par(new=T)
  plot(cf_index,c_fft[cf_index],col=2, xlab="freq(1/1000 Hz)", ylab="", xlim=c(0, length(c_random_fft)), ylim=c(0, max(c_random_fft)), lwd=1)
  for (index in cf_index){
    text(index, c_fft[index], index , cex = 1,lwd=2) 
  }
  dev.off()
  
  png(paste(path, paste(metName,"_random_fft_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot(c_random_fft[m_index-10:m_index+240], type="l", main=paste(metName," FFT(random) zoom",sep=""), xlab="freq(1/1000 Hz)", ylab="")
  dev.off()
  
  #sideband
  png(paste(path, paste(metName,"_sideband.png",sep=""), sep=""), width = 1000, height = 800)
  plot(sin_sideBand, type="l", main=paste(metName," sideband",sep=""), xlab = "time", ylab = "value")
  dev.off()
  
  png(paste(path, paste(metName,"_sideband_fft.png",sep=""), sep=""), width = 1000, height = 800)
  plot(c_sideBand_fft, type="l", main=paste(metName," FFT(sideband)",sep=""), ylab="",xlab = "" , xlim=c(0,length(c_sideBand_fft)), ylim=c(0,max(c_sideBand_fft)))
  par(new=T)
  plot(cf_index,c_fft[cf_index],col=2, xlab="freq(1/1000 Hz)", ylab="", xlim=c(0,length(c_sideBand_fft)), ylim=c(0,max(c_sideBand_fft)), lwd=1)
  for (index in cf_index){
    text(index, c_fft[index], index , cex = 1,lwd=2) 
  }
  dev.off()
  
  png(paste(path, paste(metName,"_sideband_fft_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot(c_sideBand_fft[m_index-10:m_index+240], type="l", main=paste(metName," FFT(sideband) zoom",sep=""), ylab="",xlab = "freq(1/1000 Hz)")
  dev.off()
  
  ## compare
  #all
  png(paste(path, paste(metName,"_compare_all.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met, type="l", main="original & random & sideband", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_random, type="l", main="", xlab="", ylab="", col=rgb(0, 1, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_sideBand, type="l", main="", xlab = "time", ylab = "value", col=rgb(0, 0, 1, alpha=0.5), ylim=c(-250,250))
  legend("bottomleft", legend=c("original","random","sideband"),col=c(rgb(1, 0, 0, alpha=0.5), rgb(0, 1, 0, alpha=0.5), rgb(0, 0, 1, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  dev.off()
  
  png(paste(path, paste(metName,"_compare_all_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met[0:200], type="l", main="original & random & sideband zoom", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_random[0:200], type="l", main="",xlab="", ylab="", col=rgb(0, 1, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_sideBand[0:200], type="l", main="",xlab = "time", ylab = "value", col=rgb(0, 0, 1, alpha=0.5),ylim=c(-250,250))
  #all
  legend("bottomleft", legend=c("original","random","sideband"),col=c(rgb(1, 0, 0, alpha=0.5),rgb(0, 1, 0, alpha=0.5),rgb(0, 0, 1, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  dev.off()
  
  #original & random
  png(paste(path, paste(metName,"_compare_original_random.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met, type="l", main="original & random", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_random, type="l", main="",xlab="time", ylab="value", col=rgb(0, 1, 0, alpha=0.5), ylim=c(-250,250))
  legend("bottomleft", legend=c("original","random"),col=c(rgb(1, 0, 0, alpha=0.5),rgb(0, 1, 0, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  dev.off()
  
  png(paste(path, paste(metName,"_residual_original_random.png",sep=""), sep=""), width = 1000, height = 800)
  plot((sin_random - met), type="l", main="original-random residual",xlab="time", ylab="value")
  dev.off()
  
  #original & random 0-1000
  png(paste(path, paste(metName,"_compare_original_random_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met[0:200], type="l", main="original & random zoom", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_random[0:200], type="l", main="",xlab="time", ylab="value", col=rgb(0, 1, 0, alpha=0.5), ylim=c(-250,250))
  legend("bottomleft", legend=c("original","random"),col=c(rgb(1, 0, 0, alpha=0.5),rgb(0, 1, 0, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  
  png(paste(path, paste(metName,"_residual_original_random_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot((sin_random - met)[0:200], type="l", main="original-random residual zoom",xlab="time", ylab="value")
  dev.off()
  
  #original & sideband
  png(paste(path, paste(metName,"_compare_original_sideband.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met, type="l", main="original & sideband", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_sideBand, type="l", main="",xlab = "time", ylab = "value", col=rgb(0, 0, 1, alpha=0.5),ylim=c(-250,250))
  legend("bottomleft", legend=c("original","sideband"),col=c(rgb(1, 0, 0, alpha=0.5),rgb(0, 0, 1, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  dev.off()
  
  png(paste(path, paste(metName, "_residual_original_sideband.png",sep=""), sep=""), width = 1000, height = 800)
  plot((sin_sideBand - met), type="l", main="original-sideband residual",xlab="time", ylab="value")
  dev.off()
  
  #original & sideband 0-1000
  png(paste(path, paste(metName,"_compare_original_sideband_zoom.png",sep=""), sep=""), width = 1000, height = 800)
  plot(met[0:200], type="l", main="original & sideband zoom", ylab="", xlab="", col=rgb(1, 0, 0, alpha=0.5), ylim=c(-250,250))
  par(new=T)
  plot(sin_sideBand[0:200], type="l", main="",xlab = "time", ylab = "value", col=rgb(0, 0, 1, alpha=0.5),ylim=c(-250,250))
  legend("bottomleft", legend=c("original","sideband"),col=c(rgb(1, 0, 0, alpha=0.5),rgb(0, 0, 1, alpha=0.5)),lty=c(1,2,3),pch = c(1,2,3))
  dev.off()
  
  png(paste(path, paste(metName,"_residual_original_sideband_zoom.png", sep=""), sep=""), width = 1000, height = 800)
  plot((sin_sideBand - met)[0:200], type="l", main="original-sideband residual zoom",xlab="time", ylab="value")
  dev.off()
}


df <- read.csv("test.csv", header=TRUE)
mets <- get_cus(df)
cu_x <- mets[[1]]
cu_z <- mets[[2]]
c_fft <- get_fft(cu_x)
cf_index <- get_cf(c_fft, 300)
sin_random <- get_random(cu_x)
c_random_fft <- get_fft(sin_random)
sin_sideBand <- get_sideband(cu_x, cf_index, c_fft)
c_sideBand_fft <- get_fft(sin_sideBand)
plt("CU_X", cu_x, c_fft, cf_index, sin_random, c_random_fft, sin_sideBand, c_sideBand_fft)

