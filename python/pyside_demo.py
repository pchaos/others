# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QApplication, QWidget, QLabel

# 创建应用实例
app = QApplication()

# 创建一个窗口
window = QWidget()
window.setWindowTitle("Simple Window")
window.setFixedSize(400, 300)

# 创建一个标签并显示文字
label = QLabel("Hello PySide6!", window)
label.move(150, 125)

# 显示窗口
window.show()

# 进入应用主循环
app.exec()
