library(tidyverse)
library(data.table)
library(pls)
library(klaR)
library(caret)
#library(mdatools)
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

start_time <- Sys.time()

acc_matrix <- matrix(c(0), nrow = 5, ncol = 60)
index <- seq(1,49500,1)
for (i in 0:4) {
  print(paste("i = ",i))
  model <- caret::plsda(trainData[index[seq(1,49500,1)%%5 != i],],as.factor(trainClass[index[seq(1,49500,1)%%5 != i]]),
                 ncomp = 60,probMethod = "Bayes")#,prior = rep(1/12,12))
  labels <- as.factor(trainClass[index[seq(1,49500,1)%%5 == i]])
  validationData <- trainData[index[seq(1,49500,1)%%5 == i],]
  
  for (j in 1:60){
    print(paste("i = ",i,", j = ",j))
    predlabels <- predict(model,validationData, ncomp = j)
    levels(predlabels) <- c(levels(predlabels),setdiff(levels(labels),levels(predlabels)))
    #In confusionMatrix.default(labels, predlabels) : Levels are not in the same order for reference and data. Refactoring data to match.
    confmat <- confusionMatrix(labels,predlabels) 
    if(i){
      acc_matrix[i,j] <- confmat$overall['Accuracy']
    } else {
      acc_matrix[5,j] <- confmat$overall['Accuracy']
    }
  }
}
end_time <- Sys.time()

end_time - start_time
#

ggplot() +
  geom_line(aes(x = 1:60, y = apply(1-acc_matrix, 2, mean))) +
  labs(x = "Components", y = "Error rate")

ncomp <- which.min(apply(1-acc_matrix, 2, mean))

start_time <- Sys.time()
model <- plsda(trainData,as.factor(trainClass),cv = NULL,ncomp = ncomp)
end_time <- Sys.time()

end_time - start_time
#1.766978 hours

start_time <- Sys.time()
test_res = predict(model, testData, as.factor(testClass))
end_time <- Sys.time()

end_time - start_time
#8.078789 mins

summary(test_res)

plotPredictions(test_res, ncomp = ncomp)

plotXResiduals(test_res, ncomp = ncomp)

confmat <- getConfusionMatrix(test_res, ncomp = ncomp)
confmat

accuracy <- sum(diag(confmat))/sum(confmat) * 100
accuracy
#57.2356

showPredictions(test_res, ncomp = ncomp)

ypred <- test_res$y.pred

testClassfactor <- as.factor(testClass)
levels(testClassfactor) <- c(levels(testClassfactor),'12')
confusionMatrix(as.factor(testClass),as.factor(apply(ypred[,ncomp,],1,which.max))) #73.43