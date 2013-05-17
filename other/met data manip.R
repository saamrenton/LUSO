
metdat <- read.table('Kapundamet.txt',header=TRUE)
head(metdat)

yrsused <- c(10:12,15:58,60:66,68:111 )+1900
yrsusedi <- yrsused - 1900 +12
length(yrsused)

metdat$summeryr <- metdat$year
metdat$summeryr[metdat$day>=336] <- metdat$summeryr[metdat$day>=336] + 1

#metdat <- subset(metdat,year %in% yrsused)

seq(60,365,92)

summerdat <- subset(metdat,day<60 | day >= 336)
summersum <- with(summerdat,tapply(rain,as.factor(summeryr),sum))

winterdat <- subset(metdat,day<244 | day >= 152)
wintersum <- with(winterdat,tapply(rain,as.factor(year),sum))

meanloginc <- -0.033*summersum +3.8    
meaninc <- exp(meanloginc)
plot(meaninc)
plot(summersum , meaninc,xlab='summer rain',ylab='incidence %')

diseaseImpact <- 0.0008* summersum + 0.0003 * wintersum 
plot(summersum , diseaseImpact ,xlab='summer rain',ylab='impact %')
plot(wintersum , diseaseImpact ,xlab='winter rain',ylab='impact %')
mean(diseaseImpact )

forfile <- cbind(meaninc ,diseaseImpact )
forfile <- forfile [yrsusedi ,]

write.csv(forfile ,'forfile.csv')









