library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectra <- fread("train_samples.csv", dec = ',',header = TRUE)

wav1 <- fread("wav1.csv", dec = ',',header = TRUE)

colnames(wav1) <- colnames(spectra)

wav2 <- fread("wav2.csv", dec = ',',header = TRUE)

colnames(wav2) <- colnames(spectra)

df <- bind_rows("spectrum" = spectra,"BayesShrink" = wav1,
                "VisuShrink" = wav2,.id ="id")

pdf("Soft_wavelet_sym7.pdf")

for (i in 1:100) {
  print(i)
  p <- df[c(0 + i,100 + i,200 + i),] %>% 
    pivot_longer(!id,names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength), 
           alpha = ((id == "spectrum") * 0.6 + (id != "spectrum") * 1)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity, color = id, alpha = alpha))
  print(p)
}

dev.off()
