import logging
import os
import sys
from datetime import datetime
from string import Template
from PyQt5.QtCore import QThreadPool, QUrl, Qt, pyqtSlot
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QAction, QSizeGrip

from window_dialogs.error import ErrorDialog
from ban_users.BanUsersFriends import BanUsersFriends
from ban_users.BanUsersGroups import BanUsersGroup
from helpers.vk_helper import VkHelper
from threads_worker import Worker
from file_helper import load_data_from_file, save_data_to_file
from ui_functions import UIFunctions
from ui_py.main import Ui_MainWindow
from window_dialogs.logger import Handler
from ban_users.BanUsers import BanUsers

APP_ICON = r'icons/vk/ic.ico'


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_login_likest = None
        self.token = None
        self.user = None
        self.threadpool = QThreadPool()
        self.runner = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        UIFunctions.add_new_menu(self, "Home", "vk_login_page", "url(icons/16x16/cil-home.png)", True)
        UIFunctions.add_new_menu(self, "Like", "likes_page", "url(icons/16x16/cil-heart.png)", True)
        UIFunctions.add_new_menu(self, "Repost", "repost_page", "url(icons/16x16/cil-share.png)", True)
        UIFunctions.add_new_menu(self, "Groups", "groups_followers_page", "url(icons/16x16/cil-people.png)", True)
        UIFunctions.add_new_menu(self, "Friends", "friends_page", "url(icons/24x24/cil-user-follow.png)", True)
        UIFunctions.add_new_menu(self, "Logs", "logs_page", "url(icons/16x16/cil-browser.png)", True)
        UIFunctions.add_new_menu(self, "Settings", "settings_page", "url(icons/16x16/cil-equalizer.png)", True)

        # Open telegram urls
        self.ui.waslostUrl.clicked.connect(lambda: self.open_url('https://t.me/waslost'))
        self.ui.label_title_bar_top.clicked.connect(lambda: self.open_url('https://t.me/'))

        self.ui.pushButton_4.clicked.connect(self.vk_login)
        self.ui.SaveUrlButton.clicked.connect(self.save_url)
        self.ui.SaveUrlButton_R.clicked.connect(self.save_url)
        self.ui.GroupFollowersSaveUrlButton.clicked.connect(self.save_url)

        # error dialog
        self.err_dialog = ErrorDialog()

        # save coupon
        self.ui.SaveCouponButton.clicked.connect(self.save_coupon)
        # get balance button
        self.ui.getBalance.clicked.connect(self.get_likest_balance)

        # Resize window
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # Minimize
        self.ui.btn_minimize.clicked.connect(self.showMinimized)

        # Maximize/Restore
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        # Close application
        self.ui.btn_close.clicked.connect(self.close_window)

        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(APP_ICON))

        self.tray_icon.activated.connect(self.tray_icon_double_click)
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(self.close)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def close_window(self):
        self.threadpool.clear()
        self.tray_icon.hide()
        self.close()
        sys.exit()

    def tray_icon_double_click(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

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
        logging.info('Init functions')
        # Add custom menus
        self.ui.stackedWidget.setMinimumWidth(20)
        # self.ui.checkBox.hide()
        # self.ui.LikestCheckBox.hide()
        # self.ui.RepostsCheckBox.hide()
        self.ui.labelBoxBlenderInstalation_2.setText('Balance')
        self.ui.frame_label_top_btns.mouseMoveEvent = self.move_window
        self.ui.plainTextEdit.setReadOnly(True)

        UIFunctions.ui_definitions(self)
        # self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggle_menu(self, 220, False))
        self.ui.btn_toggle_menu.hide()

        handler = Handler(self)
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.DEBUG)
        handler.new_record.connect(self.ui.plainTextEdit.appendPlainText)

        self.ui.StopLikes.clicked.connect(self.stop)
        self.ui.StartLikes.clicked.connect(self.start)

        self.ui.StopLikes_R.clicked.connect(self.stop)
        self.ui.StartLikes_R.clicked.connect(self.start)

        self.ui.GroupFollowersStart.clicked.connect(self.start)
        self.ui.GroupFollowersStop.clicked.connect(self.stop)

        self.ui.StartFriends.clicked.connect(self.start)
        self.ui.StopFriends.clicked.connect(self.stop)

        try:
            logging.info('Trying to load all data from file')
            self.data = load_data_from_file()
        except Exception as error:
            logging.error(error)

        logging.info(self.data)

        if 'login' in self.data and 'password' in self.data and 'token' in self.data and self.data.get('login') != '' and self.data.get('password') != '':
            self.token = self.data['token']
            self.user = VkHelper(
                username=self.data['login'],
                password=self.data['password']
            )
            self.user.token = self.token

            login_result = self.user.login()
            self.ui.ResultOfLogin.setText(login_result)

            try:
                self.is_login_likest = self.user.login_likest(self.user.token)
            except Exception as e:
                logging.error(e)

        elif ('token' not in self.data) and ('login' in self.data) and self.data.get('login') != '' and self.data.get('password') != '':
            self.user = VkHelper(username=self.data['login'], password=self.data['password'])
            self.user.login()
            self.token = self.user.token
            lg = Template("Ur token $token")
            logging.info(lg.substitute(self.token))

            self.data_saved = save_data_to_file(
                login=self.data['login'],
                password=self.data['password'],
                token=self.token
            )
            try:
                self.is_login_likest = self.user.login_likest(self.user.token)
            except Exception as error:
                logging.error(error)
            logging.info(f"Saved data {self.data_saved}")
        if 'user_id' in self.data and self.user and self.user.user_id:
            self.user.user_id = self.data['user_id']

        # unban button
        self.ui.clear_black_list_button.clicked.connect(self.clear_blacklist)
        self.update_icon()
        return True

    def update_icon(self):
        if self.user:
            if os.path.isfile('../../icons/vk/user_icon.png'):
                UIFunctions.user_icon(self, 'usericon', 'icons/vk/user_icon.png', True)
            else:
                self.user.get_user_image()
                UIFunctions.user_icon(self, 'usericon', 'icons/vk/user_icon.png', True)

    def clear_blacklist(self):
        if self.ui.black_list_url.text() == '' and self.ui.comboBox.currentIndex() == 1:
            self.err_dialog.set_text('Enter url')
            self.err_dialog.show()
            return

        url = self.ui.black_list_url.text()
        # main page
        if self.ui.comboBox.currentIndex() == 0:
            worker = Worker(self.user.clear_black_list_main_page, url)
            worker.signals.finished.connect(self.thread_complete)
        # public
        else:
            worker = Worker(self.user.clear_black_list_public, url)
            worker.signals.finished.connect(self.thread_complete)

        # Execute
        self.threadpool.start(worker)

    def menu_switcher(self):
        # get bt clicked
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

        # Groups followers
        if btn_widget.objectName() == "groups_followers_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.GroupFollowersPage)
            UIFunctions.reset_style(self, "Followers")
            UIFunctions.label_page(self, "Followers")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

        # Friend page
        if btn_widget.objectName() == "friends_page":
            self.ui.stackedWidget.setCurrentWidget(self.ui.FriendsPage)
            UIFunctions.reset_style(self, "Friends")
            UIFunctions.label_page(self, "Friends")
            btn_widget.setStyleSheet(UIFunctions.select_menu(btn_widget.styleSheet()))

    @staticmethod
    def open_url(url):
        QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def resizeEvent(self, event):
        return super(MainWindow, self).resizeEvent(event)

    @staticmethod
    def thread_complete():
        logging.info("Unban users complete")

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
            likest_balance = self.user.get_likes_balance()
            if likest_balance:
                self.ui.LikesBalanceLabel.setText(str(likest_balance))

    @pyqtSlot()
    def start(self):
        if self.runner is not None:
            self.err_dialog.set_text('Current thread running')
            self.err_dialog.show()
            return

        if self.ui.stackedWidget.currentIndex() == 5:
            self.data_result = 'fr'

        if not self.user or not self.data_result:
            if not self.data_result:
                self.err_dialog.set_text("You must add url")
            else:
                self.err_dialog.set_text("You must log in")
            self.err_dialog.show()
        else:
            if self.ui.LikesCount.text() == '' and self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultSaveUrl.setStyleSheet(
                    self.ui.ResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultSaveUrl.setText("Enter likes count")
                return

            elif self.ui.RepostsCount.text() == '' and self.ui.ResultStartLikes_R.text() == '' and self.ui.stackedWidget.currentIndex() == 3:
                self.ui.ResultStartLikes_R.setStyleSheet(
                    self.ui.ResultStartLikes_R.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultStartLikes_R.setText("Enter count/reward count")
                return
            elif self.ui.GroupFollowersCount.text() == '' and self.ui.GroupFollowersReward.text() == '' and self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultSaveUrl.setStyleSheet(
                    self.ui.GroupFollowersResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.GroupFollowersResultSaveUrl.setText("Enter count/reward count")
                return

            logging.info('Starting ban users.')
            if not self.user.group_id and self.ui.stackedWidget.currentIndex() != 5:
                self.user.get_group_id()

            if self.ui.stackedWidget.currentIndex() == 4:
                self.runner = BanUsersGroup(self)
            elif self.ui.stackedWidget.currentIndex() == 2:
                self.runner = BanUsers(self, task_type='like')
            elif self.ui.stackedWidget.currentIndex() == 3:
                self.runner = BanUsers(self, task_type='repost', count=self.ui.RepostsCount.text(), reward=self.ui.Reward.text())
            elif self.ui.stackedWidget.currentIndex() == 5:
                self.runner = BanUsersFriends(self)

            self.user.users_hash = self.user.get_group_users_hash()
            save_data_to_file(url_tolike=self.url, post_id=self.user.item_id)

            if self.is_login_likest:

                if self.ui.LikestCheckBox.isChecked() and self.ui.stackedWidget.currentIndex() == 2:
                    count = self.ui.LikesCount.text()
                    self.user.add_likest_task(task_type='like', count=count, url=self.url)

                elif self.ui.RepostsCheckBox.isChecked() and self.ui.stackedWidget.currentIndex() == 3:
                    count = self.ui.RepostsCount.text()
                    reward = self.ui.Reward.text()
                    self.user.add_likest_task(task_type='repost', count=count, reward=reward, url=self.url)

                elif self.ui.stackedWidget.currentIndex() == 4:
                    count = self.ui.GroupFollowersCount.text()
                    reward = self.ui.GroupFollowersReward.text()
                    self.user.add_likest_task(task_type='followers', count=count, reward=reward, url=self.url)
                    self.user.time = datetime.now()
                elif self.ui.stackedWidget.currentIndex() == 5:
                    count = self.ui.FriendsCount.text()
                    reward = self.ui.RewardFriends.text()

            else:
                if self.is_login_likest is False:
                    self.err_dialog.set_text("You can`t add task. Because you are not logged likes.")
                    self.err_dialog.show()
                if self.ui.stackedWidget.currentIndex() == 3:
                    self.ui.ResultSaveUrl_R.setText("You must add a task.")
                else:
                    self.ui.ResultSaveUrl.setText("You must add a task.")

            if self.ui.stackedWidget.currentIndex() == 3:
                self.ui.ResultStartLikes_R.setText("Started")
            elif self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultStart.setText("Started")
            elif self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultStartLikes.setText("Started")
            else:
                self.ui.ResultStartFriends.setText("Started")

            self.threadpool.start(self.runner)


    @pyqtSlot()
    def stop(self):
        if self.runner:
            self.runner.kill()
            # self.user.delete_repost()
            if self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultStartLikes.setText("Stopped")
            elif self.ui.stackedWidget.currentIndex() == 3:
                self.ui.ResultStartLikes_R.setText("Stopped")
            elif self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultStart.setText("Stopped")
            elif self.ui.stackedWidget.currentIndex() == 5:
                self.ui.ResultStartFriends.setText("Stopped")

            if self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultSaveUrl.clear()
            elif self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultSaveUrl.clear()
            elif self.ui.stackedWidget.currentIndex() == 3:
                self.ui.ResultSaveUrl_R.clear()
            self.threadpool.clear()

    def save_url(self):
        if not self.user:
            self.err_dialog.set_text("You must log in")
            self.err_dialog.exec_()
            return

        if self.ui.stackedWidget.currentIndex() == 2 and self.ui.LabelLikesUrl.text() == '':
            self.ui.ResultSaveUrl.setStyleSheet(self.ui.ResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
            self.ui.ResultSaveUrl.setText("Enter url")
            return
        elif self.ui.stackedWidget.currentIndex() == 3 and self.ui.LabelRepostsUrl.text() == '':
            self.ui.ResultSaveUrl_R.setStyleSheet(self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(195, 15, 18);")
            self.ui.ResultSaveUrl_R.setText("Enter url")
            return
        elif self.ui.stackedWidget.currentIndex() == 4 and self.ui.GroupFollowersUrl.text() == '':
            self.ui.GroupFollowersResultSaveUrl.setStyleSheet(
                self.ui.GroupFollowersResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
            self.ui.GroupFollowersResultSaveUrl.setText("Enter url")
            return

        if self.ui.stackedWidget.currentIndex() == 3:
            self.url = self.ui.LabelRepostsUrl.text()
        elif self.ui.stackedWidget.currentIndex() == 4:
            self.url = self.ui.GroupFollowersUrl.text()
        else:
            self.url = self.ui.LabelLikesUrl.text()
        self.user.url = self.url

        if self.ui.stackedWidget.currentIndex() == 4:
            self.data_result = self.user.get_data_from_link(link_to_search=self.url, is_likes_reposts=False)
        else:
            self.data_result = self.user.get_data_from_link(link_to_search=self.url, is_likes_reposts=True)
        data_from_db = {}

        if not self.data_result:
            if self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultSaveUrl.setStyleSheet(self.ui.ResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultSaveUrl.setText("Invalid url")
            elif self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultSaveUrl.setStyleSheet(
                    self.ui.GroupFollowersResultSaveUrl.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.GroupFollowersResultSaveUrl.setText("Invalid url")
            elif self.ui.stackedWidget.currentIndex() == 3:
                self.ui.ResultSaveUrl_R.setStyleSheet(
                    self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(195, 15, 18);")
                self.ui.ResultSaveUrl_R.setText("Invalid url")
        else:
            data_from_db = save_data_to_file(url_tolike=self.url, post_id=self.data_result[1])
            if self.ui.stackedWidget.currentIndex() == 2:
                self.ui.ResultSaveUrl.setStyleSheet(
                    self.ui.ResultSaveUrl.styleSheet() + "color: rgb(154, 255, 152);")
                self.ui.ResultSaveUrl.setText("Saved")
            elif self.ui.stackedWidget.currentIndex() == 4:
                self.ui.GroupFollowersResultSaveUrl.setStyleSheet(
                    self.ui.GroupFollowersResultSaveUrl.styleSheet() + "color: rgb(154, 255, 152);")
                self.ui.GroupFollowersResultSaveUrl.setText("Saved")
            else:
                self.ui.ResultSaveUrl_R.setStyleSheet(
                    self.ui.ResultSaveUrl_R.styleSheet() + "color: rgb(154, 255, 152);")
                self.ui.ResultSaveUrl_R.setText("Saved")
            logging.info(self.data_result)

        if ('login' and 'password' and 'url') in data_from_db:
            logging.info(data_from_db)

    def vk_login(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if not (login and password):
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
            self.ui.ResultOfLogin.setText("Empty data")
        else:
            self.user = VkHelper(login, password)
            if os.path.isfile('../../cookies'):
                os.remove('../../cookies')
            login_status = self.user.login()

            if not login_status:
                self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
                self.ui.ResultOfLogin.setText("Unsuccessful login")
            else:
                self.token = self.user.token

                self.data = save_data_to_file(
                    login=login,
                    password=password,
                    token=self.user.token,
                    user_id=self.user.user_id
                )
                self.check_login_result()

                if os.path.isfile('../../icons/vk/user_icon.png'):
                    os.remove('../../icons/vk/user_icon.png')
                self.user.get_user_image()
                UIFunctions.user_icon(self, 'usericon', 'icons/vk/user_icon.png', True)

    def check_login_result(self):
        if not self.data or not self.data['token']:
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(255, 121, 123);")
            self.ui.ResultOfLogin.setText("Unsuccessful login")
        elif self.data['token']:
            if self.ui.checkBox.isChecked():
                self.is_login_likest = self.user.login_likest(self.user.token)
            self.ui.ResultOfLogin.setStyleSheet("color: rgb(154, 255, 152);")
            self.ui.ResultOfLogin.setText("Successful login")