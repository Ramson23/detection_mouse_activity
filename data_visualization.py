import pandas as pd
import os
from PIL import Image, ImageDraw

from check_file import check_processed_file

def create_picture(file_name, source_dir_name, cont_dir_name):

    path = source_dir_name + '/' + file_name
    data = pd.read_csv(path)

    white = (255, 255, 255)

    image = Image.new("RGB", (1920, 1080), white)
    draw = ImageDraw.Draw(image)

    for i in range(data.shape[0]):
        row = data.iloc[i]

        if row.Marker == 'start' or row.Marker == 'stop':
            draw.ellipse([(row.X - 10, row.Y - 10), (row.X + 10, row.Y + 10)], fill='green', outline='green')
        else:
            draw.ellipse([(row.X - 5, row.Y - 5), (row.X + 5, row.Y + 5)], fill='red', outline='green')

        if (i + 1) < data.shape[0]:
            next_row = data.iloc[i + 1]
            draw.line([row.X, row.Y, next_row.X, next_row.Y], fill='black')

    filename = cont_dir_name + '/' + file_name[:-4] + ".jpg"
    image.save(filename)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    default_files = check_processed_file(os.listdir('./mouse_data'), 'draw_path/default')
    union_files = check_processed_file(os.listdir('./mouse_union'), 'draw_path/union')

    print('Обрабатываемые файлы: ', default_files)

    for file in default_files:
        create_picture(file, 'mouse_data', 'draw_path/default')

    for file in union_files:
        create_picture(file, 'mouse_union', 'draw_path/union')