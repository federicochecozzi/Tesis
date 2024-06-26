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

setwd(r"(D:\Tesis\Algunos resultados\outliers)")

q95 = c()
q975 = c()
q99 = c()

for(c in 1:12){
  print(c)
  subset <- trainData[trainClass == c,]
  centroid <- subset[,sapply(.SD,median)]
  centered_subset <- subset[,Map(`-`, .SD, centroid)]
  distance <- centered_subset[,sqrt(rowSums(.SD**2))]
  q <- quantile(distance,probs = c(0.95,0.975,0.99))
  q95 = c(q95,distance > q[1])
  q975 = c(q975,distance > q[2])
  q99 = c(q99,distance > q[3])
}

fwrite(list(q95 = q95, q975 = q975, q99 = q99),
       file = "outlier_list_euclidean.csv",
       sep = ","
)