import matplotlib.pyplot as plt
import numpy as np
from time import sleep
from random import random
from matplotlib.animation import FuncAnimation
from generator import hc_generator

# Walking
left = lambda point: (point[0]-1, point[1])
right = lambda point: (point[0]+1, point[1])
up = lambda point: (point[0], point[1]-1)
down = lambda point: (point[0], point[1]+1)

create_grid = lambda rows, cols: list([[0]*cols]*rows)
acess_lv1 = lambda row: list(map(lambda pix: float(random()), row))
randomize = lambda grid: list(map(acess_lv1, grid))
tape_reader = {
    'u': lambda step: up(step), 
    'd': lambda step: down(step), 
    'l': lambda step: left(step), 
    'r': lambda step: right(step),
    'o': lambda step: tuple(step),
}

inv_dict = {
    'u': 'd', 'd': 'u', 'l': 'r', 'r': 'l', 'o': 'o'
}
inv_tape = lambda tape: ''.join(list(map(lambda ch: inv_dict[ch], tape)))
rev_tape = lambda tape: tape[::-1]
get_conn_tape = lambda tape: map(lambda i: i[1] if i[0]%4 == 0 else 'o', enumerate(tape))


hc_maps = []
for order in range(5, 9):
    n = 2**order
    temp_map = randomize(create_grid(n, n))
    hc_maps.append(temp_map)

fig0, ax0 = plt.subplots()
im0 = ax0.imshow(hc_maps[0], cmap='gray')

fig1, ax1 = plt.subplots()
im1 = ax1.imshow(hc_maps[1], cmap='gray')

fig2, ax2 = plt.subplots()
im2 = ax2.imshow(hc_maps[2], cmap='gray')

fig3, ax3 = plt.subplots()
im3 = ax3.imshow(hc_maps[3], cmap='gray')

axes = [ax0, ax1, ax2, ax3]

p_step = [0, 0]
n_step = [0, 0]
path = []

U, D, R, L = 'dru', 'urd', 'rdl', 'ldr'
FU, FD, FR, FL = 'dlu', 'uld', 'rul', 'lur'
tape = 'o'+U+'r'+R+'d'+R+'l'+FD+\
        'd'+R+'d'+U+'r'+U+'u'+FL+\
        'r'+R+'d'+U+'r'+U+'u'+FL+\
        'u'+FD+'l'+FL+'u'+FL+'r'+U

tape_inv = inv_tape(tape)
tape_rev = rev_tape(tape)
tape = tape

tape_len = len(tape)
print('len:', tape_len)
conn_tape = ''

for i in range(tape_len//4):
    start = 4*i
    end = 4*(i+1)
    seq = tape[start:end]
    conn = seq[0]
    shape = seq[1:]

    conn_tape += conn
    print('Seq: {}, Conn: {}, Shape: {}'.format(seq, conn, shape))

order1_tape = list(get_conn_tape(conn_tape))
print('order3', tape)
print('order2:', conn_tape)
print('order1:', order1_tape)

tape = hc_generator(['odru'], 3)
print(tape)

for ax in axes:
    p_step = [0, 0]
    path = []
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    for t in tape:
        t_step = tape_reader[t](p_step)

        if t_step[0] < xlim[0] or t_step[0] > xlim[1]: break
        if t_step[1] < ylim[1] or t_step[1] > ylim[0]: break

        ax.annotate(
            '',
            xytext=(p_step[0], p_step[1]),
            xy=(t_step[0], t_step[1]),
            arrowprops=dict(arrowstyle="->", color='red', linewidth=1),
        )

        n_step = t_step[::]
        p_step = n_step[::]

        path.append(n_step)

    print('Path{}: {}'.format(len(path), path))


plt.show()