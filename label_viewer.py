# skript zum betrachten von lables und bounding boxes der bilder


import numpy as np
import sys
import os
import pygame
import argparse
import time

def get_font():
    fonts = [x for x in pygame.font.get_fonts()]
    default_font = 'ubuntumono'
    font = default_font if default_font in fonts else fonts[0]
    font = pygame.font.match_font(font)
    return pygame.font.Font(font, 14)


def draw_image(surface, image, blend=False):
    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]
    array = array[:, :, ::-1]
    image_surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    if blend:
        image_surface.set_alpha(100)
    surface.blit(image_surface, (0, 0))

def draw_labels(list_files,counter_data):
    print(list_files[counter_data][1])
    image = load_image(list_files[counter_data][0])
    labels = load_labels(list_files[counter_data][1])


    bb_surface = pygame.Surface((picture_size, picture_size))
    bb_surface.set_colorkey((0, 0, 0))

    bb_surface.blit(image, (0, 0))
    # draw lines
    for ele in labels:
        pygame.draw.line(bb_surface, BB_COLOR, (int(ele[0]), int(ele[2])), (int(ele[1]), int(ele[2])))
        pygame.draw.line(bb_surface, BB_COLOR, (int(ele[0]), int(ele[3])), (int(ele[1]), int(ele[3])))
        pygame.draw.line(bb_surface, BB_COLOR, (int(ele[0]), int(ele[2])), (int(ele[0]), int(ele[3])))
        pygame.draw.line(bb_surface, BB_COLOR, (int(ele[1]), int(ele[2])), (int(ele[1]), int(ele[3])))
    return bb_surface


picture_size = 640

BB_COLOR = (248, 64, 24)

change = False
fine_control=False



def load_image(path):
    file_image = pygame.image.load(path)
    return file_image

def load_labels(path):
    labels=[]
    with open(path) as f:
        lines = f.readlines()
        for el in lines:
            ele2 = el.split()
            list_vals = []

            list_vals.append(ele2[0])
            list_vals.append(ele2[1])
            list_vals.append(ele2[2])
            list_vals.append(ele2[3])
            list_vals.append(ele2[4])
            labels.append(list_vals)

    new_labels = []
    for ele in labels:
        x_mitte = float(ele[1]) * picture_size
        y_mitte = float(ele[2]) * picture_size
        x_länge = float(ele[3]) * picture_size
        y_länge = float(ele[4]) * picture_size
        x_start = x_mitte - (x_länge / 2)
        x_ende = x_mitte + (x_länge / 2)
        y_start = y_mitte - (y_länge / 2)
        y_ende = y_mitte + (y_länge / 2)
        mini_list = []
        mini_list.append(int(x_start))
        mini_list.append(int(x_ende))
        mini_list.append(int(y_start))
        mini_list.append(int(y_ende))
        new_labels.append(mini_list)
    return new_labels



def main(folder, task):
    tt = "train"
    data_folder = "..\\vehicle_data"
    if task =="test":
        tt = "test"
    elif task =="train":
        tt = "train"
    elif task =="val":
        tt = "val"

    data_folder = folder
    file_ending_image = ".jpeg"

    base_path = data_folder+"\\"

    # folder path
    dir_path = base_path + "labels\\"+tt+"\\"

    res = []

    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)

    val_path_images = base_path + "images\\"+tt+"\\"
    val_path_labels = base_path + "labels\\"+tt+"\\"

    list_files =[]

    for ele in res:
        file_data_value, _ = ele.split(".")

        the_image = val_path_images+file_data_value+file_ending_image
        the_labels = val_path_labels+file_data_value+".txt"

        #    if "L2" in file_data_value  and "C65" in file_data_value:

        list_files.append([the_image, the_labels])




    pygame.init()

    display = pygame.display.set_mode(
        (picture_size, picture_size),
        pygame.HWSURFACE | pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    font = get_font()

    counter_data=0

    bb_surface = pygame.Surface((picture_size, picture_size))
    bb_surface.set_colorkey((0, 0, 0))

    while True:
        clock.tick()

        time.sleep(0.1)
        keys = pygame.key.get_pressed()
        display.blit(bb_surface, (0, 0))

        pygame.display.flip()
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    counter_data -= 1
                    if counter_data == -1:
                        counter_data = 0
                    bb_surface = draw_labels(list_files, counter_data)

                elif event.key == pygame.K_2:
                    counter_data+= 1
                    if counter_data == len(list_files):
                        counter_data = len(list_files) - 1
                    bb_surface = draw_labels(list_files, counter_data)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()

        parser.add_argument('--folder', type=str, default="..\\vehicle_data",
                            help='Ordner mit image und label Unterordnern')
        parser.add_argument('--task', type=str, default="train", help='test train val')

        opt = parser.parse_args()
        main(**vars(opt))
    finally:
        print("exit")

