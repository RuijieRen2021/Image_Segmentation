# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: grabCut3.py
@time: 2022/6/23 15:41
"""
import os
import cv2
import numpy as np

def img_usm(img):
    # 对图像进行USM锐化增强:通过增加图像边缘的对比度来锐化并给图像添加细节
    """
    USM锐化增强方法(Unsharpen Mask):
    1.先对原图高斯模糊，用原图减去系数x高斯模糊的图像
    2.再把值Scale到0~255的RGB像素范围
    优点：可以去除一些细小细节的干扰和噪声，比卷积更真实
    （原图像-w*高斯模糊）/（1-w）；w表示权重（0.1~0.9），默认0.6
    """
    # sigma = 5、15、25
    # 模糊图像(img:原图像,高斯核(等于0则根据sigmaX和sigmaY计算得出),标准差)
    blur_img = cv2.GaussianBlur(img, (0, 0), 5)
    # cv.addWeighted(图1,权重1, 图2, 权重2, gamma修正系数, dst可选参数, dtype可选参数)
    usmimg = cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)
    cv2.convertScaleAbs(usmimg,usmimg)
    return usmimg

def img_grab_Cut(original_img,usmimg,rect):
    """进行grabCut图像分割"""
    # 掩码图像，如果使用掩码进行初始化，那么mask保存初始化掩码信息；
    # 在执行分割的时候，也可以将用户交互所设定的前景与背景保存到mask中，然后再传入grabCut函数；在处理结束之后，mask中会保存结果
    mask = np.zeros(usmimg.shape[:2], np.uint8)  # 初始化蒙版图像
    bgdModel = np.zeros((1, 65), np.float64)  # 背景模型
    fgdModel = np.zeros((1, 65), np.float64)  # 前景模型
    cv2.grabCut(usmimg, mask, rect, bgdModel, fgdModel, 20, cv2.GC_INIT_WITH_RECT)  # 函数返回值为mask,bgdModel,fgdModel
    # mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # 代码中将0和2合并为背景 1和3合并为前景
    # grabcut_img = usmimg * mask2[:, :, np.newaxis]  # 使用蒙板来获取前景区域

    # 提取前景ROI区域二值图像
    foreground = np.zeros(original_img.shape[:3],np.uint8)
    foreground_roi = np.zeros(original_img.shape[:3], np.uint8)
    height = original_img.shape[0]
    width = original_img.shape[1]
    for row in range(height):
        for col in range(width):
            if mask[row,col] == 1 or mask[row,col] == 3:
                foreground_roi[row,col] = [255,255,255]

    cv2.imwrite('grabcut_mask/mask.png', foreground_roi)

    # 将得到的前景ROI区域二值图像进行开运算消除细微干扰后，和锐化图像进行与（ and ）操作，得到锐化后的前景区域
    # cv2.getStructuringElement:返回指定形状和尺寸的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))

    # cv2.morphologyEx:形态学滤波,cv2.MORPH_OPEN:开运算(open)：先腐蚀后膨胀的过程。开运算可以用来消除小黑点
    cv2.morphologyEx(foreground_roi, cv2.MORPH_OPEN, kernel)
    cv2.bitwise_and(foreground_roi, usmimg, foreground)
    return foreground


def main(imgPath):

    # 读取图像
    img = cv2.imread(imgPath)
    img2 = update_img_resize(img)

    # usm锐化
    usmimg = img_usm(img2)
    cv2.imshow("mask image", usmimg)

    rect = cv2.selectROI("mask image", usmimg, fromCenter=False, showCrosshair=False)
    print(rect)
    print(rect[0],rect[1],rect[2],rect[3])
    # 进行grabCut图像分割
    grabcut_img= img_grab_Cut(img2,usmimg, rect)
    # print(grabcut_img.shape,grabcut_img.dtype)
    print("分割完成")
    cv2.imwrite('grabcut_output/test.png', grabcut_img)  # 写入图片

    current_working_dir = os.getcwd()
    grab_fore_img_path = os.path.join(current_working_dir, "grabcut_output\\test.png")
    return grab_fore_img_path

    # Alpha融合
    # Alpha_Blending()
    # cv2.imshow('GMM', grabcut_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


def update_img_resize(img):
    """修改图像尺寸"""
    # result_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result_img = cv2.resize(img,dsize=(480,640))
    return result_img



if __name__ == '__main__':
    main()

