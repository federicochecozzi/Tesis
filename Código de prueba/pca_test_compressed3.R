library(tidyverse)
library(data.table)
library(rospca)
library(rhdf5)

# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd(r"(D:\Tesis\Datasets)")    # selecting the directory containing the data files
spectraCount <- 250   

##########################################
# Train Data
##########################################

trainClass <- as.data.frame(h5read(file = "train_downsampled_d6.h5", name = "Class")) # import classes
trainData <- h5read(file = "train_downsampled_d6.h5", name = "Spectra") # import spectra
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

start_time <- Sys.time()

pcar <- robpca(trainData, ndir = 5000)

end_time <- Sys.time()

end_time - start_time#no pude medirlo pero funcionó