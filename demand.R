ercot <- read.csv("data.csv")
last_milli <- tail(ercot$time, n = 1)
ercot <- ercot[ercot$time > last_milli - 3600, ]  # 3600 = ~1 hour
lm.demand <- lm(formula = Actual.System.Demand ~ hourofday, data = ercot)
summary(lm.demand)