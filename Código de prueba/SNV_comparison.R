library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectra <- fread("train_samples.csv", dec = ',',header = TRUE)

obs <- rownames(spectra)
spectra <- cbind(spectra,obs)

SNV1 <- fread("SNV1.csv", dec = ',',header = TRUE)

SNV1 <- cbind(SNV1,obs)
colnames(SNV1) <- colnames(spectra)

SNV2 <- fread("SNV2.csv", dec = ',',header = TRUE)

SNV2 <- cbind(SNV2,obs)
colnames(SNV2) <- colnames(spectra)

#spectra %>%
#  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
#  mutate(Wavelength = as.numeric(Wavelength)) %>%
#  ggplot() + 
#  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
#  theme(legend.position = "none")

pdf("SNV_sample.pdf")

for (i in c(1,50,100)){
print(i)
p <- spectra[i,] %>%
    pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
    theme(legend.position = "none")
print(p)

p <- SNV1[i,] %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")
print(p)

p <- SNV2[i,] %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")
print(p)
}

dev.off()

pdf("SNV.pdf")

spectra %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")

SNV1 %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")

SNV2 %>%
  pivot_longer(!obs,names_to = "Wavelength", values_to = "Intensity") %>%
  mutate(Wavelength = as.numeric(Wavelength)) %>%
  ggplot() + 
  geom_line(aes(x = Wavelength , y = Intensity, color = obs)) +
  theme(legend.position = "none")

dev.off()
