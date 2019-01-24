import os
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files
from PIL import Image
import numpy as np

filename = get_testdata_files("CT_small.dcm")[0]
ds = pydicom.dcmread(filename)
print("Patient name:", ds.PatientName)
print('Modality:', ds.Modality)

image = ds.pixel_array
limit = lambda x, h: x if x < h else 0
for i, row in enumerate(image):
    for j, pix in enumerate(row):
        image[i, j] = limit(pix, 2500)

plt.imshow(image, cmap=plt.cm.gray)
plt.show()