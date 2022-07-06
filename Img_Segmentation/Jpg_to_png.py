# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: Jpg_to_png.py
@time: 2022/6/25 11:48
"""

import os
import cv2

def jpg_to_png(input_path,output_path):
    # 获取所有图片保存为列表
    files = os.listdir(input_path)
    for i in range(len(files)):
        name = files[i].split('.')
        file = os.path.join(input_path,files[i])
        # 读取图片
        img = cv2.imread(file)
        # 保存图片
        cv2.imwrite(output_path + '\\' + str(name[0]) + '.png', img)

        # # cv2.imwrite(os.path.join(output_path,files[i].replace('jpg','png')),img)
    print('修改完成')
    # 删除原有路径中.jpg格式文件
    for root,dirs,files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(root,file)
            if str(file_path.split('.')[-1]).upper() == 'JPG':
                os.remove(file_path)
    print('删除完成')


if __name__ == "__main__":
    input_path = r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd2'
    output_path = r'D:\python\RRJ\pycharmproject\Practice\chep2\bdd2'
    jpg_to_png(input_path,output_path)