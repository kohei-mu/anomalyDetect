library(lattice)

path <-  "/fft/"
setwd(path)
files <- list.files(path, pattern=".csv")
for(file in files){
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  cols <- colorRampPalette(c("blue","white","red"))(256)
  my.mat <- apply(as.matrix(df), 2, as.numeric)
  graph_title <- paste(strsplit(file, "_imp_fft.csv"), "fft heatmap", sep=" ")
  heatmap(t(my.mat),Colv = NA, Rowv = NA, col=cols, xlab="time", ylab="metrics", main=graph_title)
}


