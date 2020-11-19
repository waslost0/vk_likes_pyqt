# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hwid.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Hwid(object):
    def setupUi(self, Error):
        Error.setObjectName("Error")
        Error.resize(416, 202)
        Error.setMinimumSize(QtCore.QSize(253, 144))
        Error.setStyleSheet("background-color: rgb(32, 42, 47);")
        self.verticalLayoutWidget = QtWidgets.QWidget(Error)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 391, 102))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.lineEdit = QtWidgets.QLineEdit(Error)
        self.lineEdit.setGeometry(QtCore.QRect(10, 130, 381, 41))
        self.lineEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 12pt \"MS Shell Dlg 2\";")
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setFrame(True)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Error)
        QtCore.QMetaObject.connectSlotsByName(Error)

    def retranslateUi(self, Error):
        _translate = QtCore.QCoreApplication.translate
        Error.setWindowTitle(_translate("Error", "Dialog"))
        self.label_2.setText(_translate("Error", "TextLabel"))
