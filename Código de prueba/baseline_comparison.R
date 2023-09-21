library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

spectres <- fread("train_samples.csv", dec = ',',header = TRUE)

imodpoly <- fread("df_imodpoly.csv", dec = ',',header = TRUE)

colnames(imodpoly) <- colnames(spectres)

goldindec <- fread("df_goldindec.csv", dec = ',',header = TRUE)

colnames(goldindec) <- colnames(spectres)

mwmv <- fread("df_mwmv.csv", dec = ',',header = TRUE)

colnames(mwmv) <- colnames(spectres)

df <- bind_rows("spectre" = spectres,"imodpoly" = imodpoly,
          "goldindec" = goldindec,"mwmv" = mwmv,.id ="id")

pdf("baselines.pdf")

for (i in 1:100) {
  p <- df[c(0 + i,100 + i,200 + i,300 + i),] %>% 
    pivot_longer(!id,names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity, color = id), alpha = 0.5)
  print(p)
}

dev.off()
