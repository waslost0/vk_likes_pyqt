from ui_functions import *
import logging
import os
import subprocess
import sys
import time
import json
import pickle
import re
import random
import string
import traceback

from random import choice
import requests
from string import Template
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QUrl, Qt, pyqtSlot
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow

from ui_py.main import Ui_MainWindow
from logic import load_data_from_file, User, save_data_to_file
from ui_py.error_ui import Ui_Dialog
from ui_py.ui_splash_screen import Ui_SplashScreen
from ui_py.hwid import Ui_hwid
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)

counter = 0
is_init_loaded = False


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class Handler(QObject, logging.Handler):
    new_record = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__(parent)
        super(logging.Handler).__init__()
        formatter = Formatter('%(filename)s[LINE:%(lineno)-4s] #%(levelname)-4s [%(asctime)s]  %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        self.new_record.emit(msg)


class Formatter(logging.Formatter):
    def formatException(self, ei):
        result = super(Formatter, self).formatException(ei)
        return result

    def format(self, record):
        s = super(Formatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '')
        return s


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        def move_window(event):
            # MOVE WINDOW
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


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class SplashScreen(QMainWindow):
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

        self.threadpool = QThreadPool()
        self.main = MainWindow()
        worker = Worker(self.execute_this_fn)
        self.ui.progressBar.setTextVisible(False)
        self.show()

        # Execute
        self.threadpool.start(worker)

    def print_output(self, s):
        print(s)

    def execute_this_fn(self, progress_callback):
        global is_init_loaded
        is_init_loaded = self.main.init_functions()
        self.threadpool.clear()

    def progress(self):
        global counter
        global is_init_loaded
        if is_init_loaded:
            counter = 101

        if counter == 100:
            counter = 0
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100 and is_init_loaded:
            self.close()
            self.main.show()
            if self.main.is_login_likest is False and 'login' in self.main.data:
                self.main.err_dialog.set_text(f"Unsuccessful login likest.")
                self.main.err_dialog.show()
            self.timer.stop()

        counter += 1


class MainWindow(QMainWindow):
    def __init__(self):
        # super(QMainWindow, self).__init__(parent)
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        UIFunctions.add_new_menu(self, "Home", "vk_login_page", "url(icons/16x16/cil-home.png)", True)
        UIFunctions.add_new_menu(self, "Like", "likes_page", "url(icons/16x16/cil-heart.png)", True)
        UIFunctions.add_new_menu(self, "Repost", "repost_page", "url(icons/16x16/cil-share.png)", True)
        UIFunctions.add_new_menu(self, "Logs", "logs_page", "url(icons/16x16/cil-browser.png)", True)
        UIFunctions.add_new_menu(self, "Settings", "settings_page", "url(icons/16x16/cil-equalizer.png)", True)
        self.ui.btn_toggle_menu.hide()
        # Open telegram urls
        self.ui.waslostUrl.clicked.connect(lambda: self.open_url('https://t.me/waslost'))
        self.ui.label_title_bar_top.clicked.connect(lambda: self.open_url('https://t.me/gracz'))

        # Add custom menus
        self.ui.stackedWidget.setMinimumWidth(20)
        # Widget to move
        self.ui.frame_label_top_btns.mouseMoveEvent = self.move_window
        self.ui.plainTextEdit.setReadOnly(True)

        UIFunctions.ui_definitions(self)

    def move_window(self, event):
        # if maximized change to normal
        if UIFunctions.return_status() == 1:
            UIFunctions.maximize_restore(self)

        # move window
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def init_functions(self):
        # Toggle menu size
        # self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggle_menu(self, 220, False))
        handler = Handler(self)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        handler.new_record.connect(self.ui.plainTextEdit.appendPlainText)

        try:
            logging.info('Trying to load all data from file')
            self.data = load_data_from_file()
        except Exception as e:
            logging.error(e)

        if 'login' in self.data and 'password' in self.data and 'token' in self.data:
            self.token = self.data['token']
            self.user = User(
                username=self.data['login'],
                password=self.data['password']
            )
            self.user.token = self.token

            self.login_result = self.user.login()
            self.ui.ResultOfLogin.setText(f"{self.login_result}")

            try:
                self.is_login_likest = self.user.login_likest()

            except Exception as e:
                logging.error(e)

        elif ('token' not in self.data) and ('login' in self.data):
            self.user = User(username=self.data['login'], password=self.data['password'])
            self.user.login()
            self.token = self.user.get_token()
            lg = Template("Ur token $token")
            logging.info(lg.substitute(self.token))

            self.data_saved = save_data_to_file(
                login=self.data['login'],
                password=self.data['password'],
                token=self.token
            )
            try:
                self.is_login_likest = self.user.login_likest()
            except Exception as e:
                logging.error(e)
            logging.info(f"Saved data {self.data_saved}")
        if 'user_id' in self.data:
            self.user.user_id = self.data['user_id']

        # unban button
        self.threadpool = QThreadPool()
        self.ui.Unban_users_button_2.clicked.connect(self.unban)
        self.ui.Unban_users_button_1.clicked.connect(self.unban)
        self.ui.SaveSettingsButton.hide()

        if self.user:
            if os.path.isfile('icons/vk/user_icon.png'):
                UIFunctions.user_icon(self, 'usericon', 'icons/vk/user_icon.png', True)
            else:
                self.user.get_user_image()
                UIFunctions.user_icon(self, 'usericon', 'icons/vk/user_icon.png', True)
        return True

    def button(self):
        # GET BT CLICKED
        btn_widget = self.sender()
        # Home page
        if btn_widget.objectName() == "vk_login_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.vkLoginPage)
            UIFunctions.reset_style(self, "vkLoginPage")
            UIFunctions.label_page(self, "Home")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

        # Likes
        if btn_widget.objectName() == "likes_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.LikesPage)
            UIFunctions.reset_style(self, "LikesPage")
            UIFunctions.label_page(self, "Likes")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

        # Repost
        if btn_widget.objectName() == "repost_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.RepostPage)
            UIFunctions.reset_style(self, "RepostPage")
            UIFunctions.label_page(self, "Repost")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

        # Repost
        if btn_widget.objectName() == "logs_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.LogsPage)
            UIFunctions.reset_style(self, "LogsPage")
            UIFunctions.label_page(self, "Logs")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

        # Settings
        if btn_widget.objectName() == "settings_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.Settings)
            UIFunctions.reset_style(self, "Settings")
            UIFunctions.label_page(self, "Settings")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))
            if self.user:
                self.ui.UsernameDataSettings.setText(self.user.username)
                self.ui.PasswordDataSettings.setText(self.user.password)
                self.ui.TokenDataSettings.setText(self.user.token)

    @staticmethod
    def open_url(url):
        QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))

    ## EVENT ==> MOUSE DOUBLE CLICK
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def resizeEvent(self, event):
        return super(MainWindow, self).resizeEvent(event)

    def thread_complete(self):
        logging.info("Unban users complete")

    def unban(self):
        if not self.url:
            self.err_dialog.set_text("You must save url")
            self.err_dialog.exec_()
            return

        worker = Worker(self.user.unban_users)
        worker.signals.finished.connect(self.thread_complete)
        # Execute
        self.threadpool.start(worker)

    def save_coupon(self):
        if not self.user:
            self.err_dialog.set_text("You must log in")
            self.err_dialog.exec_()
        else:
            coupon = self.ui.LabelCoupon.text()
            result_coupon = self.user.activate_coupon(coupon)

            if 'SUCCESS' in result_coupon['status']:
                self.ui.ResultCoupon.setStyleSheet("color: rgb(154, 255, 152);")
                self.ui.ResultCoupon.setText('Activated')
            else:
                self.ui.ResultCoupon.setStyleSheet("color: rgb(195, 15, 18);")
                self.ui.ResultCoupon.setText('Not activated')

    def get_likest_balance(self):
        if not self.user:
            self.err_dialog.set_text("You must log in")
            self.err_dialog.exec_()
        else:
            likes_balance = self.user.get_likes_balance()
            if 'balance' in likes_balance:
                cur_bal = likes_balance['balance']
                self.ui.LikesBalanceLabel.setText(str(cur_bal))

    @QtCore.pyqtSlot()
    def start(self):
        if not self.user or not self.data_result:
            if not self.data_result:
                self.err_dialog.set_text("You must add url")
            else:
                self.err_dialog.set_text("You must log in")
            self.err_dialog.exec_()
        else:
            logging.info('Starting ban users.')
            reward = None
            if self.current_window == 3:
                repost_or_like = 'r'
                reward = self.ui.Reward.text()
                repost_count = self.ui.RepostsCount.text()
            else:
                repost_or_like = 'l'
                repost_count = self.ui.LikesCount.text()

            if (self.ui.LikestCheckBox.isChecked() and self.current_window == 2) or (
                    self.ui.RepostsCheckBox.isChecked() and self.current_window == 3) and self.is_login_likest:
                save_data_to_file(url_tolike=self.url, post_id=self.user.item_id)
                self.user.add_likest_task(likes_count=repost_count,
                                          like_url=self.url,
                                          repost_like=repost_or_like,
                                          reward=reward)

                if self.current_window == 3:
                    self.ui.ResultSaveUrl_R.setStyleSheet(
                        self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(154, 255, 152);")
                    self.ui.ResultSaveUrl_R.setText("Task added")
                else:
                    self.ui.ResultSaveUrl.setText("Task added")
            else:
                logging.info('Not log likest')
                if self.is_login_likest is False:
                    self.err_dialog.set_text("You can`t add task. Because you are not logged likes.")
                    self.err_dialog.show()
                if self.current_window == 3:
                    self.ui.ResultSaveUrl_R.setText("You must add a task.")
                else:
                    self.ui.ResultSaveUrl.setText("You must add a task.")

            self.m_thread = QtCore.QThread(self)
            self.m_modbus_worker = BanUsers(self.user)
            self.m_modbus_worker.moveToThread(self.m_thread)
            self.m_thread.start()
            QtCore.QTimer.singleShot(0, self.m_modbus_worker.do_work)

            if self.current_window == 3:
                self.ui.ResultStartLikes_R.setStyleSheet("color: rgb(154, 255, 152);")
                self.ui.ResultStartLikes_R.setText("Started")
            else:
                self.ui.ResultStartLikes.setStyleSheet("color: rgb(154, 255, 152);")
                self.ui.ResultStartLikes.setText("Started")

    @QtCore.pyqtSlot()
    def stop(self):
        # runnable = UnbanUsers(self.user)
        # QThreadPool.globalInstance().start(runnable)
        if self.m_modbus_worker:
            self.m_modbus_worker.stop()
            self.m_modbus_worker.terminate()
        if self.m_thread:
            self.m_thread.requestInterruption()
            self.user.delete_repost()
            if self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultStartLikes.setStyleSheet("color: rgb(154, 255, 152);")
                self.ui.ResultStartLikes.setText("Stopped")
            else:
                self.ui.ResultStartLikes_R.setStyleSheet("color: rgb(154, 255, 152);")
                self.ui.ResultStartLikes_R.setText("Stopped")
            self.m_thread.quit()
            self.m_thread.wait()
            # sys.exit(self.m_thread.exec())

    def save_url(self):
        if not self.user:
            self.err_dialog.set_text("You must log in")
            self.err_dialog.exec_()
        else:
            if self.ui.stackedWidget.currentIndex() == 2 and self.ui.LabelLikesUrl.text() == '':
                self.ui.ResultSaveUrl.setStyleSheet(self.ui.ResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultSaveUrl.setText("Enter url")
                return
            elif self.ui.stackedWidget.currentIndex() == 3 and self.ui.LabelRepostsUrl.text() == '':
                self.ui.ResultSaveUrl_R.setStyleSheet(self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultSaveUrl_R.setText("Enter url")
                return

            if self.ui.stackedWidget.currentIndex() == 3:
                self.url = self.ui.LabelRepostsUrl.text()
            else:
                self.url = self.ui.LabelLikesUrl.text()

            self.data_result = self.user.get_data_from_link(self.url)
            data_from_db = {}

            if not self.data_result:
                if self.ui.stackedWidget.currentIndex() == 2:
                    self.ui.ResultSaveUrl.setStyleSheet(self.ui.ResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                    self.ui.ResultSaveUrl.setText("Invalid url")
                    return
                else:
                    self.ui.ResultSaveUrl_R.setStyleSheet(
                        self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(195, 15, 18);")
                    self.ui.ResultSaveUrl_R.setText("Invalid url")
                    return
            else:
                # repost_result = self.user.make_repost(url)
                data_from_db = save_data_to_file(url_tolike=self.url, post_id=self.data_result[1])
                if self.ui.stackedWidget.currentIndex() == 2:
                    self.ui.ResultSaveUrl.setStyleSheet(
                        self.ui.ResultSaveUrl.styleSheet() + "color: rgb(154, 255, 152);")
                    self.ui.ResultSaveUrl.setText("Saved")
                else:
                    self.ui.ResultSaveUrl_R.setStyleSheet(
                        self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(154, 255, 152);")
                    self.ui.ResultSaveUrl_R.setText("Saved")
                logging.info(self.data_result)

            self.ui.LabelLikesUrl.clear()
            self.ui.LabelRepostsUrl.clear()
            if ('login' and 'password' and 'url') in data_from_db:
                logging.info(data_from_db)

    def vk_login(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if not (login and password):
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
            self.ui.ResultOfLogin.setText("Empty data")
        else:
            self.user = User(login, password)
            login_status = self.user.login()

            if not login_status:
                self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
                self.ui.ResultOfLogin.setText("Unsuccessful login")
            else:
                self.token = self.user.get_token()
                self.data = save_data_to_file(
                    login=login,
                    password=password,
                    token=self.user.token,
                    user_id=self.user.user_id
                )
                self.check_login_result()

    def check_login_result(self):
        if not self.data or not self.data['token']:
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
            self.ui.ResultOfLogin.setText("Unsuccessful login")
        elif self.data['token']:
            if self.ui.checkBox.isChecked():
                self.user.login_likest()
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(154, 255, 152);")
            self.ui.ResultOfLogin.setText("Successful login")


class BanUsers(QThread):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @QtCore.pyqtSlot()
    def do_work(self):
        try:
            while not QtCore.QThread.currentThread().isInterruptionRequested():
                self.user.ban_user_report()
        except Exception as error:
            logging.info(error)
            self.user.delete_repost()

    def stop(self):
        self.wait()


def get_hwid():
    return str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()


def check_hwid():
    response = requests.get("https://pastebin.com/raw/GFQrRHcS")
    user_hwid = get_hwid()
    print(user_hwid)
    if user_hwid in response.text:
        return True
    else:
        return False


if __name__ == '__main__':
    try:
        if check_hwid():
            app = QApplication(sys.argv)
            window = SplashScreen()
            sys.exit(app.exec_())
        else:
            app = QApplication([])
            error_dialog = HwidDialog()
            error_dialog.set_text(f'HWID:')
            error_dialog.set_hwid(get_hwid())
            error_dialog.show()
            app.exec_()
    except Exception as e:
        raise e
