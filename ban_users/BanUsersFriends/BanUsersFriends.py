import logging
import time
from datetime import datetime

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap

from ban_users.BanUsers import BanUsers
from bs4 import BeautifulSoup as BS


class BanUsersFriends(BanUsers):
    def __init__(self, main):
        super().__init__(main)
        self.user = main.user
        self.current_index = main.ui.stackedWidget.currentIndex()
        self.is_killed = False
        self.count = main.ui.FriendsCount.text()
        self.reward = main.ui.RewardFriends.text()
        self.combo_box_index = main.ui.comboBox_2.currentIndex()

    @pyqtSlot()
    def run(self):
        try:
            self.user.add_likest_task(task_type='friends', count=self.count, reward=self.reward)
            self.user.get_friends_task_url()
            self.user.time = datetime.now()
            while True:
                self.user.ban_user_friends(reward=self.reward, count=self.count, combo_box_index=self.combo_box_index)
                if self.is_killed:
                    self.info_dialog.set_text(
                        'Wait for task end.\nNew window will appear with info\nIt will take ~75 seconds')
                    self.info_dialog.ui.label_title_bar_top.setText('Info')
                    self.info_dialog.exec_()
                    self.user.change_friends_task(reward=self.reward, count=0)
                    while True:
                        self.user.ban_user_friends(reward=self.reward, count=self.count,
                                                   combo_box_index=self.combo_box_index,
                                                   is_stop=True)
                        if self.user.wait_for_balance_back(reward=self.reward, count=self.count,
                                                           combo_box_index=self.combo_box_index):
                            break
                        time.sleep(2)

                    self.info_dialog.set_text('Successful')
                    self.info_dialog.ui.label_title_bar_top.setText('Info')
                    self.info_dialog.ui.label.setPixmap(QPixmap("../../icons/16x16/cil-check-alt.png"))
                    self.info_dialog.ui.frame_content_right.setStyleSheet("background-color: rgb(50, 50, 60);")
                    self.info_dialog.exec_()
                    break
            self.main.runner = None

        except Exception as error:
            self.user.change_friends_task(reward=self.reward, count=0)
            while True:
                self.user.ban_user_friends(reward=self.reward, count=self.count,
                                           combo_box_index=self.combo_box_index)
                response = self.user.session.get('https://likest.ru/orders/friends')
                soup = BS(response.text, 'lxml')
                items = soup.select('div[class="form-item form-type-item"]')
                if 'Заявок на проверке' not in items[2].text:
                    self.user.clear_add_users_from_bl(self.combo_box_index)
                    self.user.change_friends_task(reward=self.reward, count=0)
                    break
                time.sleep(1)
            logging.error(error)
