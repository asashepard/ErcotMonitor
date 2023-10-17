ercot <- read.csv("data.csv")
last_milli <- tail(ercot$time, n = 1)
ercot <- ercot[ercot$time > last_milli - 3600, ]  # 3600 = ~1 hour
lm.capacity <- lm(formula = Total.System.Capacity ~ hourofday, data = ercot)
summary(lm.capacity)