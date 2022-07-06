# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: paddle_Image.py
@time: 2022/6/22 22:45
"""
# 导入库
from PIL import Image
import numpy as np
import cv2
import os
# PaddleHub是基于PaddlePaddle生态下的预训练模型管理和迁移学习工具
# 可以结合预训练模型更便捷地开展迁移学习工作,通过PaddleHub,可以便捷地获取PaddlePaddle生态下的所有预训练模型
import paddlehub as hub
import matplotlib.pyplot as plt
import matplotlib.image as mping


def img_remove(remove_img_path):
    # 删除原有路径中.jpg格式文件
    for root, dirs, files in os.walk(remove_img_path):
        for file in files:
            file_path = os.path.join(root, file)
            if str(file_path.split('.')[-1]).upper() == 'PNG':
                os.remove(file_path)
    print('删除完成')

# 用matplotlib显示中文，避免乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def paddle_cut_Image(imgPath):
    """利用deeplabv3p分割图像"""
    # imgPath = r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd\RRJ.png'
    # test_img_path = [imgPath]
    # img = cv2.imread(test_img_path[0])

    # 1.获取图片路径，传入模型
    test_img_path = imgPath

    # 2.调用飞桨训练模型
    # 调用飞桨的deeplabv3p_xception65_humanseg,该模型用于人像抠图
    moddle = hub.Module(name="deeplabv3p_xception65_humanseg")
    # 图像地址（固定格式，不要修改）
    # input_dict = {"image": test_img_path}
    # 训练模型并预测模型，打印结果（获取到抠图人像）
    result = moddle.segmentation(images=[cv2.imread(test_img_path)], visualization=True,
                                 output_dir='../humanseg_output')

    # 3.保存抠出的前景图像
    paddle_fore_img = mping.imread(result[0]['save_path'])
    mping.imsave("paddle_output/paddle_output.png", paddle_fore_img)
    # for ans in result:
    #     print(ans)
    # 4.保存轮廓图像
    res_image = Image.fromarray(np.uint8(result[0]['data']))
    path = "paddle_mask/paddle_mask.png"
    res_image.save(path)
    # 加载保存的轮廓并显示，接着对其进行二值化处理，然后进行图像的腐蚀膨胀操作，得到输出结果，根据结果调整参数值。
    counter_img_path = path
    img_counter = cv2.imread(counter_img_path)
    # 灰度图像
    img_gray = cv2.cvtColor(img_counter, cv2.COLOR_BGR2GRAY)
    # 阈值处理，图像二值化(ret:阈值，thresh1:阈值化后的图像)
    ret, thresh1 = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
    # getStructuringElement( ) 返回指定形状和尺寸的结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
    # 图像腐蚀，去除了噪声，但是会压缩图像。
    erode = cv2.erode(thresh1, kernel, iterations=2)
    # 对腐蚀的图像膨胀处理，可以去除噪声，并且保持原有形状
    dilate = cv2.dilate(erode, kernel, iterations=2)
    cv2.imwrite(path, dilate)
    # cv2.imshow('dilate',dilate)
    # # cv2.imshow('erode',erode)
    # # cv2.imshow('gray_img',img_gray)
    # # cv2.imshow('binary_img',thresh1)
    # # cv2.imshow('counter_img',img_counter)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 5.清理文件夹残存图像
    remove_img_path = r'/humanseg_output'
    img_remove(remove_img_path)

    current_working_dir = os.getcwd()
    paddle_fore_img_path = os.path.join(current_working_dir, "paddle_output\paddle_output.png")

    return paddle_fore_img_path
