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

trainData <- Data[Target$sample %in% c(1,2,3,4,6,7,8,9,10),]
trainTarget <- Target[sample %in% c(1,2,3,4,6,7,8,9,10),.(Fe_comp, Co_comp)]

testData <- Data[!Target$sample %in% c(1,2,3,4,6,7,8,9,10),]
testTarget <- Target[!sample %in% c(1,2,3,4,6,7,8,9,10),.(Fe_comp, Co_comp)]

model = pls(trainData, trainTarget, cv = NULL, x.test = testData, y.test = testTarget)
#model = selectCompNum(model, 2)
summary(model)
plot(model)

