import os
import shutil
import filecmp

from pathlib import Path
from PIL import Image
from dotenv import load_dotenv

load_dotenv()


SUFFIX = 1


def get_capture_datetime(path):
    """Get capture datetime of photo."""
    ar = Image.open(path)._getexif()
    return ar[36868]


def make_dir(dest_dir_path, year, month):
    dir_path_year = dest_dir_path + '/' + year
    if not os.path.exists(dir_path_year):
        os.makedirs(dir_path_year)
    dir_path_month = dir_path_year + '/' + month
    if not os.path.exists(dir_path_month):
        os.makedirs(dir_path_month)


def get_files(path):
    files = list()
    for (dirpath, dirnames, filenames) in os.walk(path):
        files += [
            {
                'path': f'{dirpath}/{file}',
                'name': file
            }
            for file in filenames
        ]
    print('Amount of files:', len(files))
    return files


def move_file(dest_path, file):
    file_path = Path(dest_path + '/' + file['name'])
    # if file with same name not exist yet
    if not file_path.is_file():
        shutil.move(file['path'], dest_path)
    else:
        # if the file is exactly same
        if filecmp.cmp(file['path'], dest_path + '/' + file['name']):
            duplicate_file_path = Path(os.getenv('DUPLICATES_DIR_PATH') + '/' + file['name'])
            if duplicate_file_path.is_file():
                os.remove(file['path'])
            else:
                shutil.move(file['path'], Path(os.getenv('DUPLICATES_DIR_PATH')))
        else:
            global SUFFIX
            new_file_path = file['path'] + '_' + SUFFIX
            os.rename(file['path'], new_file_path)
            file['path'] = new_file_path
            shutil.move(file['path'], Path(dest_path))
            SUFFIX += 1


def main():
    all_files = get_files(os.getenv('PHOTOS_DIR_PATH'))
    photos = []

    for file in all_files:
        try:
            datetime = get_capture_datetime(file['path'])
            date = datetime.split(' ')[0].split(':')

            photos.append({
                'path': file['path'],
                'name': file['name'],
                'day': date[2],
                'month': date[1],
                'year': date[0],
            })

        except:
            move_file(os.getenv('UNKNOWN_STUFF_DIR_PATH'), file)

    for photo in photos:
        make_dir(os.getenv('SORTED_DIR_PATH'), photo['year'], photo['month'])

    for photo in photos:
        sorted_path = os.getenv('SORTED_DIR_PATH') + '/' + photo['year'] + '/' + photo['month']
        move_file(sorted_path, photo)

    print('Done!')


if __name__ == "__main__":
    main()
