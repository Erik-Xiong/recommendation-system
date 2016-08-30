##########
#  Part 1
###########
#Dongbo Yao, 07.20.2016

#Read the data part

#create the address-list
address <- "~/Desktop/JD/order_071114_21w/part-"
address_list <- as.character(100003:100203)
address_list <- substr(address_list,2,length(address_list))
address_combined <- paste(address, address_list, sep = "")

#read the variable name and first file
tttt <- read.csv(address_combined[1], fileEncoding = "UTF-8", header = T, stringsAsFactors = F)
ttt <- read.csv(address_combined[2], fileEncoding = "UTF-8", header = F, stringsAsFactors = F)
test <- rbind(tttt,ttt)
View(test)
names(tttt)
names(test) <- names(tttt)
test1 <- test[,c(1:7,13,19,21,22)]
test2 <- test1

#read the rest file
for(i in 3:201)
{
  temp <- read.csv(address_combined[i], fileEncoding = "UTF-8", header = F, stringsAsFactors = F)
  temp_tmp <- temp[,c(1:7,13,19,21,22)]
  test2 <- rbind(test2, temp_tmp)
  print(i)
}

#delete the NA
test3 <- na.omit(test2)
names(test3) <- names(tttt)[c(1:7,13,19,21,22)]

#delete ones without user id
big_data <- test3[which(test3$user_id != "None"),]
#big_data_1 <- big_data[which(big_data$item_first_cate_cd ! = NA),]

#format the data
big_data$item_first_cate_cd <- as.numeric(big_data$item_first_cate_cd)
big_data$item_second_cate_cd <- as.numeric(big_data$item_second_cate_cd)
big_data$item_third_cate_cd <- as.numeric(big_data$item_third_cate_cd)
big_data$user_id <- as.numeric(big_data$user_id)
big_data$dt <- as.Date(big_data$dt)
dt <- as.Date(big_data$dt)
big_data <- na.omit(big_data)
write.csv(big_data, "~/Desktop/whole_2.csv", fileEncoding = "UTF-8", row.names = FALSE)
#the whole_2.csv is what we used in the first Apriori algorithm (week1-week2)

########
#  Part 2
########
#Similar process for the new data used in the last 2 weeks
# 08.11.2016

#recreate the address
address2 <- "~/Desktop/JD/order_071824_sale10_auto/part-"
address2_list <- as.character(100059:100259)
address2_list <- substr(address2_list,2,length(address2_list))
address2_combined <- paste(address2, address2_list, sep = "")
head(address2_combined)

#read the variable name and the first file
title_1 <- read.csv(address2_combined[1], fileEncoding = "UTF-8", header = T, stringsAsFactors = F)
text_1 <- read.csv(address2_combined[2], fileEncoding = "UTF-8", header = F, stringsAsFactors = F)
new_data <- text_1
names(new_data) <- names(title_1)
title_1
new_data2 <- new_data[,c(1:13,20:22,25,26,29:37)]
title_2 <- names(new_data2)
names(new_data2) <- NA

#read the rest
for(i in 3:201)
{
  temp <- read.csv(address2_combined[i], fileEncoding = "UTF-8", header = F, stringsAsFactors = F)
  temp_tmp <- temp[,c(1:13,20:22,25,26,29:37)]
  names(temp_tmp) <- NA
  new_data2 <- rbind(new_data2, temp_tmp)
  print(i)
}

#format the file
names(new_data2) <- title_2
summary(new_data2)
new_data2$item_first_cate_cd <- as.numeric(new_data2$item_first_cate_cd)
new_data2$item_second_cate_cd <- as.numeric(new_data2$item_second_cate_cd)
new_data2$item_third_cate_cd <- as.numeric(new_data2$item_third_cate_cd)
new_data2$sku_jd_prc <- as.numeric(new_data2$sku_jd_prc)                  
new_data2$sku_mkt_prc <- as.numeric(new_data2$sku_mkt_prc)
new_data2$sku_stk_prc <- as.numeric(new_data2$sku_stk_prc)
new_data2$sku_rebate_amount <- as.numeric(new_data2$sku_rebate_amount)
new_data2$user_id <- as.numeric(new_data2$user_id)
new_data3 <- na.omit(new_data2)

new_data4 <- new_data3[order(new_data3$user_id),]
new_data_good <- new_data4[-c(1:7),]

names(new_data_good)
new_data_good <- new_data_good[,-17]
new_data_good$sale_ord_dt <- as.Date(new_data_good$sale_ord_dt)

write.csv(new_data_good, "~/Desktop/new_data_0811.csv", fileEncoding = "UTF-8", row.names = FALSE)



#######
#  Part3 
########
#combine the two data set, with the variabels in data "big_data"
#then run the association part on whole new one
names(big_data)
names(new_data_good)

new_data_first <- new_data_good[,c(1,3:9,12,14)]
new_data_first$item_name <- NA
new_data_0816 <- rbind(big_data, new_data_first)
write.csv(new_data_0816, "~/Desktop/new_data_0816.csv", fileEncoding = "UTF-8", row.names = FALSE)

