import logging #line:1
import os #line:2
import subprocess #line:3
import sys #line:4
import time #line:5
import json #line:6
import pickle #line:7
import re #line:8
import random #line:9
import string #line:10
import lxml #line:11
import requests #line:12
from string import Template #line:13
from PyQt5 import QtCore ,QtGui ,QtWidgets #line:14
from PyQt5 .QtCore import QThread #line:15
from PyQt5 .QtWidgets import QMessageBox #line:16
from ui_py .test_ui import Ui_MainWindow #line:18
from logic import load_data_from_file ,User ,save_data_to_file #line:19
from ui_py .error_ui import Ui_Error #line:20
from bs4 import BeautifulSoup as BS #line:21
def resource_path (O0OOOO00000O0OOO0 ):#line:24
    ""#line:25
    """ Get absolute path to resource, works for dev and for PyInstaller """#line:26
    OO00OOO000OOO00O0 =getattr (sys ,'_MEIPASS',os .path .dirname (os .path .abspath (__file__ )))#line:27
    return os .path .join (OO00OOO000OOO00O0 ,O0OOOO00000O0OOO0 )#line:28
class QTextEditLogger (logging .Handler ):#line:31
    def __init__ (O0OO0000O0OO00OOO ,O000O0O0O0O000O00 ):#line:32
        super ().__init__ ()#line:33
        O0OO0000O0OO00OOO .widget =QtWidgets .QPlainTextEdit (O000O0O0O0O000O00 )#line:34
        O0OO0000O0OO00OOO .widget .setReadOnly (True )#line:35
        O0OO0000O0OO00OOO .widget .setFixedSize (680 ,420 )#line:36
    def emit (OO0O000OO000O0O00 ,OO0OOO0O000OOOOOO ):#line:38
        O00000OOOO0000O0O =OO0O000OO000O0O00 .format (OO0OOO0O000OOOOOO )#line:39
        OO0O000OO000O0O00 .widget .appendPlainText (O00000OOOO0000O0O )#line:40
class ErrorDialog (QtWidgets .QDialog ):#line:43
    def __init__ (OO000O00O00OO0O00 ,parent =None ):#line:44
        super (ErrorDialog ,OO000O00O00OO0O00 ).__init__ (parent )#line:45
        OO000O00O00OO0O00 .ui =Ui_Error ()#line:46
        OO000O00O00OO0O00 .ui .setupUi (OO000O00O00OO0O00 )#line:47
    def set_text (O0OO00O0O0O00OO00 ,OO0OOOOOOO0O000OO ):#line:49
        O0OO00O0O0O00OO00 .ui .label .setText (OO0OOOOOOO0O000OO )#line:50
