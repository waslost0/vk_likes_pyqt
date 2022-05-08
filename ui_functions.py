import logging

from PyQt5 import QtCore, QtGui

from helpers.vk_helper import VkHelper
from file_helper import save_data_to_file, load_data_from_file
from ui_styles import Style
from PyQt5.QtCore import QSize, QPropertyAnimation, Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QGraphicsDropShadowEffect

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True


class UIFunctions:
    @staticmethod
    def maximize_restore(main_window):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            main_window.showMaximized()
            GLOBAL_STATE = 1
            main_window.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            main_window.ui.btn_maximize_restore.setToolTip("Restore")
            main_window.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u"icons/16x16/cil-window-restore.png"))
            main_window.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            main_window.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            main_window.showNormal()
            main_window.resize(main_window.width() + 1, main_window.height() + 1)
            main_window.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            main_window.ui.btn_maximize_restore.setToolTip("Maximize")
            main_window.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u"icons/16x16/cil-window-maximize.png"))
            main_window.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            main_window.ui.frame_size_grip.show()

    @staticmethod
    def enable_maximum_size(main_window, width, height):
        if width != '' and height != '':
            main_window.setMaximumSize(QSize(width, height))
            main_window.ui.frame_size_grip.hide()
            main_window.ui.btn_maximize_restore.hide()

    @staticmethod
    def toggle_menu(main_window, max_width, enable):
        if enable:
            # Get width
            width = main_window.ui.frame_left_menu.width()
            max_extend = max_width
            standard = 70

            # Set max width
            if width == 70:
                width_extended = max_extend
            else:
                width_extended = standard

            # Animation
            main_window.animation = QPropertyAnimation(main_window.ui.frame_left_menu, b"minimumWidth")
            main_window.animation.setDuration(300)
            main_window.animation.setStartValue(width)
            main_window.animation.setEndValue(width_extended)
            main_window.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            main_window.animation.start()

    @staticmethod
    def label_title(main_window, text):
        main_window.ui.label_title_bar_top.setText(text)

    @staticmethod
    def label_description(main_window, text):
        main_window.ui.label_top_info_1.setText(text)

    @staticmethod
    def add_new_menu(main_window, name, obj_name, icon, is_top_menu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(main_window)
        button.setObjectName(obj_name)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        # button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(main_window.menu_switcher)

        if is_top_menu:
            main_window.ui.layout_menus.addWidget(button)
        else:
            main_window.ui.layout_menu_bottom.addWidget(button)

    @staticmethod
    def select_menu(current_style):
        select = current_style + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
        return select

    @staticmethod
    def deselect_menu(current_style):
        deselect = current_style.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    # Reset toggle menu buttons style
    @staticmethod
    def reset_style(main_window, widget):
        for w in main_window.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselect_menu(w.styleSheet()))

    # Change page label text
    @staticmethod
    def label_page(main_window, text):
        new_text = '| ' + text.upper()
        main_window.ui.label_top_info_2.setText(new_text)

    # User icon
    @staticmethod
    def user_icon(main_window, initials_tooltip, icon, show_hide):
        if show_hide:
            if icon:
                pixmap = QtGui.QPixmap(icon)
                main_window.ui.label_user_icon.setPixmap(pixmap)
                main_window.ui.label_user_icon.setText('')
                main_window.ui.label_user_icon.setToolTip(initials_tooltip)
        else:
            main_window.ui.label_user_icon.hide()

    @staticmethod
    def return_status():
        return GLOBAL_STATE

    @staticmethod
    def set_status(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    @staticmethod
    def ui_definitions(main_window):
        def double_click_maximize_restore(event):
            # If double click change status
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(main_window))

        # Remove standard title bar
        if GLOBAL_TITLE_BAR:
            main_window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            main_window.ui.frame_label_top_btns.mouseDoubleClickEvent = double_click_maximize_restore
        else:
            main_window.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            main_window.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            main_window.ui.frame_label_top_btns.setMinimumHeight(42)
            main_window.ui.frame_icon_top_bar.hide()
            main_window.ui.frame_btns_right.hide()
            main_window.ui.frame_size_grip.hide()

        # show drop shadow
        main_window.shadow = QGraphicsDropShadowEffect(main_window)
        main_window.shadow.setBlurRadius(17)
        main_window.shadow.setXOffset(0)
        main_window.shadow.setYOffset(0)
        main_window.shadow.setColor(QColor(0, 0, 0, 150))
        main_window.ui.frame_main.setGraphicsEffect(main_window.shadow)

        main_window.url = None
        main_window.data_result = None
        main_window.data = None
        main_window.user = None
        main_window.token = None
        main_window.is_login_likest = False

        main_window.ui.stackedWidget.setCurrentIndex(0)

    @staticmethod
    def login(main_window):
        try:
            logging.info('Trying to load all data from file')
            main_window.data = load_data_from_file()
        except Exception as e:
            logging.error(e)

        if 'login' in main_window.data and 'password' in main_window.data and 'token' in main_window.data:
            main_window.token = main_window.data['token']
            main_window.user = VkWorker(
                username=main_window.data['login'],
                password=main_window.data['password']
            )
            main_window.user.token = main_window.token

            main_window.login_result = main_window.user.login()
            main_window.ui.ResultOfLogin.setText(f"{main_window.login_result}")

            try:
                main_window.is_login_likest = main_window.user.login_likest()
            except Exception as e:
                logging.error(e)

        elif ('token' not in main_window.data) and ('login' in main_window.data):
            main_window.user = VkWorker(username=main_window.data['login'], password=main_window.data['password'])
            main_window.user.login()
            main_window.token = main_window.user.get_token()
            logging.info(f'Your token: {main_window.token}')

            main_window.data_saved = save_data_to_file(
                login=main_window.data['login'],
                password=main_window.data['password'],
                token=main_window.token
            )
            try:
                main_window.is_login_likest = main_window.user.login_likest()
            except Exception as e:
                logging.error(e)
            logging.info(f"Saved data {main_window.data_saved}")
        if 'user_id' in main_window.data:
            main_window.user.user_id = main_window.data['user_id']
