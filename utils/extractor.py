import pandas as pd
from statistics import median

from utils.geometry_operations import (
    get_dist,
    get_dist_point_line,
    get_angle_between_vector,
)

"""
В этом классе происходит выделение признаков из сырых данных. Сырые данные разделены на участки,
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


class Extractor:
    output_columns = [
        'section_count_before',
        'section_count_after',
        'angle_max1',
        'angle_max2',
        'angle_max3',
        'angle_max4',
        'angle_max5',
        'angle_median',
        'angle_average',
        'section_max1',
        'section_max2',
        'section_max3',
        'section_max4',
        'section_max5',
        'section_median',
        'section_average',
        'square_line',
        'square',
        'time',
        'time_max1',
        'time_max2',
        'time_max3',
        'time_max4',
        'time_max5',
        'time_median',
        'time_average',
        'condition',
    ]

    def __init__(self, df_default):
        self.df_default = df_default
        self.df_out = pd.DataFrame(columns=Extractor.output_columns)

        self.df_union = None

    def extract(self, threshold_union=7):

        self.df_union = Extractor.union_same_angle(self.df_default)

        ls_default = Extractor.extract_segments(self.df_default)
        ls_union = Extractor.extract_segments(self.df_union)

        for union_seg, default_seg in zip(ls_union, ls_default):
            section_count_before = len(default_seg) - 1
            section_count_after = len(union_seg) - 1
            (max_section_1,
             max_section_2,
             max_section_3,
             max_section_4,
             max_section_5,
             median_section,
             average_section,
             ) = Extractor.calculate_section(union_seg)
            (max_angle_1,
             max_angle_2,
             max_angle_3,
             max_angle_4,
             max_angle_5,
             median_angle,
             average_angle,
             ) = Extractor.calculate_angle(union_seg)

            (square_line,
             square,
             ) = Extractor.calculate_square(default_seg)

            (time,
             max_time_1,
             max_time_2,
             max_time_3,
             max_time_4,
             max_time_5,
             time_median,
             time_average
             ) = Extractor.calculate_time(union_seg)
            condition = Extractor.calculate_condition(union_seg)
            exc_row = [
                [section_count_before,
                 section_count_after,
                 max_angle_1,
                 max_angle_2,
                 max_angle_3,
                 max_angle_4,
                 max_angle_5,
                 median_angle,
                 average_angle,
                 max_section_1,
                 max_section_2,
                 max_section_3,
                 max_section_4,
                 max_section_5,
                 median_section,
                 average_section,
                 square_line,
                 square,
                 time,
                 max_time_1,
                 max_time_2,
                 max_time_3,
                 max_time_4,
                 max_time_5,
                 time_median,
                 time_average,
                 condition
                 ]
            ]
            self.df_out = pd.concat(
                [self.df_out,
                 pd.DataFrame(data=exc_row, columns=Extractor.output_columns)],
                ignore_index=True
            )
        return self.df_out

    def separate_activity_segment(self, threshold=3000):
        """
        В этом методе большие сегменты разделяются на малые относительно времени между сегментами
        """
        first_row = self.df_default.iloc[[0]]
        t_prev = first_row['T'].iloc[0]
        marker_prev = first_row.Marker.iloc[0]

        for i in range(1, self.df_default.shape[0]):

            row = self.df_default.iloc[[i]]
            t_cur = row['T'].iloc[0]
            marker_cur = row.Marker.iloc[0]

            if marker_prev == 'normal' and marker_cur == 'normal':
                if t_cur - t_prev >= threshold:
                    self.df_default.loc[i, ['Marker']] = 'start'
                    self.df_default.loc[i - 1, ['Marker']] = 'stop'

            t_prev = t_cur
            marker_prev = marker_cur

        self.df_default = Extractor.clean_data_df(self.df_default)

    @staticmethod
    def union_same_angle(df, threshold=7):
        """
        В этом методе происходит сокращение исходного датасета путем
        объединения нескольких отрезков в один при условии изменения их угла
        не больше, чем на threshold
        """
        first_row = df.iloc[[0]]
        x_prev = first_row.X.iloc[0]
        y_prev = first_row.Y.iloc[0]

        union_df = pd.DataFrame(data=first_row)

        for i in range(1, df.shape[0]):

            row = df.iloc[[i]]

            if (i + 1) < df.shape[0]:
                next_row = df.iloc[[i + 1]]

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

                    angle_between = get_angle_between_vector(
                        x_curr - x_prev,
                        y_curr - y_prev,
                        x_next - x_curr,
                        y_next - y_curr
                    )

                    if angle_between > threshold:
                        union_df = pd.concat([union_df, row], ignore_index=True)
                        x_prev = x_curr
                        y_prev = y_curr
            else:
                union_df = pd.concat([union_df, row], ignore_index=True)

        return union_df

    @staticmethod
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

    @staticmethod
    def calculate_section(notes):
        secs = []
        for i in range(len(notes) - 1):
            x_1 = notes[i].X
            y_1 = notes[i].Y
            x_2 = notes[i + 1].X
            y_2 = notes[i + 1].Y
            curr_sec = get_dist(x_1, y_1, x_2, y_2)
            secs.append(curr_sec)
        secs.sort(reverse=True)

        if len(secs) < 5:
            max_secs = secs[:]
            max_secs.extend([0] * (5 - len(secs)))
        else:
            max_secs = secs[:5]

        if len(secs) == 0:
            return (
                *max_secs,
                0,
                0
            )
        else:
            return (
                *max_secs,
                median(secs),
                (sum(secs) / (len(secs))),
            )

    @staticmethod
    def calculate_angle(notes):
        angels = []
        for i in range(len(notes) - 2):
            x_1 = notes[i].X
            y_1 = notes[i].Y
            x_2 = notes[i + 1].X
            y_2 = notes[i + 1].Y
            x_3 = notes[i + 2].X
            y_3 = notes[i + 2].Y

            curr_angle = get_angle_between_vector(x_2 - x_1, y_2 - y_1, x_3 - x_2, y_3 - y_2)
            angels.append(curr_angle)

        angels.sort(reverse=True)

        if len(angels) < 5:
            max_angels = angels[:]
            max_angels.extend([0] * (5 - len(angels)))
        else:
            max_angels = angels[:5]

        if len(angels) == 0:
            return (
                *max_angels,
                0,
                0
            )
        return (
            *max_angels,
            median(angels),
            (sum(angels) / (len(angels))),
        )

    @staticmethod
    def calculate_square(notes):
        line_x_1 = notes[0].X
        line_y_1 = notes[0].Y
        line_x_2 = notes[-1].X
        line_y_2 = notes[-1].Y

        sum_dist = 0
        for el in notes:
            if el.Marker == 'normal':
                sum_dist += get_dist_point_line(el.X, el.Y, line_x_1, line_y_1, line_x_2, line_y_2)

        return (
            get_dist(line_x_1, line_y_1, line_x_2, line_y_2),
            sum_dist,
        )

    @staticmethod
    def calculate_time(notes):
        times = []
        for i in range(len(notes) - 1):
            times.append(notes[i + 1]['T'] - notes[i]['T'])

        times.sort(reverse=True)

        if len(times) < 5:
            max_times = times[:]
            max_times.extend([0] * (5 - len(times)))
        else:
            max_times = times[:5]

        if len(times) == 0:
            return (
                *max_times,
                0,
                0
            )
        return (
            (notes[-1]['T'] - notes[0]['T']),
            *max_times,
            median(times),
            (sum(times) / len(times))
        )

    @staticmethod
    def calculate_condition(notes):
        return notes[0].Condition

    @staticmethod
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
