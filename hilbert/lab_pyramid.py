from skimage.transform import pyramid_gaussian
from PIL import Image
import matplotlib.pyplot as plt
from time import sleep

im = Image.open('images/brain_cancer.jpg')
n = 2**10
im = im.resize((n, n))
pyramid = tuple(pyramid_gaussian(im))
print('len', len(pyramid))

fig, ax = plt.subplots()
py = pyramid[8]

for ip in pyramid:
    print('Dim:', ip.shape)

ax.imshow(py, cmap='gray')

plt.show()