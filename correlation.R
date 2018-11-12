library(psych)
library(minerva)

#�ʏ�g�`�̑���
path <-  "/imp/"
setwd(path)
files <- list.files(path, pattern=".csv")
for (file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  #�s�A�\���̑��֌W���i�P���j
  #pearson <- cor(df,method="pearson")
  #graph_pearson <- paste(strsplit(file, "_imp.csv"), "_pearson", sep="")
  #cor.plot(pearson, numbers = T,main=graph_pearson, xlas=2,cex.axis=0.75, cex=0.5)
  
  #�X�s�A�}���̑��֌W���i�����j
  spearman <- cor(df,method="spearman")
  graph_spearman <- paste(strsplit(file, "_imp.csv"), "_spearman", sep="")
  cor.plot(spearman, numbers = T,main=graph_spearman,xlas=2,cex.axis=0.75, cex=0.5)
  
  #MIC(����`)
  #mic <- mine(df)$MIC
  #graph_mic <- paste(strsplit(file, "_imp.csv"), "_mic", sep="")
  #cor.plot(mic, numbers = T,main=graph_mic, xlas=2,cex.axis=0.75, cex=0.5)
}


###################


#FFT��|�������Ƃ̑���
path <-  "/fft/"
setwd(path)
files <- list.files(path, pattern=".csv")
for (file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  #�s�A�\���̑��֌W���i�P���j
  #pearson <- cor(df,method="pearson")
  #graph_pearson <- paste(strsplit(file, "_imp_fft.csv"), "_fft_pearson", sep="")
  #cor.plot(pearson, numbers = T,main=graph_pearson, xlas=2,cex.axis=0.75, cex=0.5)
  
  #�X�s�A�}���̑��֌W���i�����j
  spearman <- cor(df,method="spearman")
  graph_spearman <- paste(strsplit(file, "_imp_fft.csv"), "_fft_spearman", sep="")
  cor.plot(spearman, numbers = T,main=graph_spearman,xlas=2,cex.axis=0.75, cex=0.5)
  
  #MIC(����`)
  #mic <- mine(df)$MIC
  #graph_mic <- paste(strsplit(file, "_imp_fft.csv"), "_fft_mic", sep="")
  #cor.plot(mic, numbers = T,main=graph_mic, xlas=2,cex.axis=0.75, cex=0.5)
}

