# 最大（平均）尿流率による排尿障害の判定

import csv

import numpy as np


with open('../output/info.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    data = [row for row in reader]
    datafile.close()

with open('../output/label.txt', 'r') as label_file:
    content = label_file.read()
    label_list = content.split('\n')
    label_file.close()

data = [[row[col] for row in data] for col in range(len(data[0]))]

n_code = data.pop(0)

n_data = np.array(data).astype(float)

binary_label_encodings = []

for label in label_list:
    if label == 'Normal':
        binary_label_encodings.append(0)
    else:
        binary_label_encodings.append(1)

u_total_list = n_data[2]
q_max_list = n_data[1]

correct_list = []
incorrect_list = []
unable_list = []

for i in range(len(n_code)):
    if u_total_list[i] > 200.:
        if q_max_list[i] > 15.:
            pred = 0
        else:
            pred = 1
    elif u_total_list[i] > 50.:
        expected_min_time = u_total_list[i] / q_max_list[i]
        if expected_min_time < 10.:
            pred = 0
        else:
            pred = 1
    else:
        unable_list.append(n_code[i])
        print(n_code[i], ' unable')
        continue

    if pred == binary_label_encodings[i]:
        correct_list.append(n_code[i])
        print(n_code[i], 'correct')
    else:
        incorrect_list.append(n_code[i])
        print(n_code[i], ' incorrect')

print('correct number: ', len(correct_list))
print('incorrect number: ', len(incorrect_list))
print('unable number: ', len(unable_list))

