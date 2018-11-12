library(rgl)
library(plotly)


df <- read.csv("test.csv", header=TRUE)
accept_auth <- df[,2]
rej_auth <- df[,3]
req_auth <- df[,4]
retr_auth <- df[,5]
  
plot3d(retr_auth,rej_auth,req_auth,col=c(2,3,4),type="p")


plot_ly(x = rej_auth, y = req_auth, z =accept_auth, type = 'mesh3d')
plot_ly(x = rej_auth, y = req_auth, z =accept_auth, type="scatter3d")



