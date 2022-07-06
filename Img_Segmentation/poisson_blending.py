# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: poisson_blending.py
@time: 2022/6/26 11:55
"""
import cv2
import numpy as np
from PIL import Image


def img_Poisson_Blending(src,bg_path):
    src = cv2.resize(src, dsize=(240, 480))
    # dst = cv2.imread(r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd\JMU.png')
    dst = cv2.imread(bg_path)
    dst = cv2.resize(dst, dsize=(480, 640))

    # 创建一个白色的mask
    mask = 255 * np.ones(src.shape, src.dtype)

    rect = cv2.selectROI("background image", dst, fromCenter=False, showCrosshair=False)
    print(type(rect))
    width = int((rect[3] - rect[1])/2) + rect[1]
    height = int((rect[2] - rect[0])/2) + rect[0]
    # width, height, channels = dst.shape
    center = (height, width)

    # normal_clone_img = cv2.seamlessClone(src, dst, dilate_mask, center, cv2.NORMAL_CLONE)
    # return normal_clone_img
    mixed_clone_img = cv2.seamlessClone(src, dst, mask, center, cv2.MIXED_CLONE)
    path = "D:\\python\\RRJ\\pycharmproject\\Image_Segmentation\\PyQtImgZCQ\\ZC.png"
    cv2.imwrite(path,mixed_clone_img)
    return path

if __name__ == "__main__":
    src = cv2.imread("../paddle_output/paddle_output.png")
    src = cv2.resize(src,dsize=(240,480))
    result = img_Poisson_Blending(src)
    cv2.imshow('result',result)
    cv2.waitKey(0)
