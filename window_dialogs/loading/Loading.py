import logging

from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor

from window_dialogs.main.MainWindow import MainWindow
from threads_worker import Worker
from ui_py.ui_splash_screen import Ui_SplashScreen
from PyQt5 import QtCore
from PyQt5.QtCore import QThreadPool


class LoadingDialog(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(15)

        self.main = MainWindow()
        self.ui.progressBar.setTextVisible(False)
        self.threadpool = QThreadPool()

        worker = Worker(self.execute_this_fn)
        self.is_not_subscribed = False
        self.threadpool.start(worker)
        self.show()

        self.counter = 0
        self.is_init_loaded = False

    def execute_this_fn(self, progress_callback):
        logging.info('Init functions...')
        self.main.init_functions()
        self.is_init_loaded = True

    def progress(self):
        if self.is_init_loaded:
            self.counter = 101

        if self.counter > 100:
            self.counter = 7
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(self.counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if self.is_init_loaded:
            self.timer.stop()
            self.threadpool.clear()
            self.close()
            self.main.show()
            if self.main.is_login_likest is False and 'login' in self.main.data:
                self.main.err_dialog.set_text(f"Unsuccessful login likest.")
                self.main.err_dialog.show()
        self.counter += 1
