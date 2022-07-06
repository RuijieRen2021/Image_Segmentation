# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: createImg.py
@time: 2022/6/25 17:23
"""

import cv2

img = cv2.imread(r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd\blue.png')

height = img.shape[0]
width = img.shape[1]
depth = img.shape[2]
print(height, width, depth)
for i in range(height):
    for j in range(width):
        img[i,j] = [0,0,0]
cv2.imwrite(r"D:\python\RRJ\pycharmproject\Practice\chep2\bdd\black.png",img)
cv2.imshow("green",img)
cv2.waitKey(0)
