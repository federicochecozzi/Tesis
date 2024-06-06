library(rhdf5)
library(tidyverse)
library(data.table)


# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd(r"(D:\Tesis\Datasets)")    # selecting the directory containing the data files
spectraCount <- 500   # selecting the number of spectra for each sample (maximum of 500), recommended 100

##########################################
# Train Data
##########################################

wavelengths <- as.data.frame(h5read(file = "train_processed.h5", name = "Wavelengths")) # import wavelengths
trainClass <- as.data.frame(h5read(file = "train_processed.h5", name = "Class")) # import classes
trainData <- h5read(file = "train_processed.h5", name = "Spectra") # import spectra
h5closeAll()

##########################################
# Reduce number of spectra per sample
##########################################

reddim <- function(x){
  x <- x[1:spectraCount,]
}
trainData <- lapply(trainData,reddim)

##########################################

trainData <- as.data.table(do.call('rbind',trainData))
tempClass <- vector()
redClass <- trainClass[(1):(spectraCount),]
for (i in c(seq(500,49500,500))){
  tempClass <- trainClass[(i+1):(i+spectraCount),]
  redClass <-  append(redClass,tempClass)
  
}
trainClass <- redClass

##########################################

rm(i, redClass, spectraCount, tempClass, reddim)
gc()

##########################################
# End of loading script
##########################################

#Prueba con una clase
#subset <- trainData[trainClass == 1]

#centroid <- trainData[trainClass == 1,sapply(.SD,median)]

#https://stackoverflow.com/questions/46406029/data-table-minus-one-vector
#https://stackoverflow.com/questions/46843926/broadcasting-in-r
#centered_subset <- subset[,Map(`-`, .SD, centroid)]#subset - t(centroid)

#distance <- centered_subset[,.(rowSums(.SD**2))]
#distance <- centered_subset[,sqrt(rowSums(.SD**2))]


#q1 <- quantile(distance,probs = 0.95)

#ggplot() + 
#  geom_histogram(aes(x = distance)) +
#  geom_vline(xintercept = q1) +
#  ggtitle(paste0("Clase:",1,", cutoff = 0.95"))

#q2 <- quantile(distance,probs = 0.975)

#ggplot() + 
#  geom_histogram(aes(x = distance)) +
#  geom_vline(xintercept = q2)

#q3 <- quantile(distance,probs = 0.99)

#ggplot() + 
#  geom_histogram(aes(x = distance)) +
#  geom_vline(xintercept = q3)

#ggplot() + 
#  geom_histogram(aes(x = distance)) +
#  geom_vline(xintercept = c(q1,q2,q3))

#Todas las clases
setwd(r"(D:\Tesis\Algunos resultados\outliers)")
pdf("euclidean_outliers.pdf")
for(c in 1:12){
  print(c)
  subset <- trainData[trainClass == c,]
  centroid <- subset[,sapply(.SD,median)]
  centered_subset <- subset[,Map(`-`, .SD, centroid)]
  distance <- centered_subset[,sqrt(rowSums(.SD**2))]
  q <- quantile(distance,probs = c(0.95,0.975,0.99))

  p <- ggplot() + 
      geom_histogram(aes(x = distance)) +
      geom_vline(xintercept = q) +
      ggtitle(paste0("Class:",c,", quantiles: 0.95, 0.975, 0.99"))
  print(p)
}
dev.off()