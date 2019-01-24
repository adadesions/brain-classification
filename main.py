import os
import matplotlib.pyplot as plt
import pydicom
import numpy as np

from adabrain import *

ds = pydicom.dcmread(dcm_list[0])
print("Patient name:", ds.PatientName)
print('Modality:', ds.Modality)

image = ds.pixel_array
limit = lambda x, h: x if x < h else 0

plt.imshow(image, cmap=plt.cm.gray)
plt.show()