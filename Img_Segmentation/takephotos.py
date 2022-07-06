# -*- coding: utf-8 -*-
"""
@author: RRJ
@software: PyCharm
@file: takephotos.py
@time: 2022/6/25 20:04
"""
import cv2
import os


def take_photos():
    """
    调用摄像头拍照并保存图片到本地
    :param image_name: 图片名字
    :param image_path: 图片保存路径
    :return: 路径
    """
    image_name = "demo1.png"
    image_path = r'D:\python\RRJ\pycharmproject\Image_Segmentation\takephotos'
    img_save_path = os.path.join(image_path, "demo1.png")

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow("Capture_Paizhao", frame)  # 显示窗口
        if cv2.waitKey(100) & 0xFF == ord('q'):  # 如果按下q 就截图保存并退出
            cv2.imwrite(img_save_path, frame)
            print("保存" + image_name + "成功!")
            break
    cap.release()
    cv2.destroyAllWindows()

    return img_save_path


if __name__ == '__main__':
    img_name = "demo1.png"
    img_path = r"/takephotos/"
    print(take_photos())
