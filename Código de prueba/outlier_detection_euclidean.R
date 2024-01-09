library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectres <- fread("train_samples.csv", dec = ',',header = TRUE)

spectres_processed <- fread("SNV1.csv", dec = ',',header = TRUE)

colnames(spectres_processed) <- colnames(spectres)

class <- read.csv2("train_samples_class.csv")

subset <- spectres_processed[class$trainClass == 1]

centroid <- spectres_processed[class$trainClass == 1,sapply(.SD,median)]

#https://stackoverflow.com/questions/46406029/data-table-minus-one-vector
#https://stackoverflow.com/questions/46843926/broadcasting-in-r
centered_subset <- subset[,Map(`-`, .SD, centroid)]#subset - t(centroid)

#distance <- centered_subset[,.(rowSums(.SD**2))]
distance <- centered_subset[,sqrt(rowSums(.SD**2))]


q <- quantile(distance,probs = c(0.05,0.95))

ggplot() + 
  geom_histogram(aes(x = distance)) +
  geom_vline(xintercept = q)