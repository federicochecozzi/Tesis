library(tidyverse)
library(data.table)

setwd(r"(C:\Users\Federico Checozzi\Documents\Tesis\Código de prueba\output)")

#spectra <- fread("train_samples.csv", dec = ',',header = TRUE)

#obs <- rownames(spectra)
#spectra <- cbind(spectra,obs)

SNV <- fread("SNVFeCo.csv", dec = ',',header = TRUE)

obs <- rownames(SNV)
SNV <- cbind(SNV,obs)
#colnames(SNV) <- colnames(spectra)

pdf("SNVFeCo_sample.pdf")

for (i in c(1,50,100)){
  print(i)
  
  p <- SNV[i,] %>%
    pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNVFeCo.pdf")

SNV %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")

dev.off()