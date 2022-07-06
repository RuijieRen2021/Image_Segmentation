# 这是一个示例 Python 脚本。
# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# def print_hi(name):
#     # 在下面的代码行中使用断点来调试脚本。
#     print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from img_cut_window import Ui_MainWindow

if __name__ == '__main__':
    # 界面的入口，定义QApplication对象
    app = QApplication(sys.argv)
    MainWindow = Ui_MainWindow()  # 创建窗体对象
    window = QMainWindow()        # 实例化QMainWindow类
    MainWindow.setupUi(window)    # 主窗体对象调用setupUi方法，对QMainWindow对象进行设置
    window.show()  # 显示主窗体

    sys.exit(app.exec_())  # 程序关闭时退出进程

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
