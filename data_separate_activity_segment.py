import pandas as pd
import os
import sys

from check_file import check_processed_file

"""
В этом файле большие сегменты разделяются на малые относительно времени между сегментами
"""

path = './'
lst_dir = os.listdir(path)
if len(sys.argv) > 1:
    threshold = int(sys.argv[1])
else:
    threshold = 3000


def clean_data_df(df):
    n = df.shape[0] - 1
    i = 0
    while i < n:
        if df.iloc[i][4] == 'start' and df.iloc[i + 1][4] == 'stop':
            df = df.drop([i, i + 1])
            df = df.reset_index(drop=True)
            n -= 2
        else:
            i += 1

    return df


if __name__ == '__main__':
    if 'new_mouse_data' in lst_dir:

        all_mouse_file = check_processed_file(os.listdir('./new_mouse_data'), 'new_mouse_data_sep')

        for mouse_file in all_mouse_file:

            df = pd.read_csv("new_mouse_data/" + mouse_file)

            first_row = df.iloc[[0]]
            t_prev = first_row['T'].iloc[0]
            marker_prev = first_row.Marker.iloc[0]

            for i in range(1, df.shape[0]):

                row = df.iloc[[i]]
                t_cur = row['T'].iloc[0]
                marker_cur = row.Marker.iloc[0]

                if marker_prev == 'normal' and marker_cur == 'normal':
                    if t_cur - t_prev >= threshold:
                        df.loc[i, ['Marker']] = 'start'
                        df.loc[i - 1, ['Marker']] = 'stop'

                t_prev = t_cur
                marker_prev = marker_cur

            df = clean_data_df(df)
            df.to_csv('new_mouse_data_sep/' + mouse_file, index=False)
            print('Файл new_mouse_data_sep/' + mouse_file + ' успешно сохранен')
