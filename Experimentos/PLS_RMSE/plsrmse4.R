library(tidyverse)
library(data.table)
library(mdatools)
library(rhdf5)
#library(mlr)

#Cuidado, no hay suficiente memoria para correr este script, requiere memoria virtual

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

trainData <- as.data.frame(do.call('rbind',trainData))
tempClass <- vector()
redClass <- trainClass[(1):(spectraCount),]
for (i in c(seq(500,49500,500))){
  tempClass <- trainClass[(i+1):(i+spectraCount),]
  redClass <-  append(redClass,tempClass)
  
}
trainClass <- redClass

##########################################
# Test Data
##########################################

testData <- h5read(file = "test.h5", name = "UNKNOWN") # import spectra
h5closeAll()

testClass <- fread("test_labels.csv", dec = ',',header = FALSE)
testClass <- testClass$V1

testData <- as.data.frame(do.call('rbind',testData))

##########################################

rm(i, redClass, spectraCount, tempClass, reddim)
gc()

##########################################
# End of loading script
##########################################

start_time <- Sys.time()
model <- plsda(trainData,as.factor(trainClass),cv = list('ven', 5))
end_time <- Sys.time()

end_time - start_time
#13.1609 hours

summary(model)

plotRMSE(model)

plotPredictions(model, ncomp = 14)
plotPredictions(structure(model, class = "regmodel"), ncomp = 14, ny = 3)

start_time <- Sys.time()
test_res = predict(model, testData, as.factor(testClass))
end_time <- Sys.time()

end_time - start_time
#6.52215 mins

summary(test_res)

plotPredictions(test_res, ncomp = 14)
#plotPredictions(test_res, res = "cv", ncomp = 17)

plotXResiduals(test_res, ncomp = 14)

confmat <- getConfusionMatrix(test_res, ncomp = 14)
confmat

accuracy <- sum(diag(confmat))/sum(confmat) * 100
accuracy

showPredictions(test_res, ncomp = 14)

pred_class <- test_res$c.pred