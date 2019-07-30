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


def HC_mapping(hcq, img, type, selected_points, limit):
    sample_idx_store, sample_value_store = [], []

    # HC Index calculation
    hc_idx = tape_to_index(hcq['tape'])
    hc_order = str(hcq["order"])
    sample_x = len(selected_points[hc_order][type])
    sample_y = 2*limit+1

    for pts in selected_points[hc_order][type]:
        sample_idx = get_hc_index(hc_idx, pts, limit)
        sample_values = get_hc_value(img, sample_idx)
        sample_idx_store.append(sample_idx)
        sample_value_store.append(sample_values)

        # For Debuging
        # print("2L+1 =", 2*L+1)
        # print("Sample_idx:", sample_idx)
        # print("Sample_values:", sample_values)

    # In case, To plot sample image
    # sample_img = np.transpose(
    #     np.asarray(sample_value_store).reshape(sample_x, sample_y)
    # )
    return sample_idx_store, sample_value_store


def gabor_1d(x, scale, freq):
    # Gaussian
    def g(x, s):
        return np.exp(-0.5*np.power((x/s), 2))/(s*np.sqrt(2*p))

    # Real part
    def R(x, s, f):
        return g(x, s)*np.cos()

    return g(x, scale)*np.exp()


if __name__ == '__main__':
    # Selected Points
    selected_points = {
        "1": {
            "N": [(2, 2)],
            "L": [(1, 0)],
            "B": [(0, 0)],
        },
        "2": {
            "N": [(1, 3), (2, 3), (3, 1), (3, 2)],
            "L": [(1, 1)],
            "B": [(2, 1), (2, 2)],
        },
        "3": {
            "N": [(2, 4), (3, 4), (5, 3), (5, 4)],
            "L": [(2, 2)],
            "B": [(3, 2), (2, 3), (3, 3)],
        },
        "4": {
            "N": [(10, 10), (10, 9), (7, 5), (9, 5)],
            "L": [(5, 5), (4, 5)],
            "B": [(4, 4), (6, 3), (7, 3), (4, 6), (5, 6)],
        },
        "5": {
            "N": [(12, 19), (17, 21), (22, 17), (16, 22), (6, 20)],
            "L": [(9, 9), (10, 9), (10, 11), (12, 7)],
            "B": [(9, 13), (10, 12), (8, 9), (13, 8)],
        },
        "6": {
            "N": [(22, 41), (42, 45), (43, 23), (38, 13)],
            "L": [(19, 21), (19, 22), (20, 21), (20, 22)],
            "B": [(18, 17), (19, 16), (17, 24), (24, 19)],
        },
        "7": {
            "N": [(39, 86), (87, 82), (77, 65), (78, 32)],
            "L": [(38, 43), (40, 46), (41, 49), (48, 43)],
            "B": [(37, 34), (45, 48), (49, 38), (33, 46)],
        },
        "8": {
            "N": [(93, 182), (183, 179), (181, 109), (147, 60)],
            "L": [(79, 85), (81, 95), (103, 62), (96, 87)],
            "B": [(67, 74), (91, 93), (101, 77), (66, 75)],
        },
    }

    # Path Setting
    ROOT = os.getcwd()
    DATAPATH = './datasets/mul_channel/TCGA_CS_4941_19960909'
    IMGNAME = '1-TCGA_CS_4941_19960909_16.tif'
    IMGPATH = '/'.join([ROOT, DATAPATH, IMGNAME])
    img = cv2.imread(IMGPATH, 1)

    # HC INIT
    order = 8
    hcq = HCQ(hc_order=8)
    HC_info(hcq)

    # HC Multi-resolution
    mulres_store = hc.prepare_image(IMGPATH)
    # mulres_imshow(mulres_store)

    (sample_idx_store, sample_value_store) = HC_mapping(
        hcq,
        mulres_store[order-1],
        'B',
        selected_points,
        9
    )

    print("Sample Idx Store", sample_idx_store)
    print("Sample Value Store", sample_value_store)

    fig = plt.figure(figsize=(9, 18))
    for i, graph in enumerate(sample_value_store):
        ax = fig.add_subplot(3, 3, i+1)
        ax.set_title("i = " + str(i))
        ax.plot(graph)
    plt.show()
