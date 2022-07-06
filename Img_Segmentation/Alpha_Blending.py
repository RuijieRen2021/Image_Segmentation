# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: Alpha_Blending.py
@time: 2022/6/24 17:28
"""

from Img_Segmentation import grabCut3
import cv2

def alpha_blending(fore_img_path,bg_img_path):
    """Alpha_Blending"""
    # foreGroundImage = cv2.imread('../paddle_output/paddle_output.png', -1)
    foreGroundImage = cv2.imread(fore_img_path, -1)
    foreGroundImage = grabCut3.update_img_resize(foreGroundImage)
    # 先将通道分离
    b, g, r, a = cv2.split(foreGroundImage)
    # 得到PNG图像前景部分，在这个图片中就是除去Alpha通道的部分
    foreground = cv2.merge((b, g, r))
    # 得到PNG图像的alpha通道，即alpha掩模
    alpha = cv2.merge((a, a, a))

    # 腐蚀膨胀过滤掉图中的白点
    erode_alpha = cv2.erode(alpha, None, iterations=1)  # 图像被腐蚀后，去除了噪声，但是会压缩图像。
    alpha = cv2.dilate(erode_alpha, None, iterations=1)  # 对腐蚀过的图像，进行膨胀处理，可以去除噪声，并且保持原有形状

    # background = cv2.imread(r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd\green.png')
    background = cv2.imread(bg_img_path)
    background = grabCut3.update_img_resize(background)

    # 因为下面要进行乘法运算故将数据类型设为float，防止溢出
    foreground = foreground.astype(float)
    background = background.astype(float)

    cv2.imwrite("alpha/alpha.png", alpha)

    # 将alpha的值归一化在0-1之间，作为加权系数
    alpha = alpha.astype(float) / 255

    # cv2.imshow("alpha", alpha)
    # cv2.waitKey(0)

    # 将前景和背景进行加权，每个像素的加权系数即为alpha掩模对应位置像素的值，前景部分为1，背景部分为0
    foreground = cv2.multiply(alpha, foreground)
    background = cv2.multiply(1.0 - alpha, background)

    outImage = cv2.add(foreground, background)
    save_path = fore_img_path
    cv2.imwrite(save_path, outImage)

    # cv2.imshow("outImg", outImage / 255)
    # cv2.waitKey(0)
    return save_path

# Alpha 融合
def alpha_blending2(fore_img_path,bg_img_path):
    """ grabcut分割结果利用Alpha_Blending融合图像 """
    # 读入图片
    foreground = cv2.imread(fore_img_path)
    foreground = grabCut3.update_img_resize(foreground)
    background = cv2.imread(bg_img_path)
    background = grabCut3.update_img_resize(background)
    alpha = cv2.imread("grabcut_mask/mask.png")

    # cv2.getStructuringElement( ) 返回指定形状和尺寸的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # 腐蚀膨胀过滤掉图中的白点
    erode_alpha = cv2.erode(alpha, kernel, iterations=2)  # 图像被腐蚀后，去除了噪声，但是会压缩图像。
    alpha = cv2.dilate(erode_alpha, kernel, iterations=2)  # 对腐蚀过的图像，进行膨胀处理，可以去除噪声，并且保持原有形状
    # cv2.imshow('dilate', alpha)
    # cv2.waitKey(0)

    # 将 uint8 转换为浮点数
    foreground = foreground.astype(float)
    background = background.astype(float)

    # 标准化 alpha 蒙版将值保持在 0 和 1 之间
    alpha = alpha.astype(float) / 255

    # 将前景与 alpha 遮罩相乘
    foreground = cv2.multiply(alpha, foreground)

    # 将背景与 （1.0-alpha) 遮罩相乘
    background = cv2.multiply(1.0 - alpha, background)

    # 添加蒙板的前景和背景。
    outImage = cv2.add(foreground, background)

    # # 显示
    # cv2.imshow("outImg", outImage / 255)
    # cv2.waitKey(0)

    save_path = fore_img_path
    cv2.imwrite(save_path, outImage)
    return save_path

# 转换HSV
# hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
# lower_blue = np.array([90,70,70])  # HSV颜色范围参数
# # 分离HSV空间，v[0]为H色调,v[1]为饱和度,v[2]为灰度
# upper_blue = np.array([110,255,255])
# mask = cv2.inRange(hsv_img,lower_blue,upper_blue)
# cv2.imshow("mask",mask)
# cv2.waitKey(0)


if __name__ == "__main__":
    alpha_blending()
