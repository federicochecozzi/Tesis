library(tidyverse)
library(data.table)
library(caret)
library(mdatools)
library(rhdf5)

#setwd(r"(C:\Users\Federico Checozzi\Documents\Tesis\Código de prueba\output)")
setwd(r"(C:\Users\Federico Checozzi\Documents\Tesis\Datasets)")

#Data <- fread("SNVFeCo.csv") 
#Target <- fread("comp_FeCo.csv")
Data <- as.data.table(t(h5read(file = "catalina_processed_and_downsampled_with_target.h5", name = "spectra")))
Target <- as.data.table(t(h5read(file = "catalina_processed_and_downsampled_with_target.h5", name = "target")))

#lidiar con los nombres de variables!

#V1: sample, V2,V3: Fe_comp, Co_comp
samples <- c(3,8)
trainData <- Data[Target$V1 %in% samples,]
trainTarget <- Target[V1 %in% samples,.(V2, V3)]

testData <- Data[!Target$V1 %in% samples,]
testTarget <- Target[!V1 %in% samples,.(V2, V3)]

model = pls(as.matrix(trainData), as.matrix(trainTarget), cv = NULL, x.test = as.matrix(testData), y.test = as.matrix(testTarget))
#model = selectCompNum(model, 2)
summary(model)
plot(model)

