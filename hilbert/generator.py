import matplotlib.pyplot as plt
import numpy as np

order1 = 'dru'
inverse_table = {
    'd': 'u', 'u': 'd',
    'l': 'r', 'r': 'l',
    'o': 'o'
}
pairing_table = {
    'd': 'r', 'r': 'd',
    'u': 'l', 'l': 'u',
    'o': 'o'
}

connector = lambda header: ''.join(map(lambda ch: pairing_table[ch], header))
# assert connector('dru') == 'rdl'
conn = connector(order1)
print(conn)

# from itertools import *
# from time import sleep
# from functools import reduce
# for x in chain('ada', 'sions'):
#     print(x, end='')
# print()
# prod = [*product('durl', repeat=4)]
# print(reduce(lambda x, y: ''.join([x, y]), ['as', 'ada']))