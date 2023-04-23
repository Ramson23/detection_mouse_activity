import numpy
import pandas as pd
import math
from statistics import mean
import os

def check_processed_file(all_mouse_file, group_size):

    os.makedirs('extracted_features', exist_ok=True)
    os.makedirs('extracted_features/size_group' + group_size, exist_ok=True)
    all_group_name = os.listdir('./extracted_features')

    file_in_group = []
    for group_name in all_group_name:
        if group_name == ('size_group' + group_size):
            file_in_group = os.listdir('./extracted_features' + '/' + group_name)

    final_mouse_file = []
    for mouse_file in all_mouse_file:
        if mouse_file not in file_in_group:
            final_mouse_file.append(mouse_file[:-8] + '.csv')

    return final_mouse_file


def get_angle(x_1, y_1, x_2, y_2):
    if x_2 == x_1:
        return 90 if y2 > y1 else 270

    alfa = math.atan(abs(y_2 - y_1) / abs(x_2 - x_1)) * 180 / math.pi
    if x_2 < x_1:
        if y_2 > y_1:
            alfa = 180 - alfa
        else:
            alfa = 180 + alfa
    else:
        if y_2 < y_1:
            alfa = 360 - alfa
    return alfa


def get_dist(x_1, y_1, x_2, y_2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


group_size = 20
path = './'
lst_dir = os.listdir(path)

if 'mouse_data' in lst_dir:

    all_mouse_file = os.listdir('./mouse_data')
    all_mouse_file = check_processed_file([(i[:-4] + '_exc.csv') for i in all_mouse_file], str(group_size))

    for mouse_file in all_mouse_file:

        columns = ['Average_Angle', 'Max_Angle', 'Std_Angle', 'Average_Dist', 'Max_Dist', 'Std_Dist', 'Average_Time',
                   'Max_Time', 'Std_Time', 'Condition']
        final_data = []

        count_characteristics = 5
        data = []  # 0 столбец - угол, 1 - изменение угла, 2 столбец - расстояние, 3 - время, 4 - состояние

        row_data = pd.read_csv('mouse_data/' + mouse_file)

        for i in range(row_data.shape[0] - 1):

            data.append([0] * count_characteristics)

            x1 = row_data.X[i]
            y1 = row_data.Y[i]
            t1 = row_data.TimeStamp[i]
            x2 = row_data.X[i + 1]
            y2 = row_data.Y[i + 1]
            t2 = row_data.TimeStamp[i + 1]
            c = row_data.Condition[i]

            data[i][0] = get_angle(x1, y1, x2, y2)
            if i == 0:
                data[i][1] = data[i][0]
            else:
                data[i][1] = abs(data[i][0] - data[i - 1][0])

            data[i][2] = get_dist(x1, y1, x2, y2)
            data[i][3] = t2 - t1
            data[i][4] = c

        data.pop(0)
        count = len(data)
        row = 0
        while count > 0:
            count -= group_size
            curr_group_size = group_size if (count // group_size) >= 0 else count % group_size

            final_data.append([0] * len(columns))
            # для добавления новых характеристик изменяется рендж массива и шаг массива
            # новые признаки добавляются  final_data[row][i+k]
            data_i = 0
            for i in range(0, 9, 3):
                data_i += 1
                curr_mass = []
                for data_row in data[row * group_size: row * group_size + curr_group_size]:
                    curr_mass.append(data_row[data_i])

                final_data[row][i] = mean(curr_mass)
                final_data[row][i + 1] = max(curr_mass)
                final_data[row][i + 2] = numpy.std(curr_mass)

            curr_mass = []
            for data_row in data[row * group_size: row * group_size + curr_group_size]:
                curr_mass.append(data_row[-1])
            final_data[row][-1] = 1 if curr_mass.count(1) >= curr_mass.count(0) else 0
            row += 1

        df = pd.DataFrame(final_data, columns=columns)
        df.to_csv('extracted_features/size_group' + str(group_size) + '/' + mouse_file[:-4] + '_exc.csv')
        print('Файл ' + 'extracted_features/size_group' + str(group_size) + '/' + mouse_file[:-4] + '_exc.csv', 'сохранен')
