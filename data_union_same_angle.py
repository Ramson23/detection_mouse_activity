from tkinter import *
from tkinter import ttk
import pyautogui
import time
import pandas as pd
from multiprocessing import *
from datetime import datetime
import math
import os

from check_file import check_processed_file
from geometry_operations import get_angle

"""
В этом файле происходит сокращение исходного датасета путем
объединения нескольких отрезков в один при условии изменения их угла
не больше, чем на threshold
"""

path = './'
lst_dir = os.listdir(path)
threshold = 10

if 'mouse_data' in lst_dir:

    all_mouse_file = check_processed_file(os.listdir('./mouse_data'), 'mouse_union')

    for mouse_file in all_mouse_file:

        df = pd.read_csv("mouse_data/" + mouse_file)

        first_row = df.iloc[[0]]
        x_prev = first_row.X.iloc[0]
        y_prev = first_row.Y.iloc[0]

        union_df = pd.DataFrame(data=first_row)

        for i in range(1, df.shape[0]):

            row = df.iloc[[i]]

            if (i + 1) < df.shape[0]:
                next_row = df.iloc[[i+1]]

                if row.Marker.iloc[0] == 'stop':
                    union_df = pd.concat([union_df, row], ignore_index=True)
                elif row.Marker.iloc[0] == 'start':
                    union_df = pd.concat([union_df, row], ignore_index=True)
                    x_prev = row.X.iloc[0]
                    y_prev = row.Y.iloc[0]
                else:
                    x_curr = row.X.iloc[0]
                    y_curr = row.Y.iloc[0]
                    x_next = next_row.X.iloc[0]
                    y_next = next_row.Y.iloc[0]

                    angle_prev = get_angle(x_prev, y_prev, x_curr, y_curr)
                    angle_curr = get_angle(x_curr, y_curr, x_next, y_next)

                    if abs(angle_curr - angle_prev) > threshold:
                        union_df = pd.concat([union_df, row], ignore_index=True)
                        x_prev = x_curr
                        y_prev = y_curr
            else:
                union_df = pd.concat([union_df, row], ignore_index=True)

        union_df.to_csv('mouse_union/' + mouse_file)
        print('Файл mouse_union/' + mouse_file + ' успешно сохранен')