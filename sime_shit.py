#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

class Dialog(QDialog):
    def __init__(self,  parent = None):
        super(Dialog,  self).__init__(parent)
        self.resize(13578, 9585)
        masterLayout = QHBoxLayout(self)
        mainLayout = QVBoxLayout()
        self.pictureLabel = QLabel()
        mainLayout.addWidget(self.pictureLabel)
        self.status_Label = QLabel('100')
        masterLayout.addLayout(mainLayout)
        self.img_refresh()

    def img_refresh(self):
        imagem = QPixmap('373ун34.0402.128_14400696_2735.tif')
        myScaledPixmap = imagem.scaled(13578, 9585)
        self.pictureLabel.setPixmap(myScaledPixmap)
        self.setWindowTitle('test')

def main():
    app = QApplication(sys.argv)
    form = Dialog()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()