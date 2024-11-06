library(tidyverse)
library(data.table)

setwd(r"(C:\Users\tiama\OneDrive\Documentos\Maestría en minería y exploración de datos\Tesis de maestría\Scripts\Código de prueba\output)")

#spectra <- fread("train_samples.csv", dec = ',',header = TRUE)

#obs <- rownames(spectra)
#spectra <- cbind(spectra,obs)

SNV1 <- fread("SNV1.csv", dec = ',',header = TRUE)

#SNV1 <- cbind(SNV1,obs)
#colnames(SNV1) <- colnames(spectra)

SNV1a <- fread("SNV1_downsampledby4.csv", dec = ',',header = TRUE)

#SNV1a <- cbind(SNV1a,obs)
#colnames(SNV1a) <- colnames(spectra)

SNV1b <- fread("SNV1_downsampledby5.csv", dec = ',',header = TRUE)

#SNV1b <- cbind(SNV1b,obs)
#colnames(SNV1b) <- colnames(spectra)

SNV1c <- fread("SNV1_downsampledby6.csv", dec = ',',header = TRUE)

#SNV1c <- cbind(SNV1c,obs)
#colnames(SNV1c) <- colnames(spectra)

SNV1d <- fread("SNV1_downsampledby8.csv", dec = ',',header = TRUE)

#SNV1d <- cbind(SNV1d,obs)
#colnames(SNV1d) <- colnames(spectra)

SNV1e <- fread("SNV1_downsampledby10.csv", dec = ',',header = TRUE)

#SNV1e <- cbind(SNV1e,obs)
#colnames(SNV1e) <- colnames(spectra)

SNV1f <- fread("SNV1_downsampledby20.csv", dec = ',',header = TRUE)

#SNV1f <- cbind(SNV1f,obs)
#colnames(SNV1f) <- colnames(spectra)

SNV1g <- fread("SNV1_downsampledby30.csv", dec = ',',header = TRUE)

#SNV1g <- cbind(SNV1g,obs)
#colnames(SNV1g) <- colnames(spectra)

SNV1h <- fread("SNV1_downsampledby39.csv", dec = ',',header = TRUE)

#SNV1h <- cbind(SNV1h,obs)
#colnames(SNV1h) <- colnames(spectra)

pdf("SNV_nod.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d4.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1a[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d5.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1b[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d6.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1c[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d8.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1d[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d10.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1e[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d20.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1f[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d30.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1g[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()

pdf("SNV_d39.pdf")

for (i in c(1,50,100)){
  print(i)
  p <- SNV1h[i,] %>%
    pivot_longer(everything(),names_to = "Wavelength", values_to = "Intensity") %>%
    mutate(Wavelength = as.numeric(Wavelength)) %>%
    ggplot() + 
    geom_line(aes(x = Wavelength , y = Intensity)) +
    theme(legend.position = "none")
  print(p)
}

dev.off()