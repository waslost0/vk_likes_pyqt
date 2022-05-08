import logging
from datetime import datetime
import time

from PyQt5.QtCore import QRunnable, pyqtSlot
from PyQt5.QtGui import QPixmap

from window_dialogs.error.ErrorDialog import ErrorDialog


class BanUsers(QRunnable):
    def __init__(self, main, task_type: str = None, reward: str = None, count: str = None):
        super().__init__()
        self.main = main
        self.task_type = task_type
        self.reward = reward
        self.count = count
        self.user = main.user
        self.current_index = main.ui.stackedWidget.currentIndex()
        self.user.count = main.ui.LikesCount.text()
        self.is_killed = False
        self.info_dialog = ErrorDialog()

    @pyqtSlot()
    def run(self):
        self.info_dialog.set_text(
            'Wait for task end.\nNew window will appear with info\nIt will take ~100 seconds or more')
        self.info_dialog.ui.label_title_bar_top.setText('Info')
        self.user.time = datetime.now()
        try:
            while True:
                self.user.ban_user_report(task_type=self.task_type, reward=self.reward, count=self.count)

                if self.is_killed:
                    if self.current_index == 2 and self.main.ui.LikestCheckBox.isChecked():
                        self.info_dialog.exec_()
                        self.user.change_likes_task()
                    elif self.current_index == 3 and self.main.ui.RepostsCheckBox.isChecked():
                        self.info_dialog.exec_()
                        self.user.change_repost_task()

                    if self.main.ui.LikestCheckBox.isChecked() or self.main.ui.RepostsCheckBox.isChecked():
                        while True:
                            self.user.ban_user_report(is_kill=True)
                            if self.current_index == 2:
                                if self.user.check_is_task_changed('like'):
                                    self.user.change_likes_task()
                                    break
                            elif self.current_index == 3:
                                if self.user.check_is_task_changed('repost'):
                                    self.user.change_repost_task()
                                    break
                            time.sleep(1)

                    self.info_dialog.set_text('Successful')
                    self.info_dialog.ui.label_title_bar_top.setText('Info')
                    self.info_dialog.ui.label.setPixmap(QPixmap("../../icons/16x16/cil-check-alt.png"))
                    self.info_dialog.ui.frame_content_right.setStyleSheet("background-color: rgb(50, 50, 60);")
                    self.info_dialog.exec_()
                    break
            self.main.runner = None

        except Exception as error:
            logging.info(error)
            while True:
                self.user.ban_user_report()
                if self.current_index == 2:
                    if self.user.check_is_task_changed('like'):
                        self.user.change_likes_task()
                        break
                elif self.current_index == 3:
                    if self.user.check_is_task_changed('repost'):
                        self.user.change_repost_task()
                        break
                time.sleep(1)

    def kill(self):
        self.is_killed = True
