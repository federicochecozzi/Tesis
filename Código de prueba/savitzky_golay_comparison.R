library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectra <- fread("train_samples.csv", dec = ',',header = TRUE)

savgol1 <- fread("savgol1.csv", dec = ',',header = TRUE)

colnames(savgol1) <- colnames(spectra)

savgol2 <- fread("savgol2.csv", dec = ',',header = TRUE)

colnames(savgol2) <- colnames(spectra)

savgol3 <- fread("savgol3.csv", dec = ',',header = TRUE)

colnames(savgol3) <- colnames(spectra)

df <- bind_rows("spectrum" = spectra,"p = 2, w = 5" = savgol1,
                "p = 2, w = 11" = savgol2,"p = 6, w = 21" = savgol3,.id ="id")

pdf("savgol.pdf")

for (i in 1:100) {
  print(i)
  p <- df[c(0 + i,100 + i,200 + i,300 + i),] %>% 
    pivot_longer(!id,names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength), 
           alpha = ((id == "spectrum") * 0.4 + (id != "spectrum") * 0.8)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity, color = id, alpha = alpha))
  print(p)
}

dev.off()
