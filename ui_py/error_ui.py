# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 250)
        Dialog.setMaximumSize(QtCore.QSize(500, 250))
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_main = QtWidgets.QFrame(Dialog)
        self.frame_main.setStyleSheet("")
        self.frame_main.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_top = QtWidgets.QFrame(self.frame_main)
        self.frame_top.setStyleSheet("background-color: transparent;")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_top_right = QtWidgets.QFrame(self.frame_top)
        self.frame_top_right.setStyleSheet("background: transparent;")
        self.frame_top_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_right.setObjectName("frame_top_right")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_top_right)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top_btns = QtWidgets.QFrame(self.frame_top_right)
        self.frame_top_btns.setMaximumSize(QtCore.QSize(16777215, 42))
        self.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_btns.setObjectName("frame_top_btns")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_label_top_btns = QtWidgets.QFrame(self.frame_top_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_label_top_btns.sizePolicy().hasHeightForWidth())
        self.frame_label_top_btns.setSizePolicy(sizePolicy)
        self.frame_label_top_btns.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_label_top_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_label_top_btns.setObjectName("frame_label_top_btns")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_label_top_btns)
        self.horizontalLayout_10.setContentsMargins(5, 0, 10, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label = QtWidgets.QLabel(self.frame_label_top_btns)
        self.label.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.label.setStyleSheet("background: transparent;\n"
"    color:rgb(255, 255, 255);")
        self.label.setText("")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setPixmap(QtGui.QPixmap("icons/24x24/cil-x-circle.png"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        self.label_title_bar_top = QtWidgets.QLabel(self.frame_label_top_btns)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_title_bar_top.setFont(font)
        self.label_title_bar_top.setStyleSheet("background: transparent;\n"
"color:rgb(255, 225, 225)\n"
"\n"
"")
        self.label_title_bar_top.setObjectName("label_title_bar_top")
        self.horizontalLayout_10.addWidget(self.label_title_bar_top)
        self.horizontalLayout_4.addWidget(self.frame_label_top_btns)
        self.frame_btns_right = QtWidgets.QFrame(self.frame_top_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy)
        self.frame_btns_right.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame_btns_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns_right.setObjectName("frame_btns_right")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_close = QtWidgets.QPushButton(self.frame_btns_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(40, 0))
        self.btn_close.setMaximumSize(QtCore.QSize(40, 16777215))
        self.btn_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/16x16/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_5.addWidget(self.btn_close)
        self.horizontalLayout_4.addWidget(self.frame_btns_right, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top_btns)
        self.frame_content_right = QtWidgets.QFrame(self.frame_top_right)
        self.frame_content_right.setStyleSheet("background-color: rgb(50, 49, 60);")
        self.frame_content_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_right.setObjectName("frame_content_right")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_content_right)
        self.gridLayout.setContentsMargins(0, 0, 0, 15)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.frame_content_right)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    border: 1px solid rgb(61, 70, 86);\n"
"    color:rgb(180, 180, 180);\n"
"    border-radius: 5px;    \n"
"    background-color: rgb(52, 59, 72);\n"
"margin-right: 10px;\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(57, 65, 80);\n"
"    border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(35, 40, 49);\n"
"    border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.frame = QtWidgets.QFrame(self.frame_content_right)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setMinimumSize(QtCore.QSize(300, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:rgb(218, 218, 218);\n"
"")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_content_right)
        self.horizontalLayout_3.addWidget(self.frame_top_right)
        self.verticalLayout.addWidget(self.frame_top)
        self.verticalLayout_3.addWidget(self.frame_main)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_title_bar_top.setText(_translate("Dialog", "Error"))
        self.btn_close.setToolTip(_translate("Dialog", "Close"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.label_2.setText(_translate("Dialog", "You must log in"))
