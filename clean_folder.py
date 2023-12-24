import os
import shutil
import argparse
import sys


def main(folder):
    ls = os.listdir(folder)
    if not ls:
        print(f'Директория {folder} уже пустая')
        return

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    print(f'Директория {folder} успешно очищена')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f")
    args = parser.parse_args(sys.argv[1:])
    if args.f is not None:
        main(args.f)
    else:
        print('Укажите путь очищаемой директории!')
