#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, qApp, QAction
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PIL import ImageGrab
import time


class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        print(QApplication.screens())

        QFontDatabase.addApplicationFont("css/Lobster.ttf")

        self.TextSize1 = 50
        self.TextSize2 = 50
        self.Text1_x = 0
        self.Text2_x = 0
        self.Text1_y = 20
        self.Text2_y = 400
        self.TextFontType = 'Impact'
        self.TextColour = '#000000'
        self.Text1_case = 'none'
        self.Text2_case = 'none'
        self.Text1_text = ''
        self.Text2_text = ''

        self.lbl1 = QLabel(self)    # тексты
        self.lbl2 = QLabel(self)
        self.lbl1.setFont(QFont(self.TextFontType, self.TextSize1))
        self.lbl2.setFont(QFont(self.TextFontType, self.TextSize2))
        self.lbl1.move(self.Text1_x, self.Text1_y)
        self.lbl1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl2.move(self.Text2_x, self.Text2_y)

        self.square = QFrame(self)   # плашка нижнего меню
        self.square.setGeometry(0, 500, 800, 80)
        self.square.setStyleSheet("QWidget { background-color: #ffffff }")

        lbl_w = QLabel('Подвинуть влево/вправо', self)
        lbl_w.move(15,550)
        lbl_h = QLabel('Подвинуть вверх/вниз', self)
        lbl_h.move(20, 565)
        lbl_f = QLabel('Увеличить/уменьшить шрифт', self)
        lbl_f.move(5, 530)

        qle1 = QLineEdit(self)   # поля ввода текста
        qle2 = QLineEdit(self)
        qle1.move(165, 505)
        qle2.move(355, 505)
        qle1.textChanged[str].connect(self.onChanged)
        qle2.textChanged[str].connect(self.onChanged2)

        sld_size1 = QSlider(Qt.Horizontal, self)   # слайдер размера верхнего текста
        sld_size1.setFocusPolicy(Qt.NoFocus)
        sld_size1.setGeometry(50, 40, 130, 15)
        sld_size1.move(165,530)
        sld_size1.setValue(self.TextSize1)
        sld_size1.valueChanged[int].connect(self.ChangeTextSize1)

        sld_size2 = QSlider(Qt.Horizontal, self)   # слайдер размера нижнего текста
        sld_size2.setFocusPolicy(Qt.NoFocus)
        sld_size2.setGeometry(30, 40, 130, 15)
        sld_size2.move(355, 530)
        sld_size2.setValue(self.TextSize2)
        sld_size2.valueChanged[int].connect(self.ChangeTextSize2)

        sld_x1 = QSlider(Qt.Horizontal, self)   # слайдер x-движения верхнего текста
        sld_x1.setFocusPolicy(Qt.NoFocus)
        sld_x1.setGeometry(30, 40, 130, 15)
        sld_x1.move(165, 550)
        sld_x1.setValue(self.Text1_x)
        sld_x1.valueChanged[int].connect(self.ChangeText_x1)

        sld_x2 = QSlider(Qt.Horizontal, self)   # слайдер x-движения нижнего текста
        sld_x2.setFocusPolicy(Qt.NoFocus)
        sld_x2.setGeometry(30, 40, 130, 15)
        sld_x2.move(355, 550)
        sld_x2.setValue(self.Text2_x)
        sld_x2.valueChanged[int].connect(self.ChangeText_x2)

        sld_y1 = QSlider(Qt.Horizontal, self)  # слайдер y-движения верхнего текста
        sld_y1.setFocusPolicy(Qt.NoFocus)
        sld_y1.setGeometry(30, 40, 130, 15)
        sld_y1.move(165, 565)
        sld_y1.setValue(0)
        sld_y1.valueChanged[int].connect(self.ChangeText_y1)

        sld_y2 = QSlider(Qt.Horizontal, self)  # слайдер y-движения нижнего текста
        sld_y2.setFocusPolicy(Qt.NoFocus)
        sld_y2.setGeometry(30, 40, 130, 15)
        sld_y2.move(355, 565)
        sld_y2.setValue(0)
        sld_y2.valueChanged[int].connect(self.ChangeText_y2)

        combo = QComboBox(self)
        combo.addItem(" Шрифт ")
        combo.addItem("Impact")
        combo.addItem("Lobster")
        combo.addItem("Arial")
        combo.move(580, 504)
        combo.activated[str].connect(self.ChangeFont)

        cb = QCheckBox('caps lock', self)   # чекбокс выбор шрифта
        cb.move(600, 530)
        cb.stateChanged.connect(self.CheckBoxUpperCase)

        btn_save = QPushButton("\n\nСохранить\n\n", self)
        btn_save.move(700, 503)
        btn_save.clicked.connect(self.TakeScreenshot)

        btn_upload = QPushButton("     Выбрать картинку     ", self)
        btn_upload.setToolTip('Рекомендуется загружать картинки размером <b>800х500</b>.<br>Иначе она будет <b>автоматически</b> растянута до нужного размера')
        btn_upload.move(10, 503)
        btn_upload.clicked.connect(self.UploadPhoto)

        btn_txtcol = QPushButton("Цвет текста", self)
        btn_txtcol.move(500, 503)
        btn_txtcol.clicked.connect(self.ChangeColour)

        self.setFixedSize(800,580)
        self.center()
        self.setWindowTitle('Photo Editor v1.0')
        self.setWindowIcon(QIcon('css/icon.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        print (qr)
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Выход',
                                     "Вы действительно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def onChanged(self, text1):
        self.Text1_text = text1
        self.lbl1.setText(text1)
        self.lbl1.adjustSize()

    def onChanged2(self, text2):
        self.Text2_text = text2
        self.lbl2.setText(text2)
        self.lbl2.adjustSize()


    def TakeScreenshot(self):
        qr = self.frameGeometry()
        s_x = int(qr.x())
        s_y = int(qr.y())
        print(qr.x())
        print(qr.y())
        im = ImageGrab.grab((s_x+10,s_y+30,s_x+800,s_y+520))
        im.show()
        name = "images/IMG"+time.strftime("%Y%m%d%H%M%S")+".png"
        print(name)
        im.save(name)
        print('Сохранение снимка')



    def UploadPhoto(self):
       print('open file dialog')
       options = QFileDialog.Options()
       options |= QFileDialog.DontUseNativeDialog
       fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "templates/",
                                                 "All Files (*); Images (*.png *.jpeg *.jpg)", options=options)
       if fileName:
           print(fileName)
           oImage = QImage(fileName)
           sImage = oImage.scaled(QSize(800, 500))  # resize Image to widgets size
           palette = QPalette()
           palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
           self.setPalette(palette)

    def ChangeColour(self):
        print(' open colour popup')
        col = QColorDialog.getColor()
        if col:
            print(col.name())
            self.TextColour = col.name()
            self.lbl1.setStyleSheet('color: ' + self.TextColour)
            self.lbl2.setStyleSheet('color: ' + self.TextColour)


    def CheckBoxUpperCase(self, state):

        if state == Qt.Checked:
            self.Text1_case = 'uppercase'
            self.Text2_case = 'uppercase'
            print("Text1: " + self.Text1_case + " Text2: " + self.Text2_case)
            self.lbl1.setStyleSheet("QLabel { text-transform: " + self.Text1_case + "; " + "color: " + self.TextColour + "}")
            self.lbl2.setStyleSheet("QLabel { text-transform: " + self.Text2_case + "; " + "color: " + self.TextColour + "}")
            self.lbl1.adjustSize()
            self.lbl2.adjustSize()
        else:
            self.Text1_case = 'lowercase'
            self.Text2_case = 'lowercase'
            print("Text1: " + self.Text1_case + " Text2: " + self.Text2_case)
            self.lbl1.setStyleSheet("QLabel { text-transform: " + self.Text1_case + "; " + "color: " + self.TextColour + "}")
            self.lbl2.setStyleSheet("QLabel { text-transform: " + self.Text2_case + "; " + "color: " + self.TextColour + "}")
            self.lbl1.adjustSize()
            self.lbl2.adjustSize()

    def ChangeFont(self,text):
        if text == 'Impact':
            print(text)
            self.TextFontType = 'Impact'
            self.lbl1.setFont(QFont(self.TextFontType, self.TextSize1))
            self.lbl2.setFont(QFont(self.TextFontType, self.TextSize2))
            self.lbl1.adjustSize()
            self.lbl2.adjustSize()
        if text == 'Lobster':
            print(text)
            self.TextFontType = 'Lobster'
            self.lbl1.setFont(QFont(self.TextFontType, self.TextSize1))
            self.lbl2.setFont(QFont(self.TextFontType, self.TextSize2))
            self.lbl1.adjustSize()
            self.lbl2.adjustSize()
        if text == 'Arial':
            print(text)
            self.TextFontType = 'Arial'
            self.lbl1.setFont(QFont(self.TextFontType, self.TextSize1))
            self.lbl2.setFont(QFont(self.TextFontType, self.TextSize2))
            self.lbl1.adjustSize()
            self.lbl2.adjustSize()

    def ChangeTextSize1(self, value):
        self.TextSize1 = value
        self.lbl1.setFont(QFont(self.TextFontType, self.TextSize1))
        self.lbl1.adjustSize()

    def ChangeTextSize2(self, value):
        self.TextSize2 = value
        self.lbl2.setFont(QFont(self.TextFontType, self.TextSize2))
        self.lbl2.adjustSize()

    def ChangeText_x1(self, value):
        self.Text1_x = value*6
        self.lbl1.move(self.Text1_x,self.Text1_y)
        self.lbl1.adjustSize()
        self.lbl2.adjustSize()

    def ChangeText_x2(self, value):
        self.Text2_x = value*6
        self.lbl2.move(self.Text2_x,self.Text2_y)
        self.lbl1.adjustSize()
        self.lbl2.adjustSize()

    def ChangeText_y1(self, value):
        self.Text1_y = value*2
        self.lbl1.move(self.Text1_x,self.Text1_y)
        self.lbl1.adjustSize()
        self.lbl2.adjustSize()

    def ChangeText_y2(self, value):
        self.Text2_y = 400-value
        self.lbl2.move(self.Text2_x,self.Text2_y)
        self.lbl1.adjustSize()
        self.lbl2.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())