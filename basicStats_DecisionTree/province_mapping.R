# MAPPING TO CHINA MAP BASED ON PROVINCE FREQUENCY
# 
# JING WANG
# AUG. 13, 2016
# JD.COM, BEIJING

library(maps)
library(mapdata)
library(maptools)
setwd('/Users/jingwang/Documents/Jing Wang/2016 Summer Intern/JD RUN/projects/Final')


# x = readShapePloy('bou2_4p.shp')
getColor <- function(mapdata,provname,provcol,othercol)   
  { 
  f=function(x,y) ifelse(x %in% y,which(y==x),0);   
  colIndex=sapply(iconv(x@data$NAME,"GBK","UTF-8"),f,provname);   
  col=c(othercol,provcol)[colIndex+1];   
  return(col);   
}  
# 画地图数据  
provname=c("北京市","广东省","江苏省","上海市","四川省", "山东省","浙江省",
           "河北省","湖北省","河南省", "辽宁省","天津市","陕西省","黑龙江省",
           "山西省", "福建省","安徽省","贵州省","甘肃省", "广西壮族自治区",
           "云南省","湖南省","吉林省","重庆市", "内蒙古自治区","新疆维吾尔自治区",
           "海南省","江西省", "宁夏回族自治区");  

data = read.csv('new_province_id.csv', header = T)
freq = data[,3]

# 构建图例的位置  
nf <- layout(matrix(c(1,1,1,1,1,2,1,1,1),3,3,byrow=TRUE), c(3,1), c(3,1), TRUE)  
layout.show(nf)  

provcol <- rgb(red=1-freq/max(freq)/1,green=1-freq/max(freq)/1,blue=1/1.5);  
plot(x,col=getColor(x,provname,provcol,"white"),xlab="",ylab="")
## 整理数据  
freq <- freq - min(freq)  
freq =freq-min(freq)  

# 添加图例  
par(mar=c(0,0,0,0))  
par(mar=c(1,1,2,0),cex=0.5)  
barplot(as.matrix(rep(1,length(freq))),col=sort(provcol,dec=T),horiz=T,axes=F,border = NA )  
axis(1,seq(1,length(freq),by=2),sort(freq[seq(1,length(freq),by=2)]))  
