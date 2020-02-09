import logging
import os
import sys
import time
from string import Template
from PyQt5 import QtCore, QtGui, QtWidgets
from ui_py.test_ui import Ui_MainWindow
from logic import load_data_from_file, User, save_data_to_file
from ui_py.error_ui import Ui_Error


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)
        self.widget.setReadOnly(True)
        self.widget.setFixedSize(680, 420)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class ErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ErrorDialog, self).__init__(parent)
        self.ui = Ui_Error()
        self.ui.setupUi(self)

    def set_text(self, text):
        self.ui.label.setText(text)


class MyyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyyWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        # error dialog
        self.err_dialog = ErrorDialog()
        # подключение клик-сигнал к слоту btnClicked
        self.ui.LikesButton.clicked.connect(self.set_page_view_likes)
        self.ui.LogsButton.clicked.connect(self.set_page_view_logs)
        self.ui.VkLoginButton.clicked.connect(self.set_page_view_vklogin)
        self.ui.vkImage.setPixmap(QtGui.QPixmap(resource_path('vk.png')))
        # Get login pass
        self.ui.pushButton_4.clicked.connect(self.vk_login)
        self.ui.SaveUrlButton.clicked.connect(self.save_url)
        # save coupong
        self.ui.SaveCouponButton.clicked.connect(self.save_coupon)
        # get balance button
        self.ui.getBalance.clicked.connect(self.get_likest_balance)
        # logs
        log_handler = QTextEditLogger(self.ui.plainTextEdit)
        log_handler.setFormatter(
            logging.Formatter('%(filename)s[LINE:%(lineno)-4s]'
                              ' #%(levelname)-4s [%(asctime)s]  %(message)s'))
        logging.getLogger().addHandler(log_handler)

        # async data loader
        # self.d_thread = QtCore.QThread()
        # self.data_loader = DataLoader(self)
        # self.data_loader.moveToThread(self.d_thread)
        # self.d_thread.start()
        # QtCore.QTimer.singleShot(0, self.data_loader.loading_data)

        self.data = None
        self.user = None
        self.user_id = None
        self.post_id = None
        self.token = None
        # self.loading_data()

        # start stop buttons
        self.ui.StopLikes.clicked.connect(self.stop)
        self.ui.StartLikes.clicked.connect(self.start)

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

            self.login_result = self.user.login()
            self.ui.ResultOfLogin.setText(f"Welcome back {self.login_result}")
            self.user.login_likest()

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
            self.user.login_likest()
            logging.info(f"Saved data {self.data_saved}")
        if 'user_id' in self.data:
            self.user.user_id = self.data['user_id']

    def set_state(self):
        pass

    def save_coupon(self):
        coupon = self.ui.LabelCoupon.text()
        result_coupon = self.user.activate_coupon(coupon)

        if 'SUCCESS' in result_coupon['status']:
            self.ui.ResultCoupon.setStyleSheet("color: rgb(154, 255, 152);")
            self.ui.ResultCoupon.setText('Activated')
        else:
            self.ui.ResultCoupon.setStyleSheet("color: rgb(195, 15, 18);")
            self.ui.ResultCoupon.setText('Not activated')

    def get_likest_balance(self):
        self.likes_balance = self.user.get_likes_balance()
        if 'balance' in self.likes_balance:
            cur_bal = self.likes_balance['balance']
            self.ui.LikesBalanceLabel.setText(str(cur_bal))

    def on_succ_login(self):
        if self.login_result:
            logging.info('Data loaded. Token loaded. User session created.')
            self.ui.stackedWidget.setCurrentIndex(2)
            # self.user.login_likest()

        if 'user_id' not in self.data:
            self.user_id = self.user.get_user_id()
            self.data_saved = save_data_to_file(user_id=self.user_id)

    @QtCore.pyqtSlot()
    def start(self):

        logging.info('Starting ban/')
        if self.ui.LikestCheckBox.isChecked():
            like_url = f'https://vk.com/id{self.user.user_id}?' \
                                 f'w=wall{self.user.user_id}_{self.user.item_id}'
            save_data_to_file(url_tolike=like_url, post_id=self.user.item_id)
            self.user.add_likest_task(self.ui.LikesCount.text(), like_url)
            self.ui.ResultSaveUrl.setText("Task added!")
        else:
            logging.info('Not log likest')
            self.ui.ResultSaveUrl.setText("U should add a task.")

        self.m_thread = QtCore.QThread(self)
        self.m_modbus_worker = ModbusWorker(self.user)
        self.m_modbus_worker.moveToThread(self.m_thread)
        self.m_thread.start()
        QtCore.QTimer.singleShot(0, self.m_modbus_worker.do_work)
        self.ui.ResultStartLikes.setStyleSheet("color: rgb(154, 255, 152);")
        self.ui.ResultStartLikes.setText("Started!")

    @QtCore.pyqtSlot()
    def stop(self):
        self.m_thread.requestInterruption()
        self.ui.ResultStartLikes.setStyleSheet("color: rgb(195, 15, 18);")
        self.ui.ResultStartLikes.setText("Stopped!")
        self.user.delete_repost()

    def save_url(self):
        url = self.ui.LabelLikesUrl.text()
        data_result = self.user.get_data_from_link(url)
        data_from_db = {}

        if not url:
            self.ui.ResultSaveUrl.setStyleSheet("color: rgb(195, 15, 18);")
            self.ui.ResultSaveUrl.setText("Enter Url")
        elif not data_result:
            self.ui.ResultSaveUrl.setStyleSheet("color: rgb(195, 15, 18);")
            self.ui.ResultSaveUrl.setText("Invalid url as u")
        else:
            repost_result = self.user.make_repost(url)
            data_from_db = save_data_to_file(url_tolike=url, post_id=data_result[1])
            self.ui.ResultSaveUrl.setStyleSheet("color: rgb(154, 255, 152);")
            self.ui.ResultSaveUrl.setText("Saved")
            logging.info(data_result)

        if ('login' and 'password' and 'url') in data_from_db:
            logging.info(data_from_db)

    def set_page_view_likes(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def set_page_view_logs(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def set_page_view_vklogin(self):
        self.ui.stackedWidget.setCurrentIndex(0)

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
                self.ui.ResultOfLogin.setText("Unsuccessful login.\nInvalid email of password.")
            else:
                self.token = self.user.get_token()
                self.data = save_data_to_file(
                    login=login,
                    password=password,
                    token=self.user.token,
                    user_id=self.user.user_id
                )
                self.check_login_result(self.data)

    def check_login_result(self, data):
        if not self.data or not self.data['token']:
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
            self.ui.ResultOfLogin.setText("Unsuccessful login")
        elif self.data['token']:
            self.user.login_likest()
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(154, 255, 152);")
            self.ui.ResultOfLogin.setText("Successful login\nData saved to data.txt")


class ModbusWorker(QtCore.QObject):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @QtCore.pyqtSlot()
    def do_work(self):
        while not QtCore.QThread.currentThread().isInterruptionRequested():
            # add likest task and start listen likes
            res = self.user.ban_users()
            time.sleep(1)
            
            if res:
                if 'error' in res:
                    logging.error(res['error']['error_msg'])
                    self.user.delete_repost()
                    break

# async dataloader
# class DataLoader(QtCore.QObject):
#     def __init__(self, parent=None):
#         super(DataLoader, self).__init__(parent)
#         self.err_dialog = ErrorDialog()
#
#     @QtCore.pyqtSlot()
#     def loading_data(self):
#         try:
#             logging.info('Trying to load all data from file')
#             self.data = load_data_from_file()
#
#         except Exception as e:
#             logging.error(e)
#         else:
#             if not self.data:
#                 self.err_dialog.set_text('Data is empty. You must log in!')
#                 self.err_dialog.show()
#                 logging.info('Data is empty. You must log in!')
#             else:
#                 logging.info(self.data)
#
#         if 'login' in self.data and 'password' in self.data and 'token' in self.data:
#             self.token = self.data['token']
#             self.user = User(username=self.data['login'], password=self.data['password'], token=self.data['token'])
#             self.login_result = self.user.login()
#
#         elif ('token' not in self.data) and ('login' in self.data):
#             self.user = User(username=self.data['login'], password=self.data['password'])
#             self.user.login()
#             self.token = self.user.get_token()
#             logging.info(f"Ur token {self.token}")
#             self.data_saved = save_data_to_file(login=self.data['login'], password=self.data['password'],
#                                                 token=self.token)
#             logging.info("Saved data %(data)", self.data_saved)
#
#         print('LOADED')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')
    application = MyyWindow()
    application.show()
    sys.exit(app.exec())

'''
beta.alfaliker.com /бан ссылки 10-15 мин
turboliker.ru
likes.fm
snebes.ru
freelikes.online net
'''
