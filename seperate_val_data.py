
# validierungs daten werden bereit gestellt

# asu den test daten wird ein teil extrahiert zum validieren beim training

import random
from random import randint
import shutil
import os
import argparse

def main(folder):
    file_ending_image=".jpeg"

    random.seed(2587915)

    base_path = folder+"\\"  # ordner mit daten
  #  base_path = central.main_path

    place_val = "test"  #source of data

    # folder path
    dir_path = base_path+"labels\\"+place_val+"\\"

    # ziel ordner
    val_path_images = base_path + "images\\val\\"
    val_path_labels = base_path + "labels\\val\\"

    count_transfer=0

    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)

    list_empty=[]
    list_car = []
    list_bike = []
    list_lkw = []
    list_bicycle = []

    # gleichmäßig nach klassen aufspalten
    for string_element in res:
        if "T0" in string_element:
            list_car.append(string_element)
        elif "T1" in string_element:
            list_bike.append(string_element)
        elif "T2" in string_element:
            list_lkw.append(string_element)
        elif "T9" in string_element:
            list_empty.append(string_element)
        elif "T8" in string_element:
            list_bicycle.append(string_element)

    all_file_paths_combined = [
        list_empty ,
        list_car ,
        list_bike ,
        list_lkw ,
        list_bicycle ,
    ]

    for file_path_data in all_file_paths_combined:
        new_file_list = []

        # 0.08 der daten werden kopiert
        for index_validate_counter in range(1, int(len(file_path_data) * 0.08)):
            rand_val = randint(0, len(file_path_data) - 1)
            while file_path_data[rand_val] in new_file_list:
                rand_val = randint(0, len(file_path_data) - 1)
            new_file_list.append(file_path_data[rand_val])
        # copy files over
        for file_data_value in new_file_list:

            file_data_value,_ = file_data_value.split(".")

            shutil.move(base_path+"images\\"+place_val+"\\"+file_data_value + file_ending_image, val_path_images + file_data_value + file_ending_image , copy_function = shutil.copyfile)
            shutil.move(base_path+"labels\\"+place_val+"\\"+file_data_value+ ".txt", val_path_labels +file_data_value+ ".txt" , copy_function = shutil.copyfile)
            #print(file_data_value)
            count_transfer+=1

    print("copied: "+str(count_transfer))
    print("end")
    exit()

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('--folder', type=str, default="..\\vehicle_data",
                            help='Ordner mit image und label Unterordnern')

        opt = parser.parse_args()
        main(**vars(opt))
    finally:
        pass