import pyautogui
import time
from pynput import mouse
import pandas as pd
from datetime import datetime
import os

from multiprocessing import Process, Queue


class Recorder(Process):
    data_column = ['Date', 'X', 'Y', 'T', 'Marker', 'Condition']

    def __init__(self, condition, needed_count):
        super().__init__()

        self.q_data = Queue()
        self.data = []
        self.all_data = []

        self.q_changes = Queue()
        self.condition = condition
        self.run_flag = True

        self.needed_count = needed_count
        self.fragments_count = 0

    def run(self):
        def on_click(x_in, y_in, button, pressed):
            nonlocal marker
            if button == mouse.Button.left:
                if pressed:
                    marker = 'stop'
                    self.data.append(
                        [str(datetime.now()),
                         x_in,
                         y_in,
                         (time_current - time_initial) / 1000000,
                         marker,
                         self.condition
                         ]
                    )
                    self.fragments_count += 1
                    if self.fragments_count >= self.needed_count:
                        self.q_data.put(self.data)
                        self.all_data.extend(self.data)
                        self.data = []
                        self.fragments_count = 0

                else:
                    marker = 'start'

        listener = mouse.Listener(on_click=on_click)
        listener.start()

        time_initial = time.time_ns()
        x_old, y_old = pyautogui.position()
        sx, sy = x_old, y_old

        self.data = [[str(datetime.now()), x_old, y_old, 0, 'start', self.condition]]

        marker = 'normal'
        try:
            while self.run_flag:
                if not self.q_changes.empty():
                    self.run_flag, self.condition = self.q_changes.get()
                time_current = time.time_ns()
                x, y = pyautogui.position()
                if not (x == x_old and y == y_old):
                    x_old, y_old = x, y
                    if marker == 'normal':
                        if (x - sx) ** 2 + (y - sy) ** 2 > 100:
                            sx, sy = x, y
                            self.data.append(
                                [str(datetime.now()),
                                 x,
                                 y,
                                 (time_current - time_initial) / 1000000,
                                 marker,
                                 self.condition]
                            )
                    elif marker == 'start':
                        self.data.append(
                            [str(datetime.now()),
                             x,
                             y,
                             (time_current - time_initial) / 1000000,
                             marker,
                             self.condition]
                        )
                        marker = 'normal'
        except:
            print('Выполнение закончилось')
        finally:
            self.all_data.extend(self.data)
            self.all_data[-1][-2] = 'stop'  # присваиваем последнему маркеру значение stop
            #print('Данные собраны')
            self.clean_data()
            df = pd.DataFrame(self.all_data, columns=self.data_column)
            os.makedirs('./new_jajj/new_mouse_data', exist_ok=True)
            df.to_csv('./new_jajj/new_mouse_data/' + datetime.now().strftime("%H.%M.%S_%Y-%m-%d") + '.csv', index=False)

    def clean_data(self):
        n = len(self.all_data) - 1
        i = 0
        while i < n:
            if self.all_data[i][4] == 'start' and self.all_data[i + 1][4] == 'stop':
                self.all_data.pop(i)
                self.all_data.pop(i)
                n -= 2
            else:
                i += 1

    @staticmethod
    def convert_to_df(data):
        return pd.DataFrame(data, columns=Recorder.data_column)
