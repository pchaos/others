import sys

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMessageBox


class MyWindow:
    def __init__(self):
        # 动态加载UI文件
        ui_file = QFile("pyside_demo1.ui")
        if not ui_file.open(QFile.ReadOnly):
            print(f"无法打开UI文件: {ui_file.errorString()}")
            sys.exit(-1)

        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()

        if not self.ui:
            print("加载UI文件失败")
            sys.exit(-1)

        # 连接按钮点击信号到槽函数
        self.ui.pushButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # 显示成功消息
        QMessageBox.information(self.ui, "提示", "成功！")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.ui.show()

    sys.exit(app.exec())
