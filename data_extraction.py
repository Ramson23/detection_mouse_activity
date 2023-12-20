import pandas as pd
import os
from statistics import median

from check_file import check_processed_file
from geometry_operations import (
    get_dist,
    get_dist_point_line,
    get_angle_between_vector,
)

"""
В этом файле происходит выделение признаков из сырых данных. Сырые данные разделены на участки,
начинающиеся с маркера start и заканчивающиеся маркером stop. Таким образом, одна строка таблицы признаков
представляет собой признаки, выделенные из одного участка.
Выделяемые признаки:
(mouse_union) 
    количество отрезков,
    максимальный угол (разница между текущим углом и предыдущим),
    длина максимального отрезка,
    средняя длина отрезков,
    время участка
(mouse_data)
    площадь (сумма отклонений каждой точки от прямой, соединяющей start и stop)
"""


def extract_segments(df):
    output_list = []
    internal_index = -1

    for i in range(df.shape[0]):

        row = df.iloc[i]
        if row.Marker == 'start':
            output_list.append([])
            internal_index += 1

        output_list[internal_index].append(row)

    return output_list


def calculate_section(notes):
    secs = []
    for i in range(len(notes) - 1):
        x_1 = notes[i].X
        y_1 = notes[i].Y
        x_2 = notes[i + 1].X
        y_2 = notes[i + 1].Y
        curr_sec = get_dist(x_1, y_1, x_2, y_2)
        secs.append(curr_sec)

    return (sum(secs) / (len(secs))), max(secs), median(secs)


def calculate_angle(notes):
    angle_max = 0
    for i in range(len(notes) - 2):
        x_1 = notes[i].X
        y_1 = notes[i].Y
        x_2 = notes[i + 1].X
        y_2 = notes[i + 1].Y
        x_3 = notes[i + 2].X
        y_3 = notes[i + 2].Y

        curr_angle = get_angle_between_vector(x_2 - x_1, y_2 - y_1, x_3 - x_2, y_3 - y_2)

        if curr_angle > angle_max:
            angle_max = curr_angle

    return angle_max


def calculate_square(notes):
    line_x_1 = notes[0].X
    line_y_1 = notes[0].Y
    line_x_2 = notes[-1].X
    line_y_2 = notes[-1].Y

    sum_dist = 0
    for el in notes:
        if el.Marker == 'normal':
            sum_dist += get_dist_point_line(el.X, el.Y, line_x_1, line_y_1, line_x_2, line_y_2)

    return sum_dist / (len(notes) - 2)


def calculate_time(notes):
    times = []
    for i in range(len(notes)-1):
        times.append(notes[i+1]['T'] - notes[i]['T'])

    return (notes[-1]['T'] - notes[0]['T']), median(times), (sum(times) / len(times))


def calculate_condition(notes):
    return notes[0].Condition


if __name__ == '__main__':

    output_columns = [
        'section_count_before',
        'section_count_after',
        'angle_max',
        'section_max_value',
        'section_average_value',
        'section_median_value',
        'square',
        'time',
        'time_median',
        'time_average',
        'condition',
    ]

    path = './'
    lst_dir = os.listdir(path)

    if 'mouse_union' in lst_dir:

        all_mouse_file = check_processed_file(os.listdir('./new_mouse_union'), 'new_extracted_data')

        for file in all_mouse_file:

            df_default = pd.read_csv('new_mouse_data/' + file)
            df_union = pd.read_csv('new_mouse_union/' + file)
            df_out = pd.DataFrame(columns=output_columns)

            ls_default = extract_segments(df_default)
            ls_union = extract_segments(df_union)

            for union_seg, default_seg in zip(ls_union, ls_default):
                section_count_before = len(default_seg) - 1
                section_count_after = len(union_seg) - 1
                average_section, max_section, median_section = calculate_section(union_seg)
                max_angle = calculate_angle(union_seg)
                square = calculate_square(default_seg)
                time, time_median, time_average = calculate_time(union_seg)
                condition = calculate_condition(union_seg)
                exc_row = [
                    [section_count_before,
                     section_count_after,
                     max_angle,
                     max_section,
                     average_section,
                     median_section,
                     square,
                     time,
                     time_median,
                     time_average,
                     condition
                     ]
                ]
                df_out = pd.concat([df_out, pd.DataFrame(data=exc_row, columns=output_columns)], ignore_index=True)

            df_out.to_csv('new_extracted_data/' + file, index=False)
            print('Файл new_extracted_data/' + file + ' успешно обработан')
