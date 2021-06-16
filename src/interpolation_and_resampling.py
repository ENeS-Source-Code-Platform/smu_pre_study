import csv
import os
import numpy as np
import matplotlib.pyplot as plt

from util.preproccessing import curve_handler

raw_data = []

with open('../source_data/raw.csv', 'r', encoding='utf-8-sig') as raw:
    csv_reader = csv.reader(raw)
    rows = [row for row in csv_reader]
    raw_data = rows
    raw.close()

valid_number_list = []
valid_label_list =[]

processed_curve_container = {}
urination_time_container = {}
q_max_container = {}
u_total_container = {}


resampling_frequency = 400

for data in raw_data:
    number = data[0]
    label = data[12]
    f_name = '../source_data/plot_data/' + str(number) + '.csv'
    if os.path.exists(f_name) & os.path.isfile(f_name):
        print(f_name + ' exists')
        curve_raw_data = np.loadtxt(f_name, encoding='utf-8-sig', delimiter=',', skiprows=0).T
        if curve_raw_data.shape[0] != 2:
            print('dimension error')
            break
        else:
            curve_raw_data_x = curve_raw_data[0]
            curve_raw_data_y = curve_raw_data[1]

            processed_curve_container[number], urination_time_container[number], \
                q_max_container[number], u_total_container[number] = \
                curve_handler(curve_raw_data_x, curve_raw_data_y, resampling_frequency)

            valid_number_list.append(number)
            valid_label_list.append(label)
    else:
        print(f_name + ' not exists')

with open('../output/curves.csv', 'w') as curve_datafile:
    csv_writer = csv.writer(curve_datafile)
    for valid_number in valid_number_list:
        csv_writer.writerow(processed_curve_container[valid_number])

        # save plots into image file
        x = range(resampling_frequency)
        y = processed_curve_container[valid_number]
        plt.plot(x, y, color='black', linewidth=1)
        plt.savefig('../output/figs/' + valid_number + '.jpg')
        plt.show()

    curve_datafile.close()

with open('../output/label.txt', 'w') as label_datafile:
    for valid_label in valid_label_list:
        label_datafile.write(valid_label + '\n')
    label_datafile.close()

with open('../output/info.csv', 'w') as info_datafile:
    csv_writer = csv.writer(info_datafile)
    for valid_number in valid_number_list:
        info = [
                valid_number,
                urination_time_container[valid_number],
                q_max_container[valid_number],
                u_total_container[valid_number]
        ]
        csv_writer.writerow(info)
    info_datafile.close()
