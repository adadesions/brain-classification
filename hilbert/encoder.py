from PIL import Image
from skimage.transform import pyramid_gaussian
import numpy as np


def get_hc_tape(file_path, order=2):
    order_str = 'Order {}'.format(order)
    encoded = ''
    is_found = False

    with open(file_path, 'r') as file:
        for line in file.readlines():
            if is_found:
                encoded = line
                break;

            if order_str in line:
                is_found = True

    return encoded.replace('\n', '')


def prepare_hc(order=2):
    tape = get_hc_tape('./hilbert/hc_lookup.txt', order)

    return tape


def prepare_image(filepath):
    im = Image.open('images/brain_cancer.jpg')
    (w, h) = im.size
    max_dim = max(w, h)
    hc_order = int(np.ceil(np.log2(max_dim)))
    n = 2**hc_order
    im = im.resize((n, n))
    pyramid = tuple(pyramid_gaussian(im))
    
    return pyramid[-2::-1]


# Hilber Curve functional
left = lambda point: (point[0]-1, point[1])
right = lambda point: (point[0]+1, point[1])
up = lambda point: (point[0], point[1]-1)
down = lambda point: (point[0], point[1]+1)
tape_reader = {
    'u': lambda step: up(step), 
    'd': lambda step: down(step), 
    'l': lambda step: left(step), 
    'r': lambda step: right(step),
    'o': lambda step: tuple(step),
}


if __name__ == '__main__':
    FILEPATH = './hilbert/hc_lookup.txt'
    hc_tape = get_hc_tape(FILEPATH, 10)
    print(hc_tape)