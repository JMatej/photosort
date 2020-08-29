import os
import shutil
import filecmp
import calendar

from pathlib import Path
from PIL import Image

PHOTOS_DIR_PATH = 'sample_photos'
SORTED_DIR_PATH = 'sorted_photos'
OTHER_STUFF_DIR_PATH = 'other_stuff'
DUPLICATES_DIR_PATH = 'duplicates'


def get_date_taken(path):
    ar = Image.open(path)._getexif()
    return ar[36868]


def move_file(src, dest):
    shutil.move(src, dest)


def convert_month(month):
    month_name = "Januar"
    if month == '02':
        month_name = "Februar"
    elif month == '03':
        month_name = "Marec"
    elif month == '04':
        month_name = "April"
    elif month == '05':
        month_name = "Maj"
    elif month == '06':
        month_name = "Jun"
    elif month == '07':
        month_name = "Jul"
    elif month == '08':
        month_name = "August"
    elif month == '09':
        month_name = "September"
    elif month == '10':
        month_name = "Oktober"
    elif month == '11':
        month_name = "November"
    elif month == '12':
        month_name = "December"
    return month_name


def making_dirs(curr_path, year, month):
    dir_path_year = curr_path + '/' + year
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
                'path': os.path.join(dirpath, file),
                'name': file
            }
            for file in filenames
        ]
    print("Number of all files:", len(files))
    return files


def main():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    photos = get_files(PHOTOS_DIR_PATH)
    wrong_files = 0
    moved = 0
    correct_files = 0
    same_name = 0
    duplicates = 0
    duplikate_of_duplikate = 0
    suffix = 1

    for i, photo in enumerate(photos):
        if i % 1000 == 0:
            print(i)
        try:
            correct_files += 1
            photo['date'] = get_date_taken(photo['path'])
        except:
            wrong_files += 1
            file_2 = Path(OTHER_STUFF_DIR_PATH + '/' + photo['name'])
            if file_2.is_file():
                if filecmp.cmp(photo['path'], OTHER_STUFF_DIR_PATH + '/' + photo['name']):
                    file = Path(DUPLICATES_DIR_PATH + '/' + photo['name'])
                    if file.is_file():
                        os.remove(photo['path'])
                        duplikate_of_duplikate += 1
                    else:
                        move_file(photo['path'], DUPLICATES_DIR_PATH)
                        duplicates += 1
                else:
                    os.rename(photo['path'], photo['path'] + '_' + str(suffix))
                    photo['path'] = photo['path'] + '_' + str(suffix)
                    suffix += 1
                    move_file(photo['path'], DUPLICATES_DIR_PATH)
                    same_name += 1
            else:
                moved += 1
                move_file(photo['path'], OTHER_STUFF_DIR_PATH)

    for i, photo in enumerate(photos):
        if i % 1000 == 0:
            print(i)
        if 'date' in photo:
            day = photo['date'].split(" ")
            parsed_date = day[0].split(":")
            photo['year'] = parsed_date[0].replace(" ", "")
            photo['month'] = convert_month(parsed_date[1].replace(" ", ""))
            photo['day'] = parsed_date[2].replace(" ", "")
            photo['parsed_date'] = parsed_date[0] + parsed_date[1] + parsed_date[2]
            # print(photo['date'])

    print("Making dirs")
    # for photo in photos:
    #     if 'date' in photo:
    #         try:
    #             making_dirs(SORTED_DIR_PATH, photo['year'], photo['month'])
    #         except:
    #             pass

    print("Moving files into new dirs")
    identical_images = 0
    # for i, photo in enumerate(photos):
    #     if i % 1000 == 0:
    #         print(i)
    #     if 'date' in photo:
    #         try:
    #             sorted_path = SORTED_DIR_PATH + '/' + photo['year'] + '/' + photo['month']
    #             file = Path(sorted_path + '/' + photo['name'])
    #             if file.is_file():
    #                 file_2 = Path(OTHER_STUFF_DIR_PATH + '/' + photo['name'])
    #                 if file_2.is_file():
    #                     if filecmp.cmp(OTHER_STUFF_DIR_PATH + '/' + photo['name'], photo['path']):
    #                         file3 = Path(DUPLICATES_DIR_PATH + '/' + photo['name'])
    #                         if file3.is_file():
    #                             os.remove(photo['path'])
    #                             duplikate_of_duplikate += 1
    #                         else:
    #                             move_file(photo['path'], DUPLICATES_DIR_PATH)
    #                             identical_images += 1
    #                     else:
    #                         same_name += 1
    #                         os.rename(photo['path'], photo['path']+ '_' + str(suffix))
    #                         photo['path'] = photo['path'] + '_' + str(suffix)
    #                         suffix += 1
    #                         move_file(photo['path'], DUPLICATES_DIR_PATH)
    #                 else:
    #                     moved += 1
    #                     move_file(photo['path'], OTHER_STUFF_DIR_PATH)
    #
    #             else:
    #                 moved += 1
    #                 move_file(photo['path'], sorted_path)
    #         except:
    #             pass
    #         #     print("Problem with moving file", photo['path'])

    print("Moved:", moved)
    print("IdenticalImages:", identical_images)
    print("Duplicates:", duplicates)
    print("Duplicate Of Duplikates:", duplikate_of_duplikate)
    print("Same Name:", same_name)


if __name__ == "__main__":
    main()
