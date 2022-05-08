from ui_py.hwid import Ui_hwid

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt


class HwidDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(HwidDialog, self).__init__(parent)
        self.ui = Ui_hwid()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        def move_window(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.drag_pos)
                self.drag_pos = event.globalPos()
                event.accept()

        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.pushButton.clicked.connect(lambda: self.close())

        self.ui.frame_label_top_btns.mouseMoveEvent = move_window

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def set_text(self, text):
        self.ui.label_2.setText(text)

    def set_hwid(self, text):
        self.ui.lineEdit.setText(text)