library(psych)
library(minerva)

#通常波形の相関
path <-  "C:/Users/muramatsu/Documents/data/hirata/poc/processed/csv/imp/"
setwd(path)
files <- list.files(path, pattern=".csv")
for (file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  #ピアソンの相関係数（単調）
  #pearson <- cor(df,method="pearson")
  #graph_pearson <- paste(strsplit(file, "_imp.csv"), "_pearson", sep="")
  #cor.plot(pearson, numbers = T,main=graph_pearson, xlas=2,cex.axis=0.75, cex=0.5)
  
  #スピアマンの相関係数（同調）
  spearman <- cor(df,method="spearman")
  graph_spearman <- paste(strsplit(file, "_imp.csv"), "_spearman", sep="")
  cor.plot(spearman, numbers = T,main=graph_spearman,xlas=2,cex.axis=0.75, cex=0.5)
  
  #MIC(非線形)
  #mic <- mine(df)$MIC
  #graph_mic <- paste(strsplit(file, "_imp.csv"), "_mic", sep="")
  #cor.plot(mic, numbers = T,main=graph_mic, xlas=2,cex.axis=0.75, cex=0.5)
}


###################


#FFTを掛けたあとの相関
path <-  "C:/Users/muramatsu/Documents/data/hirata/poc/processed/csv/imp/fft/"
setwd(path)
files <- list.files(path, pattern=".csv")
for (file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  #ピアソンの相関係数（単調）
  #pearson <- cor(df,method="pearson")
  #graph_pearson <- paste(strsplit(file, "_imp_fft.csv"), "_fft_pearson", sep="")
  #cor.plot(pearson, numbers = T,main=graph_pearson, xlas=2,cex.axis=0.75, cex=0.5)
  
  #スピアマンの相関係数（同調）
  spearman <- cor(df,method="spearman")
  graph_spearman <- paste(strsplit(file, "_imp_fft.csv"), "_fft_spearman", sep="")
  cor.plot(spearman, numbers = T,main=graph_spearman,xlas=2,cex.axis=0.75, cex=0.5)
  
  #MIC(非線形)
  #mic <- mine(df)$MIC
  #graph_mic <- paste(strsplit(file, "_imp_fft.csv"), "_fft_mic", sep="")
  #cor.plot(mic, numbers = T,main=graph_mic, xlas=2,cex.axis=0.75, cex=0.5)
}

