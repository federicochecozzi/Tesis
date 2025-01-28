library(rhdf5)
library(rospca)
#library(mlr)


# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd(r"(D:\Tesis\Datasets)")    # selecting the directory containing the data files
spectraCount <- 250   # selecting the number of spectra for each sample (maximum of 500), recommended 100

##########################################
# Train Data
##########################################

wavelengths <- as.data.frame(h5read(file = "train_downsampled_d6.h5", name = "Wavelengths")) # import wavelengths
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

trainData <- as.data.frame(do.call('rbind',trainData))
tempClass <- vector()
redClass <- trainClass[(1):(spectraCount),]
for (i in c(seq(750,49750,500))){#esto permite quedarse con la segunda mitad del dataset
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

#Búsqueda de outliers

#debug

#start_time <- Sys.time()

#pcar <- robpca(trainData[trainClass == 1,], ndir = 10)

#pcar$flag.all #acá está un flag que detecta outliers

#end_time <- Sys.time()

#end_time - start_time

start_time <- Sys.time()

keep.flag <- c()

for (i in 1:12){
  print(i)
  pcar <- robpca(trainData[trainClass == i,], ndir = 1000)
  
  keep.flag <- c(keep.flag,pcar$flag.all) #acá está un flag que detecta outliers
}

#keep.flag <- !outlier.flag

end_time <- Sys.time()

end_time - start_time #47.99947 mins

setwd(r"(D:\Tesis\Algunos resultados\outliers)")  

write.csv(keep.flag, file ="keep_list_PCAR_d6_sc250b.csv", row.names=FALSE)