import logging
import time
from datetime import datetime

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from ban_users.BanUsers import BanUsers


class BanUsersGroup(BanUsers):
    def __init__(self, main):
        super().__init__(main)
        self.main = main
        self.user = main.user
        self.current_index = main.ui.stackedWidget.currentIndex()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
        try:
            while True:
                self.user.ban_users_group()
                if self.is_killed:
                    self.info_dialog.set_text(
                        'Wait for task end.\nNew window will appear with info\nIt will take ~75 seconds')
                    self.info_dialog.ui.label_title_bar_top.setText('Info')
                    self.info_dialog.exec_()
                    self.user.change_group_followers_task()

                    while True:
                        if self.user.is_group_task_changed():
                            break
                        self.user.ban_users_group()
                        time.sleep(1)

                    self.user.change_group_followers_task()
                    self.user.clear_group_users(is_all=True)
                    self.info_dialog.set_text('Successful')
                    self.info_dialog.ui.label_title_bar_top.setText('Info')
                    self.info_dialog.ui.label.setPixmap(QPixmap("../../icons/16x16/cil-check-alt.png"))
                    self.info_dialog.ui.frame_content_right.setStyleSheet("background-color: rgb(50, 50, 60);")
                    self.info_dialog.exec_()
                    break
            self.main.runner = None
        except Exception as error:
            logging.error(error)