class MyyWindow (QtWidgets .QMainWindow ):#line:53
    def __init__ (O000O0OOO0O000OOO ):#line:54
        super (MyyWindow ,O000O0OOO0O000OOO ).__init__ ()#line:55
        O000O0OOO0O000OOO .m_thread =None #line:56
        O000O0OOO0O000OOO .current_window =None #line:57
        O000O0OOO0O000OOO .ui =Ui_MainWindow ()#line:58
        O000O0OOO0O000OOO .ui .setupUi (O000O0OOO0O000OOO )#line:59
        O000O0OOO0O000OOO .ui .stackedWidget .setCurrentIndex (0 )#line:60
        O000O0OOO0O000OOO .err_dialog =ErrorDialog ()#line:63
        O000O0OOO0O000OOO .data_result =None #line:64
        O000O0OOO0O000OOO .m_modbus_worker =None #line:65
        O000O0OOO0O000OOO .ui .LikesButton .clicked .connect (O000O0OOO0O000OOO .set_page_view_likes )#line:67
        O000O0OOO0O000OOO .ui .LogsButton .clicked .connect (O000O0OOO0O000OOO .set_page_view_logs )#line:68
        O000O0OOO0O000OOO .ui .VkLoginButton .clicked .connect (O000O0OOO0O000OOO .set_page_view_vklogin )#line:69
        O000O0OOO0O000OOO .ui .vkImage .setPixmap (QtGui .QPixmap (resource_path ('vk.png')))#line:70
        O000O0OOO0O000OOO .ui .pushButton_4 .clicked .connect (O000O0OOO0O000OOO .vk_login )#line:72
        O000O0OOO0O000OOO .ui .SaveUrlButton .clicked .connect (O000O0OOO0O000OOO .save_url )#line:73
        O000O0OOO0O000OOO .ui .SaveUrlButton_R .clicked .connect (O000O0OOO0O000OOO .save_url )#line:74
        O000O0OOO0O000OOO .ui .SaveCouponButton .clicked .connect (O000O0OOO0O000OOO .save_coupon )#line:77
        O000O0OOO0O000OOO .ui .getBalance .clicked .connect (O000O0OOO0O000OOO .get_likest_balance )#line:79
        O000O0OOO0O000OOO .ui .ReposButton .clicked .connect (O000O0OOO0O000OOO .set_page_view_repost )#line:80
        O0O0OOOO0000O00O0 =QTextEditLogger (O000O0OOO0O000OOO .ui .plainTextEdit )#line:82
        O0O0OOOO0000O00O0 .setFormatter (logging .Formatter ('%(filename)s[LINE:%(lineno)-4s]' ' #%(levelname)-4s [%(asctime)s]  %(message)s'))#line:85
        logging .getLogger ().addHandler (O0O0OOOO0000O00O0 )#line:86
        O000O0OOO0O000OOO .data =None #line:88
        O000O0OOO0O000OOO .user =None #line:89
        O000O0OOO0O000OOO .user_id =None #line:90
        O000O0OOO0O000OOO .post_id =None #line:91
        O000O0OOO0O000OOO .token =None #line:92
        O000O0OOO0O000OOO .ui .StopLikes .clicked .connect (O000O0OOO0O000OOO .stop )#line:96
        O000O0OOO0O000OOO .ui .StartLikes .clicked .connect (O000O0OOO0O000OOO .start )#line:97
        O000O0OOO0O000OOO .ui .StopLikes_R .clicked .connect (O000O0OOO0O000OOO .stop )#line:99
        O000O0OOO0O000OOO .ui .StartLikes_R .clicked .connect (O000O0OOO0O000OOO .start )#line:100
        try :#line:102
            logging .info ('Trying to load all data from file')#line:103
            O000O0OOO0O000OOO .data =load_data_from_file ()#line:104
        except Exception as OOOO0OOOOOOO0OOO0 :#line:106
            logging .error (OOOO0OOOOOOO0OOO0 )#line:107
        if 'login'in O000O0OOO0O000OOO .data and 'password'in O000O0OOO0O000OOO .data and 'token'in O000O0OOO0O000OOO .data :#line:109
            O000O0OOO0O000OOO .token =O000O0OOO0O000OOO .data ['token']#line:110
            O000O0OOO0O000OOO .user =User (username =O000O0OOO0O000OOO .data ['login'],password =O000O0OOO0O000OOO .data ['password'])#line:114
            O000O0OOO0O000OOO .login_result =O000O0OOO0O000OOO .user .login ()#line:116
            O000O0OOO0O000OOO .ui .ResultOfLogin .setText (f"Welcome back {O000O0OOO0O000OOO.login_result}")#line:117
            O000O0OOO0O000OOO .user .login_likest ()#line:118
        elif ('token'not in O000O0OOO0O000OOO .data )and ('login'in O000O0OOO0O000OOO .data ):#line:120
            O000O0OOO0O000OOO .user =User (username =O000O0OOO0O000OOO .data ['login'],password =O000O0OOO0O000OOO .data ['password'])#line:121
            O000O0OOO0O000OOO .user .login ()#line:122
            O000O0OOO0O000OOO .token =O000O0OOO0O000OOO .user .get_token ()#line:123
            O00OO0O00OOOOOO00 =Template ("Ur token $token")#line:124
            logging .info (O00OO0O00OOOOOO00 .substitute (O000O0OOO0O000OOO .token ))#line:125
            O000O0OOO0O000OOO .data_saved =save_data_to_file (login =O000O0OOO0O000OOO .data ['login'],password =O000O0OOO0O000OOO .data ['password'],token =O000O0OOO0O000OOO .token )#line:131
            O000O0OOO0O000OOO .user .login_likest ()#line:132
            logging .info (f"Saved data {O000O0OOO0O000OOO.data_saved}")#line:133
        if 'user_id'in O000O0OOO0O000OOO .data :#line:134
            O000O0OOO0O000OOO .user .user_id =O000O0OOO0O000OOO .data ['user_id']#line:135
    def save_coupon (O000O00OO000O0O00 ):#line:137
        if not O000O00OO000O0O00 .user :#line:138
            O000O00OO000O0O00 .err_dialog .set_text ("You must log in")#line:139
            O000O00OO000O0O00 .err_dialog .exec_ ()#line:140
        else :#line:141
            O0000O0O0O0O0000O =O000O00OO000O0O00 .ui .LabelCoupon .text ()#line:142
            OOOO0O0O00OO0OOOO =O000O00OO000O0O00 .user .activate_coupon (O0000O0O0O0O0000O )#line:143
            if 'SUCCESS'in OOOO0O0O00OO0OOOO ['status']:#line:145
                O000O00OO000O0O00 .ui .ResultCoupon .setStyleSheet ("color: rgb(154, 255, 152);")#line:146
                O000O00OO000O0O00 .ui .ResultCoupon .setText ('Activated')#line:147
            else :#line:148
                O000O00OO000O0O00 .ui .ResultCoupon .setStyleSheet ("color: rgb(195, 15, 18);")#line:149
                O000O00OO000O0O00 .ui .ResultCoupon .setText ('Not activated')#line:150
    def get_likest_balance (O0OO000OO000O0O0O ):#line:152
        if not O0OO000OO000O0O0O .user :#line:153
            O0OO000OO000O0O0O .err_dialog .set_text ("You must log in")#line:154
            O0OO000OO000O0O0O .err_dialog .exec_ ()#line:155
        else :#line:156
            O0OO000OO000O0O0O .likes_balance =O0OO000OO000O0O0O .user .get_likes_balance ()#line:157
            if 'balance'in O0OO000OO000O0O0O .likes_balance :#line:158
                OO00OO0O0OO0OO0O0 =O0OO000OO000O0O0O .likes_balance ['balance']#line:159
                O0OO000OO000O0O0O .ui .LikesBalanceLabel .setText (str (OO00OO0O0OO0OO0O0 ))#line:160
    def on_succ_login (OOOO0O0OO00OOO00O ):#line:162
        if OOOO0O0OO00OOO00O .login_result :#line:163
            logging .info ('Data loaded. Token loaded. User session created.')#line:164
            OOOO0O0OO00OOO00O .ui .stackedWidget .setCurrentIndex (2 )#line:165
        if 'user_id'not in OOOO0O0OO00OOO00O .data :#line:168
            OOOO0O0OO00OOO00O .user_id =OOOO0O0OO00OOO00O .user .get_user_id ()#line:169
            OOOO0O0OO00OOO00O .data_saved =save_data_to_file (user_id =OOOO0O0OO00OOO00O .user_id )#line:170
    @QtCore .pyqtSlot ()#line:172
    def start (OOOOOOO0000000OO0 ):#line:173
        if not OOOOOOO0000000OO0 .user or not OOOOOOO0000000OO0 .data_result :#line:174
            if not OOOOOOO0000000OO0 .data_result :#line:175
                OOOOOOO0000000OO0 .err_dialog .set_text ("You must add url")#line:176
            else :#line:177
                OOOOOOO0000000OO0 .err_dialog .set_text ("You must log in")#line:178
            OOOOOOO0000000OO0 .err_dialog .exec_ ()#line:179
        else :#line:180
            logging .info ('Starting ban users.')#line:181
            O00O0000OOOO0O0OO =''#line:182
            OOO0O00O0OO000O00 =None #line:183
            if OOOOOOO0000000OO0 .current_window ==3 :#line:184
                O00O0000OOOO0O0OO ='r'#line:185
                OOO0O00O0OO000O00 =OOOOOOO0000000OO0 .ui .Reward .text ()#line:186
                O0OO0OO0000000OOO =OOOOOOO0000000OO0 .ui .RepostsCount .text ()#line:187
            else :#line:188
                O00O0000OOOO0O0OO ='l'#line:189
                O0OO0OO0000000OOO =OOOOOOO0000000OO0 .ui .LikesCount .text ()#line:190
            if OOOOOOO0000000OO0 .ui .LikestCheckBox .isChecked ()or OOOOOOO0000000OO0 .ui .RepostsCheckBox .isChecked ():#line:192
                O0OO0O00000O00OOO =f'https://vk.com/wall{OOOOOOO0000000OO0.user.user_id}_{OOOOOOO0000000OO0.user.item_id}'#line:193
                save_data_to_file (url_tolike =O0OO0O00000O00OOO ,post_id =OOOOOOO0000000OO0 .user .item_id )#line:195
                OOOOOOO0000000OO0 .user .add_likest_task (likes_count =O0OO0OO0000000OOO ,like_url =O0OO0O00000O00OOO ,repost_like =O00O0000OOOO0O0OO ,reward =OOO0O00O0OO000O00 )#line:197
                if OOOOOOO0000000OO0 .current_window ==3 :#line:199
                    OOOOOOO0000000OO0 .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:200
                    OOOOOOO0000000OO0 .ui .ResultSaveUrl_R .setText ("Task added")#line:201
                else :#line:202
                    OOOOOOO0000000OO0 .ui .ResultSaveUrl .setText ("Task added!")#line:203
            else :#line:204
                logging .info ('Not log likest')#line:205
                if OOOOOOO0000000OO0 .current_window ==3 :#line:206
                    OOOOOOO0000000OO0 .ui .ResultSaveUrl_R .setText ("You must add a task.")#line:207
                else :#line:208
                    OOOOOOO0000000OO0 .ui .ResultSaveUrl .setText ("You must add a task.")#line:209
            OOOOOOO0000000OO0 .m_thread =QtCore .QThread (OOOOOOO0000000OO0 )#line:211
            OOOOOOO0000000OO0 .m_modbus_worker =ModbusWorker (OOOOOOO0000000OO0 .user )#line:212
            OOOOOOO0000000OO0 .m_modbus_worker .moveToThread (OOOOOOO0000000OO0 .m_thread )#line:213
            OOOOOOO0000000OO0 .m_thread .start ()#line:214
            QtCore .QTimer .singleShot (0 ,OOOOOOO0000000OO0 .m_modbus_worker .do_work )#line:215
            if OOOOOOO0000000OO0 .current_window ==3 :#line:217
                OOOOOOO0000000OO0 .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:218
                OOOOOOO0000000OO0 .ui .ResultStartLikes_R .setText ("  Started!")#line:219
            else :#line:220
                OOOOOOO0000000OO0 .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:221
                OOOOOOO0000000OO0 .ui .ResultStartLikes .setText ("  Started!")#line:222
    @QtCore .pyqtSlot ()#line:224
    def stop (OO0O00OOOOOOOO00O ):#line:225
        if OO0O00OOOOOOOO00O .m_modbus_worker :#line:226
            OO0O00OOOOOOOO00O .m_modbus_worker .stop ()#line:227
            OO0O00OOOOOOOO00O .m_modbus_worker .terminate ()#line:228
        if OO0O00OOOOOOOO00O .m_thread :#line:229
            OO0O00OOOOOOOO00O .m_thread .requestInterruption ()#line:230
            OO0O00OOOOOOOO00O .ui .ResultStartLikes .setStyleSheet ("color: rgb(195, 15, 18);")#line:231
            OO0O00OOOOOOOO00O .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:232
            OO0O00OOOOOOOO00O .ui .ResultStartLikes .setText (" Wait!")#line:233
            OO0O00OOOOOOOO00O .ui .ResultStartLikes_R .setText (" Wait!")#line:234
            OO0O00OOOOOOOO00O .user .delete_repost ()#line:235
            OO0O00OOOOOOOO00O .user .unban_users ()#line:236
            OO0O00OOOOOOOO00O .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:237
            OO0O00OOOOOOOO00O .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:238
            OO0O00OOOOOOOO00O .ui .ResultStartLikes .setText (" Stopped")#line:239
            OO0O00OOOOOOOO00O .ui .ResultStartLikes_R .setText (" Stopped")#line:240
            OO0O00OOOOOOOO00O .m_thread .quit ()#line:241
            OO0O00OOOOOOOO00O .m_thread .wait ()#line:242
            sys .exit (OO0O00OOOOOOOO00O .m_thread .exec ())#line:243
    def save_url (O00OOO000OOOOOO00 ):#line:245
        if not O00OOO000OOOOOO00 .user :#line:246
            O00OOO000OOOOOO00 .err_dialog .set_text ("You must log in")#line:247
            O00OOO000OOOOOO00 .err_dialog .exec_ ()#line:248
        else :#line:249
            if O00OOO000OOOOOO00 .current_window ==3 :#line:250
                O00000OOOO0O0O0O0 =O00OOO000OOOOOO00 .ui .LabelRepostsUrl .text ()#line:251
            else :#line:252
                O00000OOOO0O0O0O0 =O00OOO000OOOOOO00 .ui .LabelLikesUrl .text ()#line:253
            if O00000OOOO0O0O0O0 is None :#line:255
                O00000OOOO0O0O0O0 =O00OOO000OOOOOO00 .ui .LabelRepostsUrl .text ()#line:256
            O00OOO000OOOOOO00 .data_result =O00OOO000OOOOOO00 .user .get_data_from_link (O00000OOOO0O0O0O0 )#line:258
            OO0OOO00OO0OO0000 ={}#line:259
            if not O00000OOOO0O0O0O0 :#line:261
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:262
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setText ("Enter Url")#line:263
                if O00OOO000OOOOOO00 .current_window ==3 :#line:264
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:265
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setText ("Enter Url")#line:266
            elif not O00OOO000OOOOOO00 .data_result :#line:267
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:268
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setText ("Invalid url.")#line:269
                if O00OOO000OOOOOO00 .current_window ==3 :#line:270
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:271
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setText ("Invalid url.")#line:272
            else :#line:273
                OO0OOO00OO0OO0000 =save_data_to_file (url_tolike =O00000OOOO0O0O0O0 ,post_id =O00OOO000OOOOOO00 .data_result [1 ])#line:275
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setStyleSheet ("color: rgb(154, 255, 152);")#line:276
                O00OOO000OOOOOO00 .ui .ResultSaveUrl .setText ("Saved")#line:277
                if O00OOO000OOOOOO00 .current_window ==3 :#line:278
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:279
                    O00OOO000OOOOOO00 .ui .ResultSaveUrl_R .setText ("Saved")#line:280
                logging .info (O00OOO000OOOOOO00 .data_result )#line:281
            O00OOO000OOOOOO00 .ui .LabelLikesUrl .clear ()#line:283
            O00OOO000OOOOOO00 .ui .LabelRepostsUrl .clear ()#line:284
            if ('login'and 'password'and 'url')in OO0OOO00OO0OO0000 :#line:285
                logging .info (OO0OOO00OO0OO0000 )#line:286
    def set_page_view_likes (O00OOOOOOOOO0O000 ):#line:288
        O00OOOOOOOOO0O000 .current_window =2 #line:289
        O00OOOOOOOOO0O000 .ui .stackedWidget .setCurrentIndex (2 )#line:290
    def set_page_view_repost (O0OOO000O00OOO00O ):#line:292
        O0OOO000O00OOO00O .current_window =3 #line:293
        O0OOO000O00OOO00O .ui .stackedWidget .setCurrentIndex (3 )#line:294
    def set_page_view_logs (OO0000O0O0O00O000 ):#line:296
        OO0000O0O0O00O000 .current_window =1 #line:297
        OO0000O0O0O00O000 .ui .stackedWidget .setCurrentIndex (1 )#line:298
    def set_page_view_vklogin (OOO0O0OOOO00000O0 ):#line:300
        OOO0O0OOOO00000O0 .current_window =0 #line:301
        OOO0O0OOOO00000O0 .ui .stackedWidget .setCurrentIndex (0 )#line:302
    def vk_login (OO00OO00000OO0O00 ):#line:304
        OO00OOOO0OOO0O00O =OO00OO00000OO0O00 .ui .lineEdit .text ()#line:305
        O0OOOO0O0O000OOO0 =OO00OO00000OO0O00 .ui .lineEdit_2 .text ()#line:306
        if not (OO00OOOO0OOO0O00O and O0OOOO0O0O000OOO0 ):#line:307
            OO00OO00000OO0O00 .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:308
            OO00OO00000OO0O00 .ui .ResultOfLogin .setText ("Empty data")#line:309
        else :#line:310
            OO00OO00000OO0O00 .user =User (OO00OOOO0OOO0O00O ,O0OOOO0O0O000OOO0 )#line:311
            OO0000OO0OOOOOO0O =OO00OO00000OO0O00 .user .login ()#line:312
            if not OO0000OO0OOOOOO0O :#line:314
                OO00OO00000OO0O00 .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:315
                OO00OO00000OO0O00 .ui .ResultOfLogin .setText ("Unsuccessful login.\nInvalid email of password.")#line:316
            else :#line:317
                OO00OO00000OO0O00 .token =OO00OO00000OO0O00 .user .get_token ()#line:318
                OO00OO00000OO0O00 .data =save_data_to_file (login =OO00OOOO0OOO0O00O ,password =O0OOOO0O0O000OOO0 ,token =OO00OO00000OO0O00 .user .token ,user_id =OO00OO00000OO0O00 .user .user_id )#line:324
                OO00OO00000OO0O00 .check_login_result (OO00OO00000OO0O00 .data )#line:325
    def check_login_result (O0OOOOOOOOO0O00OO ,OOO00O0OO0O0O0OOO ):#line:327
        if not O0OOOOOOOOO0O00OO .data or not O0OOOOOOOOO0O00OO .data ['token']:#line:328
            O0OOOOOOOOO0O00OO .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:329
            O0OOOOOOOOO0O00OO .ui .ResultOfLogin .setText ("Unsuccessful login")#line:330
        elif O0OOOOOOOOO0O00OO .data ['token']:#line:331
            O0OOOOOOOOO0O00OO .user .login_likest ()#line:332
            O0OOOOOOOOO0O00OO .ui .ResultOfLogin .setStyleSheet ("color: rgb(154, 255, 152);")#line:333
            O0OOOOOOOOO0O00OO .ui .ResultOfLogin .setText ("Successful login\nData saved to data.txt")#line:334
