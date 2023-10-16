ercot <- read.csv("data.csv")
last_hour <- tail(ercot$hourofday, n = 1)
ercot <- ercot[ercot$hourofday > last_hour - 3 & ercot$hourofday < last_hour, ]
lm.capacity <- lm(formula = Total.System.Capacity ~ hourofday + Current.Frequency + Instantaneous.Time.Error + Actual.System.Demand + Average.Net.Load + Total.Wind.Output + Total.PVGR.Output + Current.System.Inertia, data = ercot)
summary(lm.capacity)