from tkinter import *
from tkinter import ttk
import pyautogui
import time
import pandas as pd
from multiprocessing import *
from datetime import datetime
import os


def btnstr_click(event):
    global start, num_txt_curr
    start.value = 1
    txt_curr_proc.set("Данные собираются...")
    p = Process(target=record_data, args=(num_txt_curr, start))
    p.start()


def btnstop_click():
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


def record_data(num, st):
    data = [[0, 0, 0, 0, 0]]
    columns = ['Date', 'TimeStamp', 'X', 'Y', 'Condition']

    begin = time.time_ns()
    old = begin
    try:
        while st.value == 1:
            current = time.time_ns()
            if current - old > 1000:
                x, y = pyautogui.position()
                if not (x == data[-1][2] and y == data[-1][3]):
                    data.append([str(datetime.now()), (current - begin) / 1000000, x, y, num.value])
                old = current
    except:
        print('\n')
    finally:
        print('Данные собраны')
        df = pd.DataFrame(data, columns=columns)
        os.makedirs('mouse_data', exist_ok=True)
        df.to_csv('mouse_data/' + datetime.now().strftime("%H.%M.%S_%Y-%m-%d") + '.csv')


if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')
    start = Value('i', 0)
    num_txt_curr = Value('i', 0)

    root = Tk()
    root.title('Движение мышки ')
    root.geometry('500x400')

    main_frame = Frame(root)
    main_frame.pack(expand=True)

    label = Label(main_frame, text='Убедитесь, что перед запуском программы \nфайл mouse_data.csv не открыт.')
    label.grid(column=0, row=2)

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

    stop_button = Button(start_stop_frame, text='Стоп', bg='#FC4242', command=btnstop_click)
    stop_button.grid(column=1, row=0)

    txt_curr_proc = StringVar(value='Ожидание запуска...')
    lbl_curr_proc = Label(start_stop_frame, textvariable=txt_curr_proc)
    lbl_curr_proc.grid(column=0, columnspan=2, row=1)

    root.mainloop()
