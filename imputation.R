library(mice)

path <- "C:/Users/muramatsu/Documents/data/hirata/poc/processed/csv"
setwd(path)
files <- list.files(path, pattern=".csv")

for ( file in files){
  
  #入力ファイル名
  file_path <- paste(path, file, sep="")
  df <- read.csv(file_path, header=TRUE)
  
  #欠損値確認
  #md.pattern(df)
  
  #補完アルゴリズム確認
  #methods(mice)
  #補完実行
  tempData <- mice(df,
                   m=5, 
                   maxit=20,
                   meth='pmm', 
                   seed=500)
  
  #補完候補確認
  #tempData$imp
  #補完データと元データの分布が大きく変化していないことを確認
  #densityplot(tempData)
  
  #補完データ決定
  completedData <- complete(tempData,3)
  #md.pattern(completedData)
  
  #出力ファイル名
  out_file_tmp <- paste(strsplit(file, ".csv"), "_imp.csv", sep="")
  out_file <- paste(paste(path,'imp/',sep=""), out_file_tmp, sep="")
  #補完済みデータを出力
  write.csv(completedData, out_file, quote=FALSE, row.names=FALSE)

}





