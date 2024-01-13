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

wavelengths <- as.data.frame(h5read(file = "train.h5", name = "Wavelengths")) # import wavelengths
trainClass <- as.data.frame(h5read(file = "train.h5", name = "Class")) # import classes
trainData <- h5read(file = "train.h5", name = "Spectra") # import spectra
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

#trainData[trainClass == 1,]
subset <- spectres_processed[class$trainClass == 1]

centroid <- spectres_processed[class$trainClass == 1,sapply(.SD,median)]

#https://stackoverflow.com/questions/46406029/data-table-minus-one-vector
#https://stackoverflow.com/questions/46843926/broadcasting-in-r
centered_subset <- subset[,Map(`-`, .SD, centroid)]#subset - t(centroid)

#distance <- centered_subset[,.(rowSums(.SD**2))]
distance <- centered_subset[,sqrt(rowSums(.SD**2))]


q1 <- quantile(distance,probs = c(0.05,0.95))

ggplot() + 
  geom_histogram(aes(x = distance)) +
  geom_vline(xintercept = q1)

q2 <- quantile(distance,probs = c(0.025,0.975))

ggplot() + 
  geom_histogram(aes(x = distance)) +
  geom_vline(xintercept = q2)

q3 <- quantile(distance,probs = c(0.01,0.99))

ggplot() + 
  geom_histogram(aes(x = distance)) +
  geom_vline(xintercept = q3)