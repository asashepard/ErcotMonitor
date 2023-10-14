import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


class Data:

    def __init__(self):
        self.URL = 'https://www.ercot.com/content/cdr/html/real_time_system_conditions.html'
        self.nwd = 2  # non-website data, number of columns not scraped using URL
        self.categories = ['time',  # unique
                           'hourofday',
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
        self.last_update = []
        self.momentum = [0]*self.categories.__len__()
        self.continue_running = False

    def setup(self):
        self.continue_running = True
        with open('data.csv', 'r') as csvfile:
            csv_dict = [row for row in csv.DictReader(csvfile)]
            if len(csv_dict) != 0:
                self.df = pd.read_csv('data.csv')  # put csv into dataframe
        self.last_update.clear()
        if self.df.__len__() > 0:
            for i in self.df.loc[len(self.df.index) - 1]:  # 1: excludes index
                self.last_update.append(i)  # update last_update array with last dataframe entry

    def scrape_data(self):
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.text, 'lxml')

        table = soup.find('table')
        layer = [datetime.now().timestamp(), round(int(datetime.now().hour) + datetime.now().minute / 60 + datetime.now().second / 3600, 4)]
        for i in table.find_all('tr'):
            columns = i.find_all('td')
            if not columns:
                continue
            for j in columns:
                if j.text.strip().replace('.', '').replace('-', '').isnumeric():
                    layer.append(float(j.text.strip()))
        if self.last_update[self.nwd:] == layer[self.nwd:]:
            print('no change - dataframe not updated')
        else:
            # update dataframe
            self.df.loc[len(self.df)] = dict(zip(self.categories, layer))
            print('dataframe updated')
            # update csv
            self.df.to_csv('data.csv', sep=',', index=False, encoding='utf-8')
            for i in range(self.nwd, self.last_update.__len__()):
                if self.last_update[i] < layer[i]:  # increasing
                    if self.momentum[i] <= 0:
                        self.momentum[i] = 0
                    else:
                        self.momentum[i] += 1
                elif self.last_update[i] > layer[i]:  # decreasing
                    if self.momentum[i] <= 0:
                        self.momentum[i] -= 1
                    else:
                        self.momentum[i] = 0

            self.last_update = layer
