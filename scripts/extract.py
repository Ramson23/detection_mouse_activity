import pandas as pd
import os
from utils.check_file import check_processed_file
from utils.extractor import Extractor

main_dir = '../new_jajj'
os.chdir(main_dir)

all_mouse_file = check_processed_file(os.listdir('./new_mouse_data'), 'new_extracted_data', main_dir)

print(all_mouse_file)

for file in all_mouse_file:

    df = pd.read_csv('./new_mouse_data/' + file)
    exc = Extractor(df)
    df_out = exc.extract()

    df_out.to_csv('./new_extracted_data/' + file, index=False)
    print('Файл new_extracted_data/' + file + ' успешно обработан')
