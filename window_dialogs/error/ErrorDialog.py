from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor

from ui_py.error_ui import Ui_Dialog
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        def move_window(event):
            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_pos)
                self.drag_pos = event.globalPos()
                event.accept()

        self.ui.btn_close.clicked.connect(self.close_window)
        self.ui.pushButton.clicked.connect(self.close_window)

        self.ui.frame_label_top_btns.mouseMoveEvent = move_window

    def close_window(self):
        self.close()

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def set_text(self, text):
        self.ui.label_2.setText(text)
