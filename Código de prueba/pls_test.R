library(tidyverse)
library(data.table)
library(mdatools)
library(rhdf5)
library(mlr)

#Prueba con dataset de menor dimensionalidad
#setwd("C://Users//tiama//OneDrive//Documentos//Maestría en minería y exploración de datos//Taller de Tesis 1//TT1//Datos procesados")

#df <- read.csv2("spc24Oct2019/Minería.csv")

#model <- plsda(df %>% select(where(is.numeric)),as.factor(df$Group),cv = list('ven', 5))

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectra <- fread("SNV1_downsampled.csv", dec = ',',header = TRUE)
class <- fread("train_samples_class.csv", dec = ',',header = TRUE)

#para usar con SNV.csv
#downsampled_spectra <- spectra %>% 
#  select(where(is.numeric)) %>% 
#  apply(1,decimate, q = 3) %>% 
#  t()

start_time <- Sys.time()
model <- plsda(spectra,as.factor(class$trainClass),cv = list('ven', 5))
end_time <- Sys.time()

end_time - start_time
#Tarda 7 minutos 

summary(model, ncomp = 17)

#https://wiki.eigenvector.com/index.php?title=Faq_what_are_reduced_T%5E2_and_Q_Statistics
plotXResiduals(model, ncomp = 17)

plotRMSE(model)

plotPredictions(structure(model, class = "regmodel"), ncomp = 17, ny = 3)

setwd("C:/Users/tiama/OneDrive/Documentos/Dataset EMSLIBS2019/")
##########################################
# Test Data
##########################################

testData <- h5read(file = "test_downsampled.h5", name = "UNKNOWN") # import spectra
h5closeAll()

test_class <- fread("test_labels.csv", dec = ',',header = FALSE)

##########################################
# Merge
##########################################


testData <- as.data.frame(do.call('rbind',testData))

##########################################
# End of loading script
##########################################

test_res = predict(model, testData, as.factor(test_class$V1))

summary(test_res)

plotPredictions(test_res, ncomp = 17)
#plotPredictions(test_res, res = "cv", ncomp = 17)

plotXResiduals(test_res, ncomp = 17)

getConfusionMatrix(test_res, ncomp = 17)

#pred <- test_res$c.pred

showPredictions(test_res, ncomp = 17)

pred_class <- test_res$c.pred
#c <- classres(test_res$c.pred,as.factor(test_class$V1))
#measureACC(predictions$class,df_test$Group)

#prueba con criterio de Wold y 50 componentes
modelb <- plsda(spectra,as.factor(class$trainClass),cv = list('ven', 5),ncomp = 50, ncomp.selcrit = 'wold')

summary(modelb)

plotRMSE(modelb)

test_resb = predict(modelb, testData, as.factor(test_class$V1))

summary(test_resb)