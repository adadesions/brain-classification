import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    hc_ul = (
        (1, 1), (1, 0),
        (0, 0), (0, 1)
    )

    get_x = lambda data: data[0]
    get_y = lambda data: data[1]
    split_xy = lambda data: [
        list(map(get_x, data)),
        list(map(get_y, data))
    ]
    xor_1 = lambda data: data^1
    flip = lambda data: list(map(xor_1, data))
    c_shift = lambda data, pos: data[pos:]+data[:pos]
    to_coor = lambda index: list(zip(index[0], index[1]))
    # im_hc2 = [
    #     [1, 1, 1, 1],
    #     [0, 1, 1, 1],
    #     [0, 0, 1, 1],
    #     [0, 0, 0, 1],
    # ]

    im_hc2 = [
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
    ]

    original_val = []
    for d in im_hc2:
        original_val.extend(d)

    print(original_val)

    pt0 = split_xy(hc_ul)
    pts = [
        [flip(pt0[0]), flip(pt0[1])]
    ]

    for order in [1, 3, 0]:
        temp = [
            c_shift(pt0[0][::-1], order),
            c_shift(pt0[1][::-1], order)
        ]
        pts.append(temp)

    fig1, ax1 = plt.subplots()
    ax1.set(title='Hilbert Curve', ylabel='Rows', xlabel='Cols')
    im = ax1.imshow(im_hc2, cmap='gist_heat')
    colors =['r', 'g', 'b', 'purple']
    len_pts = len(pts)
    hc_index = []
    prv_m, prv_n = 0, 0

    for i, pt in zip([0, 1, 3, 2], pts):
        temp = [[], []]
        if (i+1)%2 == 0:
            temp[0] = list(np.add(pt[0], i+1))
            temp[1] = pt[1]

        else:
            temp[0] = pt[0]
            temp[1] = list(np.add(pt[1], i))

        if i == len_pts-1:
            temp = np.add(pt, 2).tolist()
            temp = [
                flip(temp[0]),
                flip(temp[1]),
            ]

        hc_index.append(to_coor(temp))

    hc_index[3] = hc_index[3][::-1]
    hc_x, hc_y, hc_v = [], [], []

    for hc in hc_index:
        for i, (x, y) in enumerate(hc):
            ax1.plot(x, y, c=colors[i], linewidth=8)
            ax1.scatter(x, y, c=colors[i], linewidth=8)
            plt.text(x, y, '({}, {})'.format(x, y), color=colors[i])
            ax1.annotate(
                '',
                xytext=(prv_m, prv_n),
                xy=(x, y),
                arrowprops=dict(arrowstyle="->", color='yellow', linewidth=3),
            )
            prv_m, prv_n = x, y
            hc_x.append(x)
            hc_y.append(y)
            hc_v.append(im_hc2[y][x])

            print('({}, {}) = {}'.format(y, x, im_hc2[y][x]))

    fig_hc, ax_hc = plt.subplots(2, 1)
    ax_hc[0].set(title='Hilbert Encoded', ylabel='pixel', xlabel='index')
    ax_hc[0].plot(hc_v, color='r')

    ax_hc[1].set(title='Original', ylabel='pixel', xlabel='index')
    ax_hc[1].plot(original_val, color='r')

    plt.show()
