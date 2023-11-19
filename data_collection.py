from tkinter import *
from tkinter import ttk
import pyautogui
import time
from pynput import mouse
import pandas as pd
from multiprocessing import *
from datetime import datetime
import os

'''
В этом файле происходит сбор данных и создание csv файла.
'''
'''
Заметки:
Отрезок активности измеряется от клика до клика мыши.
'''


def btnstr_click(event):
    global start, num_txt_curr
    start.value = 1
    txt_curr_proc.set("Данные собираются...")
    p = Process(target=record_data, args=(num_txt_curr, start))
    p.start()


def btnstop_click(event):
    global start
    start.value = 0
    txt_curr_proc.set('Данные собраны и сохранены')


def btn0_click():
    txt_curr.set('Уставший')
    global num_txt_curr
    num_txt_curr.value = 0


def btn1_click():
    txt_curr.set('Бодрый')
    global num_txt_curr
    num_txt_curr.value = 1


def clean_data(data):
    n = len(data) - 1
    i = 0
    while i < n:
        if data[i][4] == 'start' and data[i + 1][4] == 'stop':
            data.pop(i)
            data.pop(i)
            n -= 2
        else:
            i += 1


def record_data(num, st):
    def on_click(x_in, y_in, button, pressed):
        nonlocal marker
        if button == mouse.Button.left:
            if pressed:
                marker = 'stop'
                data.append(
                    [str(datetime.now()), x_in, y_in, (time_current - time_initial) / 1000000, marker, num.value])
            else:
                marker = 'start'

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    time_initial = time.time_ns()
    x_old, y_old = pyautogui.position()
    sx, sy = x_old, y_old

    data_column = ['Date', 'X', 'Y', 'T', 'Marker', 'Condition']
    data = [[str(datetime.now()), x_old, y_old, 0, 'start', num.value]]

    marker = 'normal'

    try:
        while st.value == 1:
            time_current = time.time_ns()
            x, y = pyautogui.position()
            if not (x == x_old and y == y_old):
                x_old, y_old = x, y
                if marker == 'normal':
                    if (x - sx) ** 2 + (y - sy) ** 2 > 100:
                        sx, sy = x, y
                        data.append(
                            [str(datetime.now()), x, y, (time_current - time_initial) / 1000000, marker, num.value])
                elif marker == 'start':
                    data.append([str(datetime.now()), x, y, (time_current - time_initial) / 1000000, marker, num.value])
                    marker = 'normal'
    except:
        print('Выполнение закончилось')
    finally:
        data[-1][-2] = 'stop'  # присваиваем последнему маркеру значение stop
        print('Данные собраны')
        clean_data(data)
        df = pd.DataFrame(data, columns=data_column)
        os.makedirs('new_mouse_data', exist_ok=True)
        df.to_csv('new_mouse_data/' + datetime.now().strftime("%H.%M.%S_%Y-%m-%d") + '.csv', index=False)


if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')
    start = Value('i', 0)
    num_txt_curr = Value('i', 0)

    root = Tk()
    root.title('Движение мыши ')
    root.geometry('500x400')

    main_frame = Frame(root)
    main_frame.pack(expand=True)

    frame = ttk.Frame(main_frame, borderwidth=2, relief=SOLID, padding=[8, 10])
    frame.grid(column=0, row=0)
    title = Label(frame, text='Укажите свое состояние:')
    title.pack(anchor='n')
    button0 = Button(frame, text='Уставший', command=btn0_click)
    button0.pack(anchor='w', fill=X)
    button1 = Button(frame, text='Бодрый', command=btn1_click)
    button1.pack(anchor='e', fill=X)

    txt_curr = StringVar(value='Неопределено')
    ttl_curr = Label(frame, textvariable=txt_curr)
    ttl_curr.pack(side=BOTTOM)

    ttl_curr_condition = Label(frame, text='Текущее состояние:')
    ttl_curr_condition.pack(side=BOTTOM)

    start_stop_frame = ttk.Frame(main_frame, padding=[8, 10])
    start_stop_frame.grid(column=0, row=1)

    str_button = Button(start_stop_frame, text='Старт', bg='#3FFF6C')
    str_button.grid(column=0, row=0)
    str_button.bind('<ButtonPress>', btnstr_click)
    root.bind('s', lambda event: btnstr_click(None))

    stop_button = Button(start_stop_frame, text='Стоп', bg='#FC4242')
    stop_button.grid(column=1, row=0)
    stop_button.bind('<ButtonPress>', btnstop_click)
    root.bind('t', lambda event: btnstop_click(None))

    txt_curr_proc = StringVar(value='Ожидание запуска...')
    lbl_curr_proc = Label(start_stop_frame, textvariable=txt_curr_proc)
    lbl_curr_proc.grid(column=0, columnspan=2, row=1)

    root.mainloop()
