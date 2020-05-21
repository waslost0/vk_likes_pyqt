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
from random import choice #line:12
import requests #line:13
from string import Template #line:14
from PyQt5 import QtCore ,QtGui ,QtWidgets #line:15
from PyQt5 .QtCore import QThread #line:16
from PyQt5 .QtWidgets import QMessageBox #line:17
from ui_py .test_ui import Ui_MainWindow #line:19
from logic import load_data_from_file ,User ,save_data_to_file #line:20
from ui_py .error_ui import Ui_Error #line:21
from ui_py .hwid import Ui_Hwid #line:22
from bs4 import BeautifulSoup as BS #line:23
from PyQt5 .QtCore import (QCoreApplication ,QObject ,QRunnable ,QThread ,QThreadPool ,pyqtSignal )#line:25
def resource_path (OOO0O00OOOO00O00O ):#line:28
    ""#line:29
    """ Get absolute path to resource, works for dev and for PyInstaller """#line:30
    O000O000O0O0OOO0O =getattr (sys ,'_MEIPASS',os .path .dirname (os .path .abspath (__file__ )))#line:31
    return os .path .join (O000O000O0O0OOO0O ,OOO0O00OOOO00O00O )#line:32
class QTextEditLogger (logging .Handler ):#line:35
    def __init__ (O000OO0O0000OO0O0 ,OOOO0OO00OOO0OOOO ):#line:36
        super ().__init__ ()#line:37
        O000OO0O0000OO0O0 .widget =QtWidgets .QPlainTextEdit (OOOO0OO00OOO0OOOO )#line:38
        O000OO0O0000OO0O0 .widget .setReadOnly (True )#line:39
        O000OO0O0000OO0O0 .widget .setFixedSize (680 ,420 )#line:40
    def emit (OO00O00O0O0O00OO0 ,OOOO00OO0OO0O00OO ):#line:42
        O000OO0O000OO00O0 =OO00O00O0O0O00OO0 .format (OOOO00OO0OO0O00OO )#line:43
        OO00O00O0O0O00OO0 .widget .appendPlainText (O000OO0O000OO00O0 )#line:44
class ErrorDialog (QtWidgets .QDialog ):#line:47
    def __init__ (O0OOOO0OO0OOOO0OO ,parent =None ):#line:48
        super (ErrorDialog ,O0OOOO0OO0OOOO0OO ).__init__ (parent )#line:49
        O0OOOO0OO0OOOO0OO .ui =Ui_Error ()#line:50
        O0OOOO0OO0OOOO0OO .ui .setupUi (O0OOOO0OO0OOOO0OO )#line:51
    def set_text (OO0000O00O00O000O ,OO00000O0000O00OO ):#line:53
        OO0000O00O00O000O .ui .label .setText (OO00000O0000O00OO )#line:54
class HwidDialog (QtWidgets .QDialog ):#line:57
    def __init__ (OO00O00O00OO00000 ,parent =None ):#line:58
        super (HwidDialog ,OO00O00O00OO00000 ).__init__ (parent )#line:59
        OO00O00O00OO00000 .ui =Ui_Hwid ()#line:60
        OO00O00O00OO00000 .ui .setupUi (OO00O00O00OO00000 )#line:61
    def set_text (O00OO0OOO000O00O0 ,O00OO0O0O0O0OOOOO ):#line:63
        O00OO0OOO000O00O0 .ui .label_2 .setText (O00OO0O0O0O0OOOOO )#line:64
    def set_hwid (O0OOOO0O0OOOOO0OO ,OO0O0OOO0O000000O ):#line:66
        O0OOOO0O0OOOOO0OO .ui .lineEdit .setText (OO0O0OOO0O000000O )#line:67
