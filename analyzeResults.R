# kurtis bertauche
# cpe 400 project
# analyzeResults.R

library(stringr)

data <- read.csv("./results.csv")

sparseResults <- data[which(str_detect(data$network, "sparse")),]
mediumResults <- data[which(str_detect(data$network, "medium")),]
denseResults <- data[which(str_detect(data$network, "dense")),]

n <- c(1,2,3,4,5)
sparseSmallVar <- sparseResults[which(sparseResults$num_user_packets == 500),]$variance
sparseMedVar <- sparseResults[which(sparseResults$num_user_packets == 1000),]$variance
sparseLargeVar <- sparseResults[which(sparseResults$num_user_packets == 1500),]$variance

plot(n,
     sparseSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Variance",
     pch = "o",
     ylim = c(1000, 15000),
     main = "Variance of Remaining Energy Levels in Sparse Network")

points(n, sparseMedVar, col="red", pch="o")
lines(n, sparseMedVar, col="red")

points(n, sparseLargeVar, col = "green", pch = "o")
lines(n, sparseLargeVar, col = "green", pch = "o")

legend(1,11500,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))

sparseSmallVar <- sparseResults[which(sparseResults$num_user_packets == 500),]$lowest_energy
sparseMedVar <- sparseResults[which(sparseResults$num_user_packets == 1000),]$lowest_energy
sparseLargeVar <- sparseResults[which(sparseResults$num_user_packets == 1500),]$lowest_energy

plot(n,
     sparseSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Energy Level",
     pch = "o",
     ylim = c(300, 1000),
     main = "Lowest Remaining Energy Levels in Sparse Network")

points(n, sparseMedVar, col="red", pch="o")
lines(n, sparseMedVar, col="red")

points(n, sparseLargeVar, col = "green", pch = "o")
lines(n, sparseLargeVar, col = "green", pch = "o")

legend(1,1000,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))

mediumSmallVar <- mediumResults[which(mediumResults$num_user_packets == 500),]$variance
mediumMedVar <- mediumResults[which(mediumResults$num_user_packets == 1000),]$variance
mediumLargeVar <- mediumResults[which(mediumResults$num_user_packets == 1500),]$variance

plot(n,
     mediumSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Variance",
     pch = "o",
     ylim = c(3000, 30000),
     main = "Variance of Remaining Energy Levels in Medium-Density Network")

points(n, mediumMedVar, col="red", pch="o")
lines(n, mediumMedVar, col="red")

points(n, mediumLargeVar, col = "green", pch = "o")
lines(n, mediumLargeVar, col = "green", pch = "o")

legend(1,20000,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))

mediumSmallVar <- mediumResults[which(mediumResults$num_user_packets == 500),]$lowest_energy
mediumMedVar <- mediumResults[which(mediumResults$num_user_packets == 1000),]$lowest_energy
mediumLargeVar <- mediumResults[which(mediumResults$num_user_packets == 1500),]$lowest_energy

plot(n,
     mediumSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Energy Level",
     pch = "o",
     ylim = c(300, 1000),
     main = "Lowest Remaining Energy Levels in Medium-Density Network")

points(n, mediumMedVar, col="red", pch="o")
lines(n, mediumMedVar, col="red")

points(n, mediumLargeVar, col = "green", pch = "o")
lines(n, mediumLargeVar, col = "green", pch = "o")

legend(1,1000,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))

largeSmallVar <- denseResults[which(denseResults$num_user_packets == 500),]$variance
largeMedVar <- denseResults[which(denseResults$num_user_packets == 1000),]$variance
largeLargeVar <- denseResults[which(denseResults$num_user_packets == 1500),]$variance

plot(n,
     largeSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Variance",
     pch = "o",
     ylim = c(3000, 30000),
     main = "Variance of Remaining Energy Levels in Dense Network")

points(n, largeMedVar, col="red", pch="o")
lines(n, largeMedVar, col="red")

points(n, largeLargeVar, col = "green", pch = "o")
lines(n, largeLargeVar, col = "green", pch = "o")

legend(1,20000,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))

largeSmallVar <- denseResults[which(denseResults$num_user_packets == 500),]$lowest_energy
largeMedVar <- ldenseesults[which(denseResults$num_user_packets == 1000),]$lowest_energy
largeLargeVar <- denseResults[which(denseResults$num_user_packets == 1500),]$lowest_energy

plot(n,
     largeSmallVar,
     type = "o",
     col = "blue",
     xlab = "n",
     ylab = "Energy Level",
     pch = "o",
     ylim = c(300, 1000),
     main = "Lowest Remaining Energy Levels in Dense Network")

points(n, largeMedVar, col="red", pch="o")
lines(n, largeMedVar, col="red")

points(n, largeLargeVar, col = "green", pch = "o")
lines(n, largeLargeVar, col = "green", pch = "o")

legend(1,1000,legend=c("500 Packets", "1000 Packets", "1500 Packets"), col = c("blue","red","green"),pch=c("o","o","o"),ncol= 1,lty=c(1,1,1))






