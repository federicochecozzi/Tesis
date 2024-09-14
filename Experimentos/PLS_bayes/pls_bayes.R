library(tidyverse)
library(data.table)
library(caret)
library(mdatools)
library(rhdf5)
#library(mlr)


# In case of insufficent memory, uncomment following line. Your disc will be used as buffer and data might be loaded
# memory.limit(size=65536)

# set number of spectra and path to the data files
setwd(r"(D:\Tesis\Datasets)")    # selecting the directory containing the data files
spectraCount <- 500   # selecting the number of spectra for each sample (maximum of 500), recommended 100

##########################################
# Train Data
##########################################

wavelengths <- as.data.frame(h5read(file = "train_downsampled.h5", name = "Wavelengths")) # import wavelengths
trainClass <- as.data.frame(h5read(file = "train_downsampled.h5", name = "Class")) # import classes
trainData <- h5read(file = "train_downsampled.h5", name = "Spectra") # import spectra
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
  
}#¿Puede cargarse hasta 50000?
trainClass <- redClass

##########################################
# Test Data
##########################################

testData <- h5read(file = "test_downsampled.h5", name = "UNKNOWN") # import spectra
h5closeAll()

testClass <- fread("test_labels.csv", dec = ',',header = FALSE)
testClass <- testClass$V1

testData <- as.data.frame(do.call('rbind',testData))

##########################################
# Outlier Data
##########################################
#setwd(r"(D:\Tesis\Algunos resultados\outliers)")

#outlier_list <- fread("outlier_list_euclidean.csv", dec = ',',header = TRUE)

#trainData <- trainData[outlier_list$q99 == FALSE,]
#trainClass <- trainClass[outlier_list$q99 == FALSE]

##########################################

rm(i, redClass, spectraCount, tempClass, reddim)
gc()

##########################################
# End of loading script
##########################################

#Entrenar el modelo
ncomp <- 60
start_time <- Sys.time()
model <- plsda(trainData,as.factor(trainClass),cv = NULL,ncomp = ncomp)
y <- model$calres$y.pred[,ncomp,] #esto genera una matriz de n observaciones por m clases

density.function.list <- list()
for (i in 1:12){
  density.function <- approxfun(density(y[,i]))
  append(density.function.list,density.function)
}

end_time <- Sys.time()

end_time - start_time

#Predicción con regla bayesiana

start_time <- Sys.time()

test_res = predict(model, testData, as.factor(testClass))

ypred <- test_res$y.pred
ypred <- ypred[,ncomp,]

#density.vector = numeric(nrow(testData),12)
#for (i in 1:12){
#  for (j in 1:nrow(testData)){
#   density.vector[j,i] = density.function.list[[i]](ypred[j,i])
#  }
#}
#priors = rep(1/12, 12)
#pclass = (density.vector * priors) / sum(density.vector * priors)

#regla detallada en: Statistical comparison of decision rules in PLS2-DA prediction model for 
#classification of blue gel pen inks according to pen brand and pen model
#class.pred <- integer(nrow(testData))
pmatrix <- numeric(nrow(testData),12)
pvector <- numeric(12)
priors <- rep(1/12, 12)
for (i in 1:nrow(testData)){
  for (j in 1:12){
    pvector[j] <- density.function.list[[j]](ypred[i,j]) * priors[j]
  }
  pvector <- pvector/sum(pvector)
  pmatrix[i,] <- pvector
  #class.pred[i] <- which.max(pvector)
}
class.pred <- as.factor(apply(pmatrix,1,which.max))

testClassfactor <- as.factor(testClass)
levels(testClassfactor) <- c(levels(testClassfactor),'12')
confusionMatrix(as.factor(testClass),class.pred) #


end_time <- Sys.time()

end_time - start_time

