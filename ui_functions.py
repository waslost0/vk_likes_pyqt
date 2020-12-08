from main import *
from ui_styles import Style
from PyQt5.QtCore import QSize, QPropertyAnimation
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QPushButton, QSizeGrip, QSizePolicy, QGraphicsDropShadowEffect

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

counter = 0


class UIFunctions(MainWindow):
    @staticmethod
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u"icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u"icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    @staticmethod
    def enable_maximum_size(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()

    @staticmethod
    def toggle_menu(self, max_width, enable):
        if enable:
            # Get width
            width = self.ui.frame_left_menu.width()
            max_extend = max_width
            standard = 70

            # Set max width
            if width == 70:
                width_extended = max_extend
            else:
                width_extended = standard

            # Animation
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(width_extended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def remove_title_bar(self):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = self

    def label_title(self, text):
        self.ui.label_title_bar_top.setText(text)

    def label_description(self, text):
        self.ui.label_top_info_1.setText(text)

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
        button.clicked.connect(main_window.button)

        if is_top_menu:
            main_window.ui.layout_menus.addWidget(button)
        else:
            main_window.ui.layout_menu_bottom.addWidget(button)

    @staticmethod
    def select_menu(self):
        select = self + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
        return select

    @staticmethod
    def deselect_menu(self):
        deselect = self.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    @staticmethod
    def select_standard_menu(main_window, widget):
        for w in main_window.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.select_menu(w.styleSheet()))

    # Reset toggle menu buttons style
    @staticmethod
    def reset_style(main_window, widget):
        for w in main_window.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselect_menu(w.styleSheet()))

    # Change page label text
    @staticmethod
    def label_page(self, text):
        new_text = '| ' + text.upper()
        self.ui.label_top_info_2.setText(new_text)

    # User icon
    @staticmethod
    def user_icon(self, initials_tooltip, icon, show_hide):
        if show_hide:
            # set text
            # self.ui.label_user_icon.setText(initials_tooltip)

            # SET ICON
            if icon:
                # style = self.ui.label_user_icon.styleSheet()
                # set_icon = "QLabel { image: " + icon + "; }"
                # self.ui.label_user_icon.setStyleSheet(style + set_icon)
                pixmap = QtGui.QPixmap(icon)
                self.ui.label_user_icon.setPixmap(pixmap)
                self.ui.label_user_icon.setText('')
                self.ui.label_user_icon.setToolTip(initials_tooltip)
        else:
            self.ui.label_user_icon.hide()

    @staticmethod
    def return_status():
        return GLOBAL_STATE

    @staticmethod
    def set_status(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    @staticmethod
    def ui_definitions(self):
        def double_click_maximize_restore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = double_click_maximize_restore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()

        ## SHOW ==> DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())

        self.m_thread = None
        self.current_window = None
        self.url = None
        self.err_dialog = ErrorDialog()
        self.data_result = None
        self.m_modbus_worker = None
        self.ui.pushButton_4.clicked.connect(self.vk_login)
        self.ui.SaveUrlButton.clicked.connect(self.save_url)
        self.ui.SaveUrlButton_R.clicked.connect(self.save_url)

        # save coupon
        self.ui.SaveCouponButton.clicked.connect(self.save_coupon)
        # get balance button
        self.ui.getBalance.clicked.connect(self.get_likest_balance)

        self.data = None
        self.user = None
        self.user_id = None
        self.post_id = None
        self.token = None

        self.ui.StopLikes.clicked.connect(self.stop)
        self.ui.StartLikes.clicked.connect(self.start)

        self.ui.StopLikes_R.clicked.connect(self.stop)
        self.ui.StartLikes_R.clicked.connect(self.start)
        self.is_login_likest = False

        self.ui.stackedWidget.setCurrentIndex(0)

    @staticmethod
    def login(self):
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

    def close_window(self):
        self.parent().close()
