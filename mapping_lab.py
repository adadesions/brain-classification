import os
import numpy as np
import sfcpy.hilbert as hc
import matplotlib.pyplot as plt
import cv2
from PIL import Image


def search_idx(hc_array, target):
    hc_index = [i for i, element in enumerate(hc_array) if element == target]

    try:
        return hc_index[0]
    except IndexError:
        print("Search not Found!")
        return 0


def get_hc_index(hc_array, target, offset):
    center_idx = search_idx(hc_array, target)
    start = center_idx - offset
    end = center_idx + offset + 1
    is_inbound = start >= 0 and end < len(hc_array)

    return hc_array[start:end] if is_inbound else []


def get_hc_value(img, hc_idx):
    sample_values = []
    for idx in hc_idx:
        try:
            sample_values.append(img[idx])
        except IndexError:
            continue

    return sample_values


def create_grid(dim):
    x = np.linspace(0, 1, dim)
    y = np.linspace(0, 1, dim)
    grid, yv = np.meshgrid(x, y)
    print('GRID SHAPE:', grid.shape)

    return grid


def HCQ(hc_order):
    hc_dim = np.power(2, hc_order)
    return {
        "order": hc_order,
        "dim": hc_dim,
        "size": np.power(hc_dim, 2),
        "tape": hc.get_hc_tape(hc_order),
    }


def HC_info(hcq):
    print('HC Order:', hcq['order'])
    print('Tape_Len:', len(hcq['tape']))
    print('HC_DIM:', hcq['dim'])
    print('HC_SIZE:', hcq['size'])


def tape_to_index(hc_tape):
    cur_pt = (0, 0)
    hc_idx = []

    for i, letter in enumerate(hc_tape):
        cal_pt = hc.tape_reader[letter](cur_pt)
        cur_pt = cal_pt
        (x, y) = cal_pt
        hc_idx.append((y, x))

    return hc_idx


def mulres_imshow(mulres_imgs):
    fig = plt.figure(figsize=(9, 18))
    for i, img in enumerate(mulres_imgs):
        ax = fig.add_subplot(3, 3, i+1)
        ax.set_title(img.shape)
        ax.imshow(img, cmap='gray')
    plt.show()


if __name__ == '__main__':
    # Path Setting
    ROOT = os.getcwd()
    DATAPATH = './datasets/mul_channel/TCGA_CS_4941_19960909'
    IMGNAME = '1-TCGA_CS_4941_19960909_16.tif'
    IMGPATH = '/'.join([ROOT, DATAPATH, IMGNAME])
    img = cv2.imread(IMGPATH, 1)

    # HC INIT
    hcq = HCQ(hc_order=2)
    HC_info(hcq)
    mulres_imgs = hc.prepare_image(IMGPATH)
    mulres_imshow(mulres_imgs)

    grid = create_grid(hcq['dim'])
    hc_idx = tape_to_index(hcq['tape'])
    sample_idx = get_hc_index(hc_idx, (1, 2), 1)
    sample_values = get_hc_value(grid, sample_idx)

    print("HC_ARRAY:", hc_idx)
    print("Sample_idx:", sample_idx)
    print("Sample_values:", sample_values)