class MyyWindow (QtWidgets .QMainWindow ):#line:70
    def __init__ (OOOOO000OOOO0OOOO ):#line:71
        super (MyyWindow ,OOOOO000OOOO0OOOO ).__init__ ()#line:72
        OOOOO000OOOO0OOOO .m_thread =None #line:73
        OOOOO000OOOO0OOOO .current_window =None #line:74
        OOOOO000OOOO0OOOO .ui =Ui_MainWindow ()#line:75
        OOOOO000OOOO0OOOO .ui .setupUi (OOOOO000OOOO0OOOO )#line:76
        OOOOO000OOOO0OOOO .ui .stackedWidget .setCurrentIndex (0 )#line:77
        OOOOO000OOOO0OOOO .err_dialog =ErrorDialog ()#line:80
        OOOOO000OOOO0OOOO .data_result =None #line:81
        OOOOO000OOOO0OOOO .m_modbus_worker =None #line:82
        OOOOO000OOOO0OOOO .ui .LikesButton .clicked .connect (OOOOO000OOOO0OOOO .set_page_view_likes )#line:84
        OOOOO000OOOO0OOOO .ui .LogsButton .clicked .connect (OOOOO000OOOO0OOOO .set_page_view_logs )#line:85
        OOOOO000OOOO0OOOO .ui .VkLoginButton .clicked .connect (OOOOO000OOOO0OOOO .set_page_view_vklogin )#line:86
        OOOOO000OOOO0OOOO .ui .vkImage .setPixmap (QtGui .QPixmap (resource_path ('vk.png')))#line:87
        OOOOO000OOOO0OOOO .ui .pushButton_4 .clicked .connect (OOOOO000OOOO0OOOO .vk_login )#line:89
        OOOOO000OOOO0OOOO .ui .SaveUrlButton .clicked .connect (OOOOO000OOOO0OOOO .save_url )#line:90
        OOOOO000OOOO0OOOO .ui .SaveUrlButton_R .clicked .connect (OOOOO000OOOO0OOOO .save_url )#line:91
        OOOOO000OOOO0OOOO .ui .SaveCouponButton .clicked .connect (OOOOO000OOOO0OOOO .save_coupon )#line:94
        OOOOO000OOOO0OOOO .ui .getBalance .clicked .connect (OOOOO000OOOO0OOOO .get_likest_balance )#line:96
        OOOOO000OOOO0OOOO .ui .ReposButton .clicked .connect (OOOOO000OOOO0OOOO .set_page_view_repost )#line:97
        O000OO00O0000OOOO =QTextEditLogger (OOOOO000OOOO0OOOO .ui .plainTextEdit )#line:99
        O000OO00O0000OOOO .setFormatter (logging .Formatter ('%(filename)s[LINE:%(lineno)-4s]' ' #%(levelname)-4s [%(asctime)s]  %(message)s'))#line:103
        logging .getLogger ("getmac").setLevel (logging .WARNING )#line:104
        logging .getLogger ().addHandler (O000OO00O0000OOOO )#line:106
        OOOOO000OOOO0OOOO .data =None #line:108
        OOOOO000OOOO0OOOO .user =None #line:109
        OOOOO000OOOO0OOOO .user_id =None #line:110
        OOOOO000OOOO0OOOO .post_id =None #line:111
        OOOOO000OOOO0OOOO .token =None #line:112
        OOOOO000OOOO0OOOO .ui .StopLikes .clicked .connect (OOOOO000OOOO0OOOO .stop )#line:116
        OOOOO000OOOO0OOOO .ui .StartLikes .clicked .connect (OOOOO000OOOO0OOOO .start )#line:117
        OOOOO000OOOO0OOOO .ui .StopLikes_R .clicked .connect (OOOOO000OOOO0OOOO .stop )#line:119
        OOOOO000OOOO0OOOO .ui .StartLikes_R .clicked .connect (OOOOO000OOOO0OOOO .start )#line:120
        OOOOO000OOOO0OOOO .is_login_likest =False #line:121
        try :#line:123
            logging .info ('Trying to load all data from file')#line:124
            OOOOO000OOOO0OOOO .data =load_data_from_file ()#line:125
        except Exception as OOOOOO00O00OO0000 :#line:127
            logging .error (OOOOOO00O00OO0000 )#line:128
        if 'login'in OOOOO000OOOO0OOOO .data and 'password'in OOOOO000OOOO0OOOO .data and 'token'in OOOOO000OOOO0OOOO .data :#line:130
            OOOOO000OOOO0OOOO .token =OOOOO000OOOO0OOOO .data ['token']#line:131
            OOOOO000OOOO0OOOO .user =User (username =OOOOO000OOOO0OOOO .data ['login'],password =OOOOO000OOOO0OOOO .data ['password'])#line:135
            OOOOO000OOOO0OOOO .login_result =OOOOO000OOOO0OOOO .user .login ()#line:137
            OOOOO000OOOO0OOOO .ui .ResultOfLogin .setText (f"Welcome back {OOOOO000OOOO0OOOO.login_result}")#line:138
            try :#line:139
                OOOOO000OOOO0OOOO .is_login_likest =OOOOO000OOOO0OOOO .user .login_likest ()#line:140
            except Exception as OOOOOO00O00OO0000 :#line:142
                logging .error (OOOOOO00O00OO0000 )#line:143
        elif ('token'not in OOOOO000OOOO0OOOO .data )and ('login'in OOOOO000OOOO0OOOO .data ):#line:145
            OOOOO000OOOO0OOOO .user =User (username =OOOOO000OOOO0OOOO .data ['login'],password =OOOOO000OOOO0OOOO .data ['password'])#line:146
            OOOOO000OOOO0OOOO .user .login ()#line:147
            OOOOO000OOOO0OOOO .token =OOOOO000OOOO0OOOO .user .get_token ()#line:148
            OO0OO000OO0OO0O0O =Template ("Ur token $token")#line:149
            logging .info (OO0OO000OO0OO0O0O .substitute (OOOOO000OOOO0OOOO .token ))#line:150
            OOOOO000OOOO0OOOO .data_saved =save_data_to_file (login =OOOOO000OOOO0OOOO .data ['login'],password =OOOOO000OOOO0OOOO .data ['password'],token =OOOOO000OOOO0OOOO .token )#line:156
            try :#line:157
                OOOOO000OOOO0OOOO .is_login_likest =OOOOO000OOOO0OOOO .user .login_likest ()#line:158
            except Exception as OOOOOO00O00OO0000 :#line:159
                logging .error (OOOOOO00O00OO0000 )#line:160
            logging .info (f"Saved data {OOOOO000OOOO0OOOO.data_saved}")#line:161
        if 'user_id'in OOOOO000OOOO0OOOO .data :#line:162
            OOOOO000OOOO0OOOO .user .user_id =OOOOO000OOOO0OOOO .data ['user_id']#line:163
    def save_coupon (OO0O000OO0OO00000 ):#line:165
        if not OO0O000OO0OO00000 .user :#line:166
            OO0O000OO0OO00000 .err_dialog .set_text ("You must log in")#line:167
            OO0O000OO0OO00000 .err_dialog .exec_ ()#line:168
        else :#line:169
            O00O000OOO0O0O000 =OO0O000OO0OO00000 .ui .LabelCoupon .text ()#line:170
            OOOOOOOOO00OO00OO =OO0O000OO0OO00000 .user .activate_coupon (O00O000OOO0O0O000 )#line:171
            if 'SUCCESS'in OOOOOOOOO00OO00OO ['status']:#line:173
                OO0O000OO0OO00000 .ui .ResultCoupon .setStyleSheet ("color: rgb(154, 255, 152);")#line:174
                OO0O000OO0OO00000 .ui .ResultCoupon .setText ('Activated')#line:175
            else :#line:176
                OO0O000OO0OO00000 .ui .ResultCoupon .setStyleSheet ("color: rgb(195, 15, 18);")#line:177
                OO0O000OO0OO00000 .ui .ResultCoupon .setText ('Not activated')#line:178
    def get_likest_balance (OO0OOOOO00000OO0O ):#line:180
        if not OO0OOOOO00000OO0O .user :#line:181
            OO0OOOOO00000OO0O .err_dialog .set_text ("You must log in")#line:182
            OO0OOOOO00000OO0O .err_dialog .exec_ ()#line:183
        else :#line:184
            OO0OOOOO00000OO0O .likes_balance =OO0OOOOO00000OO0O .user .get_likes_balance ()#line:185
            if 'balance'in OO0OOOOO00000OO0O .likes_balance :#line:186
                O0O0OOO0O0OOO00O0 =OO0OOOOO00000OO0O .likes_balance ['balance']#line:187
                OO0OOOOO00000OO0O .ui .LikesBalanceLabel .setText (str (O0O0OOO0O0OOO00O0 ))#line:188
    def on_succ_login (OO0OO00OO00OO0O0O ):#line:190
        if OO0OO00OO00OO0O0O .login_result :#line:191
            logging .info ('Data loaded. Token loaded. User session created.')#line:192
            OO0OO00OO00OO0O0O .ui .stackedWidget .setCurrentIndex (2 )#line:193
        if 'user_id'not in OO0OO00OO00OO0O0O .data :#line:196
            OO0OO00OO00OO0O0O .user_id =OO0OO00OO00OO0O0O .user .get_user_id ()#line:197
            OO0OO00OO00OO0O0O .data_saved =save_data_to_file (user_id =OO0OO00OO00OO0O0O .user_id )#line:198
    @QtCore .pyqtSlot ()#line:200
    def start (O000OO0OO0OOO00O0 ):#line:201
        if not O000OO0OO0OOO00O0 .user or not O000OO0OO0OOO00O0 .data_result :#line:202
            if not O000OO0OO0OOO00O0 .data_result :#line:203
                O000OO0OO0OOO00O0 .err_dialog .set_text ("You must add url")#line:204
            else :#line:205
                O000OO0OO0OOO00O0 .err_dialog .set_text ("You must log in")#line:206
            O000OO0OO0OOO00O0 .err_dialog .exec_ ()#line:207
        else :#line:208
            logging .info ('Starting ban users.')#line:209
            OO00OO00OOOOO0O0O =''#line:210
            O0000O0OOOOO0OO0O =None #line:211
            if O000OO0OO0OOO00O0 .current_window ==3 :#line:212
                OO00OO00OOOOO0O0O ='r'#line:213
                O0000O0OOOOO0OO0O =O000OO0OO0OOO00O0 .ui .Reward .text ()#line:214
                O00OOO0O00OO0O0OO =O000OO0OO0OOO00O0 .ui .RepostsCount .text ()#line:215
            else :#line:216
                OO00OO00OOOOO0O0O ='l'#line:217
                O00OOO0O00OO0O0OO =O000OO0OO0OOO00O0 .ui .LikesCount .text ()#line:218
            if (O000OO0OO0OOO00O0 .ui .LikestCheckBox .isChecked ()or O000OO0OO0OOO00O0 .ui .RepostsCheckBox .isChecked ())and O000OO0OO0OOO00O0 .is_login_likest :#line:220
                O0OO000OO00OO0000 =f'https://vk.com/wall{O000OO0OO0OOO00O0.user.user_id}_{O000OO0OO0OOO00O0.user.item_id}'#line:221
                save_data_to_file (url_tolike =O0OO000OO00OO0000 ,post_id =O000OO0OO0OOO00O0 .user .item_id )#line:223
                O000OO0OO0OOO00O0 .user .add_likest_task (likes_count =O00OOO0O00OO0O0OO ,like_url =O0OO000OO00OO0000 ,repost_like =OO00OO00OOOOO0O0O ,reward =O0000O0OOOOO0OO0O )#line:225
                if O000OO0OO0OOO00O0 .current_window ==3 :#line:227
                    O000OO0OO0OOO00O0 .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:228
                    O000OO0OO0OOO00O0 .ui .ResultSaveUrl_R .setText ("Task added")#line:229
                else :#line:230
                    O000OO0OO0OOO00O0 .ui .ResultSaveUrl .setText ("Task added!")#line:231
            else :#line:232
                logging .info ('Not log likest')#line:233
                if O000OO0OO0OOO00O0 .is_login_likest is False :#line:234
                    O000OO0OO0OOO00O0 .err_dialog .set_text ("You can`t add task. Because you are not logged likes.")#line:235
                    O000OO0OO0OOO00O0 .err_dialog .show ()#line:236
                if O000OO0OO0OOO00O0 .current_window ==3 :#line:237
                    O000OO0OO0OOO00O0 .ui .ResultSaveUrl_R .setText ("You must add a task.")#line:238
                else :#line:239
                    O000OO0OO0OOO00O0 .ui .ResultSaveUrl .setText ("You must add a task.")#line:240
            O000OO0OO0OOO00O0 .m_thread =QtCore .QThread (O000OO0OO0OOO00O0 )#line:242
            O000OO0OO0OOO00O0 .m_modbus_worker =ModbusWorker (O000OO0OO0OOO00O0 .user )#line:243
            O000OO0OO0OOO00O0 .m_modbus_worker .moveToThread (O000OO0OO0OOO00O0 .m_thread )#line:244
            O000OO0OO0OOO00O0 .m_thread .start ()#line:245
            QtCore .QTimer .singleShot (0 ,O000OO0OO0OOO00O0 .m_modbus_worker .do_work )#line:246
            if O000OO0OO0OOO00O0 .current_window ==3 :#line:248
                O000OO0OO0OOO00O0 .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:249
                O000OO0OO0OOO00O0 .ui .ResultStartLikes_R .setText ("  Started!")#line:250
            else :#line:251
                O000OO0OO0OOO00O0 .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:252
                O000OO0OO0OOO00O0 .ui .ResultStartLikes .setText ("  Started!")#line:253
    @QtCore .pyqtSlot ()#line:255
    def stop (O00000O00OOO00OOO ):#line:256
        OO00O000O0OOO0OOO =Runnable (O00000O00OOO00OOO .user )#line:257
        QThreadPool .globalInstance ().start (OO00O000O0OOO0OOO )#line:258
        if O00000O00OOO00OOO .m_modbus_worker :#line:259
            O00000O00OOO00OOO .m_modbus_worker .stop ()#line:260
            O00000O00OOO00OOO .m_modbus_worker .terminate ()#line:261
        if O00000O00OOO00OOO .m_thread :#line:262
            O00000O00OOO00OOO .m_thread .requestInterruption ()#line:263
            O00000O00OOO00OOO .ui .ResultStartLikes .setStyleSheet ("color: rgb(195, 15, 18);")#line:264
            O00000O00OOO00OOO .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:265
            O00000O00OOO00OOO .ui .ResultStartLikes .setText (" Wait!")#line:266
            O00000O00OOO00OOO .ui .ResultStartLikes_R .setText (" Wait!")#line:267
            O00000O00OOO00OOO .user .delete_repost ()#line:268
            O00000O00OOO00OOO .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:269
            O00000O00OOO00OOO .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:270
            O00000O00OOO00OOO .ui .ResultStartLikes .setText (" Stopped")#line:271
            O00000O00OOO00OOO .ui .ResultStartLikes_R .setText (" Stopped")#line:272
            O00000O00OOO00OOO .m_thread .quit ()#line:273
            O00000O00OOO00OOO .m_thread .wait ()#line:274
            sys .exit (O00000O00OOO00OOO .m_thread .exec ())#line:275
    def save_url (OO00000O0O0OO0O0O ):#line:277
        if not OO00000O0O0OO0O0O .user :#line:278
            OO00000O0O0OO0O0O .err_dialog .set_text ("You must log in")#line:279
            OO00000O0O0OO0O0O .err_dialog .exec_ ()#line:280
        else :#line:281
            if OO00000O0O0OO0O0O .current_window ==3 :#line:282
                O00O00O0OOO0OO0OO =OO00000O0O0OO0O0O .ui .LabelRepostsUrl .text ()#line:283
            else :#line:284
                O00O00O0OOO0OO0OO =OO00000O0O0OO0O0O .ui .LabelLikesUrl .text ()#line:285
            if O00O00O0OOO0OO0OO is None :#line:287
                O00O00O0OOO0OO0OO =OO00000O0O0OO0O0O .ui .LabelRepostsUrl .text ()#line:288
            OO00000O0O0OO0O0O .data_result =OO00000O0O0OO0O0O .user .get_data_from_link (O00O00O0OOO0OO0OO )#line:290
            OO000OOOO0OOO00OO ={}#line:291
            if not O00O00O0OOO0OO0OO :#line:293
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:294
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setText ("Enter Url")#line:295
                if OO00000O0O0OO0O0O .current_window ==3 :#line:296
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:297
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setText ("Enter Url")#line:298
            elif not OO00000O0O0OO0O0O .data_result :#line:299
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:300
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setText ("Invalid url.")#line:301
                if OO00000O0O0OO0O0O .current_window ==3 :#line:302
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:303
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setText ("Invalid url.")#line:304
            else :#line:305
                OO000OOOO0OOO00OO =save_data_to_file (url_tolike =O00O00O0OOO0OO0OO ,post_id =OO00000O0O0OO0O0O .data_result [1 ])#line:307
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(154, 255, 152);")#line:308
                OO00000O0O0OO0O0O .ui .ResultSaveUrl .setText ("Saved")#line:309
                if OO00000O0O0OO0O0O .current_window ==3 :#line:310
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:311
                    OO00000O0O0OO0O0O .ui .ResultSaveUrl_R .setText ("Saved")#line:312
                logging .info (OO00000O0O0OO0O0O .data_result )#line:313
            OO00000O0O0OO0O0O .ui .LabelLikesUrl .clear ()#line:315
            OO00000O0O0OO0O0O .ui .LabelRepostsUrl .clear ()#line:316
            if ('login'and 'password'and 'url')in OO000OOOO0OOO00OO :#line:317
                logging .info (OO000OOOO0OOO00OO )#line:318
    def set_page_view_likes (OO00OO000O0OO0O0O ):#line:320
        OO00OO000O0OO0O0O .current_window =2 #line:321
        OO00OO000O0OO0O0O .ui .stackedWidget .setCurrentIndex (2 )#line:322
    def set_page_view_repost (O0000O000OO0O0O0O ):#line:324
        O0000O000OO0O0O0O .current_window =3 #line:325
        O0000O000OO0O0O0O .ui .stackedWidget .setCurrentIndex (3 )#line:326
    def set_page_view_logs (OO0O00OOO00OOO00O ):#line:328
        OO0O00OOO00OOO00O .current_window =1 #line:329
        OO0O00OOO00OOO00O .ui .stackedWidget .setCurrentIndex (1 )#line:330
    def set_page_view_vklogin (OOOO00OOO0O0OOOOO ):#line:332
        OOOO00OOO0O0OOOOO .current_window =0 #line:333
        OOOO00OOO0O0OOOOO .ui .stackedWidget .setCurrentIndex (0 )#line:334
    def vk_login (O000OO0O0O0O00OOO ):#line:336
        OO00OO0O0O000O0O0 =O000OO0O0O0O00OOO .ui .lineEdit .text ()#line:337
        O0O0O00O0O00OO0O0 =O000OO0O0O0O00OOO .ui .lineEdit_2 .text ()#line:338
        if not (OO00OO0O0O000O0O0 and O0O0O00O0O00OO0O0 ):#line:339
            O000OO0O0O0O00OOO .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:340
            O000OO0O0O0O00OOO .ui .ResultOfLogin .setText ("Empty data")#line:341
        else :#line:342
            O000OO0O0O0O00OOO .user =User (OO00OO0O0O000O0O0 ,O0O0O00O0O00OO0O0 )#line:343
            OOOOO0OO00OO0O0O0 =O000OO0O0O0O00OOO .user .login ()#line:344
            if not OOOOO0OO00OO0O0O0 :#line:346
                O000OO0O0O0O00OOO .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:347
                O000OO0O0O0O00OOO .ui .ResultOfLogin .setText ("Unsuccessful login.\nInvalid email of password.")#line:348
            else :#line:349
                O000OO0O0O0O00OOO .token =O000OO0O0O0O00OOO .user .get_token ()#line:350
                O000OO0O0O0O00OOO .data =save_data_to_file (login =OO00OO0O0O000O0O0 ,password =O0O0O00O0O00OO0O0 ,token =O000OO0O0O0O00OOO .user .token ,user_id =O000OO0O0O0O00OOO .user .user_id )#line:356
                O000OO0O0O0O00OOO .check_login_result ()#line:357
    def check_login_result (O000O0OOOOO0O000O ):#line:359
        if not O000O0OOOOO0O000O .data or not O000O0OOOOO0O000O .data ['token']:#line:360
            O000O0OOOOO0O000O .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:361
            O000O0OOOOO0O000O .ui .ResultOfLogin .setText ("Unsuccessful login")#line:362
        elif O000O0OOOOO0O000O .data ['token']:#line:363
            if O000O0OOOOO0O000O .ui .checkBox .isChecked ():#line:364
                O000O0OOOOO0O000O .user .login_likest ()#line:365
            O000O0OOOOO0O000O .ui .ResultOfLogin .setStyleSheet ("color: rgb(154, 255, 152);")#line:366
            O000O0OOOOO0O000O .ui .ResultOfLogin .setText ("Successful login\nData saved to data.txt")#line:367
