import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from tifffile import imsave

from PIL import Image


def sep_ch(mul_img):
    num_ch = mul_img.shape[2]
    mul_store = [mul_img[:, :, i] for i in range(num_ch)]

    return mul_store


def save_tiff(img, save_location):
    imsave(save_location, img)


def creat_image_list():
    data_location = 'datasets/lgg-mri-segmentation/kaggle_3m'
    folder_list = os.listdir(data_location)

    for folder in folder_list:
        try:
            the_folder = '/'.join([data_location, folder])
            imageNames = os.listdir(the_folder)
            with open('onlyImagesList.txt', 'a') as f:
                for name in imageNames:
                    if 'mask' not in name:
                        fullpath = '/'.join([the_folder, name])
                        f.write(fullpath+'\n')
        except NotADirectoryError:
            continue


if __name__ == '__main__':
    with open('onlyImagesList.txt', 'r') as file:
        for image_name in file:
            image_name = image_name.replace('\n', '')
            if '.tif' not in image_name:
                continue

            original_img = cv2.imread(image_name)
            mul_imgs = sep_ch(original_img)
            name_splited = image_name.split('/')
            img_name = name_splited[-1]
            dir_name = '_'.join(img_name.split('_')[:-1])
            for i, mul_img in enumerate(mul_imgs):
                save_location = '/'.join(
                    ['datasets/mul_channel', dir_name, str(i)+'-'+img_name])
                try:
                    save_tiff(img=mul_imgs[i], save_location=save_location)
                except FileNotFoundError:
                    os.makedirs('/'.join(['datasets/mul_channel', dir_name]))
                    save_tiff(img=mul_imgs[i], save_location=save_location)