class ModbusWorker (QThread ):#line:337
    def __init__ (O000O0O0OOOOO0OO0 ,OO0O000O0OO0OO0OO ):#line:338
        super ().__init__ ()#line:339
        O000O0O0OOOOO0OO0 .user =OO0O000O0OO0OO0OO #line:340
        O000O0O0OOOOO0OO0 .threadactive =True #line:341
    @QtCore .pyqtSlot ()#line:343
    def do_work (O0OO0O0OOOO0OO0OO ):#line:344
        while not QtCore .QThread .currentThread ().isInterruptionRequested ()or O0OO0O0OOOO0OO0OO .threadactive :#line:345
            O0OO0O0OOOO0OO0OO .user .ban_user_report ()#line:347
    def stop (O0O0000O0OOOO000O ):#line:349
        O0O0000O0OOOO000O .threadactive =False #line:350
        O0O0000O0OOOO000O .wait ()#line:351
def check_hwid ():#line:354
    OOO0000O000O0OOOO =requests .get ("https://pastebin.com/raw/vNkGmGNi")#line:355
    OOOOO0000O0OO0000 =str (subprocess .check_output ('wmic csproduct get uuid')).split ('\\r\\n')[1 ].strip ('\\r').strip ()#line:356
    if OOOOO0000O0OO0000 in OOO0000O000O0OOOO .text :#line:357
        return True #line:358
    else :#line:359
        return False #line:360
if __name__ =='__main__':#line:363
    try :#line:364
        if check_hwid ():#line:365
            app =QtWidgets .QApplication ([])#line:366
            app .setStyle ('Windows')#line:367
            application =MyyWindow ()#line:369
            application .show ()#line:370
            sys .exit (app .exec ())#line:371
        else :#line:372
            app =QtWidgets .QApplication ([])#line:373
            error_dialog =ErrorDialog ()#line:374
            error_dialog .set_text ('You are not Subscribed!')#line:375
            error_dialog .show ()#line:376
            app .exec_ ()#line:377
    except Exception as e :#line:378
        raise e #line:379
'''
beta.alfaliker.com /бан ссылки 10-15 мин
turboliker.ru
likes.fm
snebes.ru
freelikes.online net
'''#line:387
