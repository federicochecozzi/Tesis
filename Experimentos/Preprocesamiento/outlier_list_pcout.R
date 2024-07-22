library(rhdf5)
library(tidyverse)
library(data.table)
library(mvoutlier)

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

pcoutlierp25 = c()
pcoutlierp10 = c()
pcoutlierp05 = c()
pcoutlierp045 = c()
pcoutlierp04 = c()
pcoutlierp035 = c()
pcoutlierp03 = c()

for(c in 1:12){
  print(c)
  subset <- trainData[trainClass == c,]
  result <- pcout(subset)
  
  pcoutlierp25 = c(pcoutlierp25, result$wfinal < 0.25)
  pcoutlierp10 = c(pcoutlierp10, result$wfinal < 0.10)
  pcoutlierp05 = c(pcoutlierp05, result$wfinal < 0.05)
  pcoutlierp045 = c(pcoutlierp045, result$wfinal < 0.045)
  pcoutlierp04 = c(pcoutlierp04, result$wfinal < 0.04)
}

hist(trainClass[pcoutlierp25 == FALSE])
sum(pcoutlierp25)
hist(trainClass[pcoutlierp10 == FALSE])
sum(pcoutlierp10)
hist(trainClass[pcoutlierp05 == FALSE])
sum(pcoutlierp05)
hist(trainClass[pcoutlierp045 == FALSE])
sum(pcoutlierp045)#a partir de acá no vale la pena demasiado
hist(trainClass[pcoutlierp04 == FALSE])
sum(pcoutlierp04)#se va a cero, tendría que hilar muy fino o almacenar resultados para encontrar un buen punto de corte

fwrite(list(pcoutlierp25 = pcoutlierp25, pcoutlierp10 = pcoutlierp10, 
            pcoutlierp05 = pcoutlierp05, pcoutlierp045 = pcoutlierp045),
       file = "outlier_list_pcout.csv",
       sep = ","
)
