import csv
import os
import numpy as np

from util.preproccessing import curve_handler

raw_data = []

with open('../source_data/raw.csv', 'r', encoding='utf-8-sig') as raw:
    csv_reader = csv.reader(raw)
    rows = [row for row in csv_reader]
    raw_data = rows
    raw.close()

processed_curve = {}

for data in raw_data:
    number = data[0]
    f_name = '../source_data/plot_data/' + str(number) + '.csv'
    if os.path.exists(f_name) & os.path.isfile(f_name):
        print(f_name + ' exists')
        curve_raw_data = np.loadtxt(f_name, delimiter=',', skiprows=0).T
        if curve_raw_data.shape[0] != 2:
            print('dimension error')
            break
        else:
            curve_raw_data_x = curve_raw_data[0]
            curve_raw_data_y = curve_raw_data[1]

            curve_handler(curve_raw_data_x, curve_raw_data_y)
    else:
        print(f_name + ' not exists')

    break