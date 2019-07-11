#!/usr/bin/python3
'''
    Thesis Purpose
'''
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

from sfcpy import hilbert as hc


def main():
    imgs, tapes = [], []
    filePath = os.path.abspath(os.path.dirname(__file__))
    dataPath = os.path.join(filePath, "datasets")
    mriPath = os.path.join(dataPath, "lgg-mri-segmentation", "kaggle_3m")
    mriFolder = os.listdir(mriPath)

    mri_sample = os.path.join(mriPath, mriFolder[1])

    imgPath = os.path.join(mri_sample, os.listdir(mri_sample)[6])
    # imgPath = os.path.join(dataPath, 'sample.png')
    sample = Image.open(imgPath)

    fig, ax = plt.subplots()
    ax.imshow(sample, cmap='gray')
    nrows, ncols = 3, 3
    axes_num = nrows*ncols

    path, val = [], []
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    highest_order = axes_num+1

    imgs = hc.prepare_image(imgPath)
    for order in range(highest_order-axes_num, highest_order+1):
        tape = hc.get_hc_tape(order)
        tapes.append(tape)

    for i, tape in enumerate(tapes):
        val_temp = []
        p_step = [0, 0]
        for t in tape:
            t_step = hc.tape_reader[t](p_step)

            if t_step[0] < xlim[0] or t_step[0] > xlim[1]:
                break
            if t_step[1] < ylim[1] or t_step[1] > ylim[0]:
                break

            n_step = t_step[::]
            p_step = n_step[::]

            path.append(n_step)
            try:
                val_temp.append(imgs[i][n_step])
            except IndexError:
                continue
        val.append(val_temp)

    print('tape len:', len(tapes))
    print('imgs len:', len(imgs))
    fig1, ax1 = plt.subplots(nrows=nrows, ncols=ncols)
    count_val = 0

    for i in range(nrows):
        for j in range(ncols):
            order_str = 'Order {}'.format(highest_order-axes_num+count_val)
            ax1[i, j].set(title=order_str)
            ax1[i, j].plot(val[count_val], color='red', linewidth=3)
            count_val += 1
    plt.show()


if __name__ == "__main__":
    main()