class Runnable (QRunnable ):#line:370
    def __init__ (OOOOO0OOOO0O0OOOO ,O00OO0OO00OO000O0 ):#line:371
        super ().__init__ ()#line:372
        OOOOO0OOOO0O0OOOO .user =O00OO0OO00OO000O0 #line:373
    def run (OOO0O0OOO0000O000 ):#line:375
        try :#line:376
            logging .info ('Unbaning users')#line:377
            OOO0O0OOO0000O000 .user .unban_users ()#line:378
        except Exception as O00OO00O000O000OO :#line:379
            logging .error (O00OO00O000O000OO )#line:380
class ModbusWorker (QThread ):#line:383
    def __init__ (O0OO00OO00OO00O0O ,O00000OOOO0OO00O0 ):#line:384
        super ().__init__ ()#line:385
        O0OO00OO00OO00O0O .user =O00000OOOO0OO00O0 #line:386
    @QtCore .pyqtSlot ()#line:388
    def do_work (OOO0000OOO00OO00O ):#line:389
        try :#line:390
            while not QtCore .QThread .currentThread ().isInterruptionRequested ():#line:391
                OOO0000OOO00OO00O .user .ban_user_report ()#line:393
        except Exception as O0OOO0O000OO00O00 :#line:394
            logging .log (O0OOO0O000OO00O00 )#line:395
            OOO0000OOO00OO00O .user .delete_repost ()#line:396
    def stop (O0O00O0O00OO00O0O ):#line:398
        O0O00O0O00OO00O0O .wait ()#line:400
