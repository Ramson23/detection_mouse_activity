import os

def check_processed_file(unprocessed_mouse_file, dir_name):

    os.makedirs(dir_name, exist_ok=True)
    existed_mouse_file = os.listdir('./' + dir_name)

    for i, file in enumerate(unprocessed_mouse_file):
        unprocessed_mouse_file[i] = file[:-4]

    for i, file in enumerate(existed_mouse_file):
        existed_mouse_file[i] = file[:-4]

    final_mouse_file = []
    for file in unprocessed_mouse_file:
        if file not in existed_mouse_file:
            final_mouse_file.append(file + '.csv')

    return final_mouse_file