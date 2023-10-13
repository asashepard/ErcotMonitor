from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Data:

    def __init__(self):
        self.URL = 'https://www.ercot.com/content/cdr/html/real_time_system_conditions.html'
        self.categories = ['time',
                           'Current Frequency',
                           'Instantaneous Time Error',
                           'Consecutive BAAL Clock-Minute Exceedances',
                           'Actual System Demand',
                           'Average Net Load',
                           'Total System Capacity',
                           'Total Wind Output',
                           'Total PVGR Output',
                           'Current System Inertia',
                           'DC_E (East)',
                           'DC_L (Laredo VFT)',
                           'DC_N (North)',
                           'DC_R (Railroad)',
                           'DC_S (Eagle Pass)']
        self.df = pd.DataFrame(columns=self.categories)
        self.last_update = []  # todo get from csv if there
        self.momentum = [0]*self.categories.__len__()  # todo replace functionality with dataframe reference
        self.continue_running = False

    def setup(self):
        self.continue_running = True
        self.df.update(pd.read_csv('data.csv'))
        self.last_update.clear()
        if self.df.__len__() > 0:
            for i in self.df.iloc[self.df.__len__() - 1]:
                self.last_update.append(i)

    def scrape_data(self):
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.text, 'lxml')

        table = soup.find('table')
        layer = [datetime.now().timestamp()]
        for i in table.find_all('tr'):
            columns = i.find_all('td')
            if not columns:
                continue
            for j in columns:
                if j.text.strip().replace('.', '').replace('-', '').isnumeric():  # todo replace with regex
                    layer.append(j.text.strip())
        if self.last_update[1:] == layer[1:]:
            print('no change - dataframe not updated')
        else:
            # todo update dataframe
            # todo update csv
            print(layer)
            for i in range(1, self.last_update.__len__()):  # todo make way for momentum to be reset to 0
                if self.last_update[i] < layer[i]:  # increasing
                    if self.momentum[i] <= 0:
                        self.momentum[i] = 1
                    else:
                        self.momentum[i] += 1
                elif self.last_update[i] > layer[i]:  # decreasing
                    if self.momentum[i] <= 0:
                        self.momentum[i] -= 1
                    else:
                        self.momentum[i] = -1

            self.last_update = layer
