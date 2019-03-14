from sfcpy.hilbert import get_hc_tape
from sfcpy.data import data

tape = get_hc_tape(order=4)
print(tape)
print(data("/test.txt"))