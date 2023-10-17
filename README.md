# ErcotMonitor

I was inspired to create this bot in early 2022 when Texas had been suffering power outages due to extreme weather.

The bot can provide visual, numerical, and easy historical tracking of the values made public by ERCOT, listed by typing "!ercot" in a Discord server channel.

![image](https://github.com/asashepard/ErcotMonitor/assets/78510770/905cf8b2-1db9-4068-8e4a-a32f85e427ae)

By typing "!ercotcreate" a live report is created which updates itself once per minute. The predicted changes in capacity and demand are calculated using a linear regression model through R.

![image](https://github.com/asashepard/ErcotMonitor/assets/78510770/5531f679-65d2-464e-a26c-bee47a05b4f6)

The bot also provides warnings when the frequency of the grid, the best indicator for whether the grid is in danger of collapse, approaches a low level. For demo and testing purposes, the normal values of 59.7 Hz for the warning indicator and 59.4 Hz for the warning ping were set to higher values.

![image](https://github.com/asashepard/ErcotMonitor/assets/78510770/d06b3bef-72d5-4e4a-b747-db30e17ad200)

![image](https://github.com/asashepard/ErcotMonitor/assets/78510770/02873fea-3443-45fd-8385-0fe53f72ba57)

For personal bot use, code can be compiled and hosted on any compatible computer or server. Future alterations might include considering factors like cloud coverage and historical data in a larger multiple linear regression prediction algorithm.
