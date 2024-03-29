# In case of missing library rhdf5, uncomment following line for first run of the script. Not needed later
# install.packages("rhdf5")
library(rhdf5)
library(tidyverse)
library(rospca)

# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd(r"(D:\Tesis\Datasets)")     # selecting the directory containing the data files
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

trainData <- as.data.frame(do.call('rbind',trainData))
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

start_time <- Sys.time()

pca <- prcomp(trainData[trainClass == 1,]) #44.44883 mins

end_time <- Sys.time()

end_time - start_time

start_time <- Sys.time()

pcar <- robpca(trainData[trainClass == 1,], ndir = 5000) #1.020878 hours

end_time <- Sys.time()

end_time - start_time