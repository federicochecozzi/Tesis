library(tidyverse)
library(data.table)
library(tidymodels)

#Prueba con dataset de menor dimensionalidad
#setwd("C://Users//tiama//OneDrive//Documentos//Maestría en minería y exploración de datos//Taller de Tesis 1//TT1//Datos procesados")

#df <- read.csv2("spc24Oct2019/Minería.csv")

#model <- plsda(df %>% select(where(is.numeric)),as.factor(df$Group),cv = list('ven', 5))

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectra <- fread("SNV1_downsampled.csv", dec = ',',header = TRUE)
class <- fread("train_samples_class.csv", dec = ',',header = TRUE)

spectra_and_class <- spectra[, class := class[,trainClass]]

result <- .convert_form_to_xy_fit("class~.",spectra_and_class)
