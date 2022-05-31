import sys,os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import flower_detect as fd
from detect import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi()
        self.setWindowTitle("花卉分类识别")
        self.setWindowIcon(QIcon('./predator.ico'))

        self.imgNamepath = None
        self.saved = False

    def setupUi(self):
        self.setObjectName("FlowerDetect")
        self.resize(750, 700)


        self.pushbutton1 = QtWidgets.QPushButton(self)
        self.pushbutton1.setObjectName("ChoosePic")
        self.pushbutton1.setText("选择图片")
        self.pushbutton1.setGeometry(100, 50, 150, 100)
        self.pushbutton1.clicked.connect(self.openimg)

        self.pushbutton2 = QtWidgets.QPushButton(self)
        self.pushbutton2.setObjectName("Detect")
        self.pushbutton2.setText("识别")
        self.pushbutton2.setGeometry(500, 50, 150, 100)
        self.pushbutton2.clicked.connect(self.detected)

        self.pushbutton3 = QtWidgets.QPushButton(self)
        self.pushbutton3.setObjectName("Save Image With Label")
        self.pushbutton3.setText("保存图片")
        self.pushbutton3.setGeometry(500, 550, 150, 100)
        self.pushbutton3.clicked.connect(self.save_detect)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setObjectName("Display Pic")
        self.label1.setGeometry(25, 200, 300, 300)
        self.label1.setFrameShape(QtWidgets.QFrame.Box)
        self.label1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label1.setFrameShape(QFrame.Box)
        self.label1.setStyleSheet('border-width: 2px; border-style: solid; border-color: rgb(0, 0, 255) ')

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setObjectName("Display Pic With Label")
        self.label2.setGeometry(425, 200, 300, 300)
        self.label2.setFrameShape(QtWidgets.QFrame.Box)
        self.label2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label2.setFrameShape(QFrame.Box)
        self.label2.setStyleSheet('border-width: 2px; border-style: solid; border-color: rgb(0, 0, 255) ')

        self.label3 = QtWidgets.QLabel("", self)
        self.label3.setObjectName("Detect Result")
        self.label3.setGeometry(25, 588, 300, 25)
        self.label3.setFrameShape(QtWidgets.QFrame.Box)
        self.label3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label3.setFrameShape(QFrame.Box)
        self.label3.setStyleSheet('border-width: 2px; border-style: solid; border-color: rgb(0, 0, 255) ')


    # 打开图片并显示
    def openimg(self):
        # 打开文件的对话框默认在用户的桌面
        global username, default_path
        username = os.path.expanduser('~')
        default_path = os.path.join(username, 'Desktop')

        self.imgNamepath, self.imgType = QFileDialog.getOpenFileName(self.pushbutton1, "选择图片", default_path, "*.jpg")

        img = QtGui.QPixmap(self.imgNamepath).scaled(self.label1.width(), self.label1.height())
        self.label1.setPixmap(img)

    # 识别图片并标记，返回标记后的图片和识别结果
    def detected(self):
        if self.imgNamepath is None:
            QMessageBox.warning(self, "警告", "没有图片！", QMessageBox.Yes | QMessageBox.Yes)
            return

        drawPicPath, self.PicLabel, self.saved = detect(self.imgNamepath, default_path)
        global imag
        imag = QtGui.QPixmap(drawPicPath).scaled(self.label2.width(), self.label2.height())
        self.label2.setPixmap(imag)
        self.label3.setText("识别结果是：" + self.PicLabel)

    def save_detect(self):
        if self.saved is not True:
            QMessageBox.warning(self, "警告", "没有保存", QMessageBox.Yes | QMessageBox.Yes)
            return
        QMessageBox.information(self, "提示", "带识别结果的图片已保存至桌面", QMessageBox.Yes|QMessageBox.Yes)
        self.saved = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
