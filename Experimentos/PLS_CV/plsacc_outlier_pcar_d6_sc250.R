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

trainData <- as.data.table(do.call('rbind',trainData))
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

testData <- h5read(file = "test_downsampled.h5", name = "UNKNOWN") # import spectra
h5closeAll()

testClass <- fread("test_labels.csv", dec = ',',header = FALSE)
testClass <- testClass$V1

testData <- as.data.frame(do.call('rbind',testData))

##########################################
# Outlier Data
##########################################
setwd(r"(D:\Tesis\Algunos resultados\outliers)")

keep_lista <- as.vector(fread("keep_list_PCAR_d6_sc250.csv")$x)
keep_listb <- as.vector(fread("keep_list_PCAR_d6_sc250b.csv")$x)

tempa <- keep_lista[1:250]
tempb <- keep_listb[1:250]
keep_list <- c(tempa,tempb)
for (i in c(seq(250,24750,250))){
  tempa <- keep_lista[(i+1):(i+250)]
  tempb <- keep_listb[(i+1):(i+250)]
  keep_list <-  c(keep_list,tempa)
  keep_list <-  c(keep_list,tempb)
}

trainData <- trainData[keep_list == TRUE,]
trainClass <- trainClass[keep_list == TRUE]

##########################################

rm(i, redClass, spectraCount, tempClass, reddim)
gc()

##########################################
# End of loading script
##########################################

start_time <- Sys.time()

acc_matrix <- matrix(c(0), nrow = 5, ncol = 60)
index <- seq(1,nrow(trainData),1)
for (i in 0:4) {
  print(paste("i = ",i))
  model <- plsda(trainData[index[index%%5 != i],],as.factor(trainClass[index[index%%5 != i]]),cv = NULL,ncomp = 60)
  labels <- as.factor(trainClass[index[index%%5 == i]])
  test_res <- predict(model, trainData[index[index%%5 == i],], labels)
  
  ypred <- test_res$y.pred
  
  for (j in 1:60){
    print(paste("i = ",i,", j = ",j))
    predlabels <- as.factor(apply(ypred[,j,],1,which.max))
    levels(predlabels) <- c(levels(predlabels),setdiff(levels(labels),levels(predlabels)))
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
#5.408002 hours

ggplot() +
  geom_line(aes(x = 1:60, y = apply(1-acc_matrix, 2, mean))) +
  labs(x = "Components", y = "Error rate")

ncomp <- which.min(apply(1-acc_matrix, 2, mean))

start_time <- Sys.time()
model <- plsda(trainData,as.factor(trainClass),cv = NULL,ncomp = ncomp)
end_time <- Sys.time()

end_time - start_time
#1.282857 hours 

start_time <- Sys.time()
test_res = predict(model, testData, as.factor(testClass))
end_time <- Sys.time()

end_time - start_time
#9.983981 mins

summary(test_res)

plotPredictions(test_res, ncomp = ncomp)

plotXResiduals(test_res, ncomp = ncomp)

confmat <- getConfusionMatrix(test_res, ncomp = ncomp)
confmat

accuracy <- sum(diag(confmat))/sum(confmat) * 100
accuracy
#55.93578%

showPredictions(test_res, ncomp = ncomp)

ypred <- test_res$y.pred

testClassfactor <- as.factor(testClass)
levels(testClassfactor) <- c(levels(testClassfactor),'12')
confusionMatrix(as.factor(testClass),as.factor(apply(ypred[,ncomp,],1,which.max))) #69,6%
