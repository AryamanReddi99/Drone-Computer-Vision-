###
# input：80*60 resolution
# return: new data 0~1 floating
# https://blog.csdn.net/lql0716/article/details/52416086
# https://blog.csdn.net/guduruyu/article/details/71404941
###
# coding=gbk
from PIL import Image
from PIL import ImageFilter
import numpy as np
import matplotlib.pyplot as plt

# filter + matrixing; need adjustment
# input: image
def ImageToMatrix(im):
    width, height = im.size
    im = im.convert("L")  # convert to gray scale
    im = im.filter(ImageFilter.GaussianBlur(radius=4))  # need adjusting
    data = im.getdata()
    data = np.matrix(data, dtype='float')/255.0
    new_data = np.reshape(data, (height, width))
    return new_data


def MatrixToImage(data):
    data = data*255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im


def main():
    filename = '1.jpg'
    im = Image.open(filename)
    data = ImageToMatrix(im)
    print(data)
    new_im = MatrixToImage(data)
    plt.imshow(data, cmap=plt.cm.gray, interpolation='nearest')
    new_im.show()
    new_im.save('lena_1.bmp')


# test
if __name__ == '__main__':
    main()