def get_hwid ():#line:403
    return str (subprocess .check_output ('wmic csproduct get uuid')).split ('\\r\\n')[1 ].strip ('\\r').strip ()#line:404
def check_hwid ():#line:407
    OO0OO0OO000OOO000 =requests .get ("https://pastebin.com/raw/GFQrRHcS")#line:408
    O0O00O0OO0O0000O0 =str (subprocess .check_output ('wmic csproduct get uuid')).split ('\\r\\n')[1 ].strip ('\\r').strip ()#line:409
    if O0O00O0OO0O0000O0 in OO0OO0OO000OOO000 .text :#line:410
        return True #line:411
    else :#line:412
        return False #line:413
if __name__ =='__main__':#line:416
    try :#line:417
        if check_hwid ():#line:418
            app =QtWidgets .QApplication ([])#line:419
            app .setStyle ('Windows')#line:420
            application =MyyWindow ()#line:422
            application .show ()#line:423
            if application .is_login_likest is False and 'login'in application .data :#line:424
                application .err_dialog .set_text (f"Unsuccessful login likest.")#line:425
                application .err_dialog .show ()#line:426
            sys .exit (app .exec ())#line:427
        else :#line:428
            app =QtWidgets .QApplication ([])#line:429
            error_dialog =HwidDialog ()#line:430
            error_dialog .set_text (f'You are not Subscribed!\nHWID:')#line:431
            error_dialog .set_hwid (get_hwid ())#line:432
            error_dialog .show ()#line:433
            app .exec_ ()#line:434
    except Exception as e :#line:435
        logging .error (e )#line:436
'''
beta.alfaliker.com /бан ссылки 10-15 мин
turboliker.ru
likes.fm
snebes.ru
freelikes.online net

https://app.likeorgasm.com/cabinet
'''#line:446
