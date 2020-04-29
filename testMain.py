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
def resource_path (OOOOOOOOOOOOO0OOO ):#line:24
    ""#line:25
    """ Get absolute path to resource, works for dev and for PyInstaller """#line:26
    O0OO0000OO00O00O0 =getattr (sys ,'_MEIPASS',os .path .dirname (os .path .abspath (__file__ )))#line:27
    return os .path .join (O0OO0000OO00O00O0 ,OOOOOOOOOOOOO0OOO )#line:28
class QTextEditLogger (logging .Handler ):#line:31
    def __init__ (OOOO0O000OOOOOO0O ,O00O0OOO000O000O0 ):#line:32
        super ().__init__ ()#line:33
        OOOO0O000OOOOOO0O .widget =QtWidgets .QPlainTextEdit (O00O0OOO000O000O0 )#line:34
        OOOO0O000OOOOOO0O .widget .setReadOnly (True )#line:35
        OOOO0O000OOOOOO0O .widget .setFixedSize (680 ,420 )#line:36
    def emit (OOOOOOOOOO0OOOO00 ,OOOOO000OOOOO0O0O ):#line:38
        O0O00OOOOOOO0O00O =OOOOOOOOOO0OOOO00 .format (OOOOO000OOOOO0O0O )#line:39
        OOOOOOOOOO0OOOO00 .widget .appendPlainText (O0O00OOOOOOO0O00O )#line:40
class ErrorDialog (QtWidgets .QDialog ):#line:43
    def __init__ (OO00O00O00O00O000 ,parent =None ):#line:44
        super (ErrorDialog ,OO00O00O00O00O000 ).__init__ (parent )#line:45
        OO00O00O00O00O000 .ui =Ui_Error ()#line:46
        OO00O00O00O00O000 .ui .setupUi (OO00O00O00O00O000 )#line:47
    def set_text (O000OOO0OOOOOO00O ,O0OO00O00O00OO00O ):#line:49
        O000OOO0OOOOOO00O .ui .label .setText (O0OO00O00O00OO00O )#line:50
class MyyWindow (QtWidgets .QMainWindow ):#line:53
    def __init__ (OOO00O0O0000OO00O ):#line:54
        super (MyyWindow ,OOO00O0O0000OO00O ).__init__ ()#line:55
        OOO00O0O0000OO00O .m_thread =None #line:56
        OOO00O0O0000OO00O .current_window =None #line:57
        OOO00O0O0000OO00O .ui =Ui_MainWindow ()#line:58
        OOO00O0O0000OO00O .ui .setupUi (OOO00O0O0000OO00O )#line:59
        OOO00O0O0000OO00O .ui .stackedWidget .setCurrentIndex (0 )#line:60
        OOO00O0O0000OO00O .err_dialog =ErrorDialog ()#line:63
        OOO00O0O0000OO00O .data_result =None #line:64
        OOO00O0O0000OO00O .m_modbus_worker =None #line:65
        OOO00O0O0000OO00O .ui .LikesButton .clicked .connect (OOO00O0O0000OO00O .set_page_view_likes )#line:67
        OOO00O0O0000OO00O .ui .LogsButton .clicked .connect (OOO00O0O0000OO00O .set_page_view_logs )#line:68
        OOO00O0O0000OO00O .ui .VkLoginButton .clicked .connect (OOO00O0O0000OO00O .set_page_view_vklogin )#line:69
        OOO00O0O0000OO00O .ui .vkImage .setPixmap (QtGui .QPixmap (resource_path ('vk.png')))#line:70
        OOO00O0O0000OO00O .ui .pushButton_4 .clicked .connect (OOO00O0O0000OO00O .vk_login )#line:72
        OOO00O0O0000OO00O .ui .SaveUrlButton .clicked .connect (OOO00O0O0000OO00O .save_url )#line:73
        OOO00O0O0000OO00O .ui .SaveUrlButton_R .clicked .connect (OOO00O0O0000OO00O .save_url )#line:74
        OOO00O0O0000OO00O .ui .SaveCouponButton .clicked .connect (OOO00O0O0000OO00O .save_coupon )#line:77
        OOO00O0O0000OO00O .ui .getBalance .clicked .connect (OOO00O0O0000OO00O .get_likest_balance )#line:79
        OOO00O0O0000OO00O .ui .ReposButton .clicked .connect (OOO00O0O0000OO00O .set_page_view_repost )#line:80
        O000OO0O0O000O0OO =QTextEditLogger (OOO00O0O0000OO00O .ui .plainTextEdit )#line:82
        O000OO0O0O000O0OO .setFormatter (logging .Formatter ('%(filename)s[LINE:%(lineno)-4s]' ' #%(levelname)-4s [%(asctime)s]  %(message)s'))#line:85
        logging .getLogger ().addHandler (O000OO0O0O000O0OO )#line:86
        OOO00O0O0000OO00O .data =None #line:88
        OOO00O0O0000OO00O .user =None #line:89
        OOO00O0O0000OO00O .user_id =None #line:90
        OOO00O0O0000OO00O .post_id =None #line:91
        OOO00O0O0000OO00O .token =None #line:92
        OOO00O0O0000OO00O .ui .StopLikes .clicked .connect (OOO00O0O0000OO00O .stop )#line:96
        OOO00O0O0000OO00O .ui .StartLikes .clicked .connect (OOO00O0O0000OO00O .start )#line:97
        OOO00O0O0000OO00O .ui .StopLikes_R .clicked .connect (OOO00O0O0000OO00O .stop )#line:99
        OOO00O0O0000OO00O .ui .StartLikes_R .clicked .connect (OOO00O0O0000OO00O .start )#line:100
        try :#line:102
            logging .info ('Trying to load all data from file')#line:103
            OOO00O0O0000OO00O .data =load_data_from_file ()#line:104
        except Exception as OOOO00O0OO0000O0O :#line:106
            logging .error (OOOO00O0OO0000O0O )#line:107
        if 'login'in OOO00O0O0000OO00O .data and 'password'in OOO00O0O0000OO00O .data and 'token'in OOO00O0O0000OO00O .data :#line:109
            OOO00O0O0000OO00O .token =OOO00O0O0000OO00O .data ['token']#line:110
            OOO00O0O0000OO00O .user =User (username =OOO00O0O0000OO00O .data ['login'],password =OOO00O0O0000OO00O .data ['password'])#line:114
            OOO00O0O0000OO00O .login_result =OOO00O0O0000OO00O .user .login ()#line:116
            OOO00O0O0000OO00O .ui .ResultOfLogin .setText (f"Welcome back {OOO00O0O0000OO00O.login_result}")#line:117
            OOO00O0O0000OO00O .user .login_likest ()#line:118
        elif ('token'not in OOO00O0O0000OO00O .data )and ('login'in OOO00O0O0000OO00O .data ):#line:120
            OOO00O0O0000OO00O .user =User (username =OOO00O0O0000OO00O .data ['login'],password =OOO00O0O0000OO00O .data ['password'])#line:121
            OOO00O0O0000OO00O .user .login ()#line:122
            OOO00O0O0000OO00O .token =OOO00O0O0000OO00O .user .get_token ()#line:123
            O0OOOOOO00O0O0000 =Template ("Ur token $token")#line:124
            logging .info (O0OOOOOO00O0O0000 .substitute (OOO00O0O0000OO00O .token ))#line:125
            OOO00O0O0000OO00O .data_saved =save_data_to_file (login =OOO00O0O0000OO00O .data ['login'],password =OOO00O0O0000OO00O .data ['password'],token =OOO00O0O0000OO00O .token )#line:131
            OOO00O0O0000OO00O .user .login_likest ()#line:132
            logging .info (f"Saved data {OOO00O0O0000OO00O.data_saved}")#line:133
        if 'user_id'in OOO00O0O0000OO00O .data :#line:134
            OOO00O0O0000OO00O .user .user_id =OOO00O0O0000OO00O .data ['user_id']#line:135
    def save_coupon (OO00OO0OOO0O0OOO0 ):#line:137
        if not OO00OO0OOO0O0OOO0 .user :#line:138
            OO00OO0OOO0O0OOO0 .err_dialog .set_text ("You must log in")#line:139
            OO00OO0OOO0O0OOO0 .err_dialog .exec_ ()#line:140
        else :#line:141
            O00O000O000OOOO0O =OO00OO0OOO0O0OOO0 .ui .LabelCoupon .text ()#line:142
            O0O00O00000O00O00 =OO00OO0OOO0O0OOO0 .user .activate_coupon (O00O000O000OOOO0O )#line:143
            if 'SUCCESS'in O0O00O00000O00O00 ['status']:#line:145
                OO00OO0OOO0O0OOO0 .ui .ResultCoupon .setStyleSheet ("color: rgb(154, 255, 152);")#line:146
                OO00OO0OOO0O0OOO0 .ui .ResultCoupon .setText ('Activated')#line:147
            else :#line:148
                OO00OO0OOO0O0OOO0 .ui .ResultCoupon .setStyleSheet ("color: rgb(195, 15, 18);")#line:149
                OO00OO0OOO0O0OOO0 .ui .ResultCoupon .setText ('Not activated')#line:150
    def get_likest_balance (OO000O00OOOO000OO ):#line:152
        if not OO000O00OOOO000OO .user :#line:153
            OO000O00OOOO000OO .err_dialog .set_text ("You must log in")#line:154
            OO000O00OOOO000OO .err_dialog .exec_ ()#line:155
        else :#line:156
            OO000O00OOOO000OO .likes_balance =OO000O00OOOO000OO .user .get_likes_balance ()#line:157
            if 'balance'in OO000O00OOOO000OO .likes_balance :#line:158
                OOOOO0O0O0O0O0O0O =OO000O00OOOO000OO .likes_balance ['balance']#line:159
                OO000O00OOOO000OO .ui .LikesBalanceLabel .setText (str (OOOOO0O0O0O0O0O0O ))#line:160
    def on_succ_login (O0OOO00000O0OO000 ):#line:162
        if O0OOO00000O0OO000 .login_result :#line:163
            logging .info ('Data loaded. Token loaded. User session created.')#line:164
            O0OOO00000O0OO000 .ui .stackedWidget .setCurrentIndex (2 )#line:165
        if 'user_id'not in O0OOO00000O0OO000 .data :#line:168
            O0OOO00000O0OO000 .user_id =O0OOO00000O0OO000 .user .get_user_id ()#line:169
            O0OOO00000O0OO000 .data_saved =save_data_to_file (user_id =O0OOO00000O0OO000 .user_id )#line:170
    @QtCore .pyqtSlot ()#line:172
    def start (O000O0O0O00OO0O0O ):#line:173
        if not O000O0O0O00OO0O0O .user or not O000O0O0O00OO0O0O .data_result :#line:174
            if not O000O0O0O00OO0O0O .data_result :#line:175
                O000O0O0O00OO0O0O .err_dialog .set_text ("You must add url")#line:176
            else :#line:177
                O000O0O0O00OO0O0O .err_dialog .set_text ("You must log in")#line:178
            O000O0O0O00OO0O0O .err_dialog .exec_ ()#line:179
        else :#line:180
            logging .info ('Starting ban users.')#line:181
            OO0OOO000000OOOOO =''#line:182
            OO0OO0O0OOO00OO0O =None #line:183
            if O000O0O0O00OO0O0O .current_window ==3 :#line:184
                OO0OOO000000OOOOO ='r'#line:185
                OO0OO0O0OOO00OO0O =O000O0O0O00OO0O0O .ui .Reward .text ()#line:186
                O00O0OO000O0O0OO0 =O000O0O0O00OO0O0O .ui .RepostsCount .text ()#line:187
            else :#line:188
                OO0OOO000000OOOOO ='l'#line:189
                O00O0OO000O0O0OO0 =O000O0O0O00OO0O0O .ui .LikesCount .text ()#line:190
            if O000O0O0O00OO0O0O .ui .LikestCheckBox .isChecked ()or O000O0O0O00OO0O0O .ui .RepostsCheckBox .isChecked ():#line:192
                O0OOOO0OO0000O0O0 =f'https://vk.com/wall{O000O0O0O00OO0O0O.user.user_id}_{O000O0O0O00OO0O0O.user.item_id}'#line:193
                save_data_to_file (url_tolike =O0OOOO0OO0000O0O0 ,post_id =O000O0O0O00OO0O0O .user .item_id )#line:195
                O000O0O0O00OO0O0O .user .add_likest_task (likes_count =O00O0OO000O0O0OO0 ,like_url =O0OOOO0OO0000O0O0 ,repost_like =OO0OOO000000OOOOO ,reward =OO0OO0O0OOO00OO0O )#line:197
                if O000O0O0O00OO0O0O .current_window ==3 :#line:199
                    O000O0O0O00OO0O0O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:200
                    O000O0O0O00OO0O0O .ui .ResultSaveUrl_R .setText ("Task added")#line:201
                else :#line:202
                    O000O0O0O00OO0O0O .ui .ResultSaveUrl .setText ("Task added!")#line:203
            else :#line:204
                logging .info ('Not log likest')#line:205
                if O000O0O0O00OO0O0O .current_window ==3 :#line:206
                    O000O0O0O00OO0O0O .ui .ResultSaveUrl_R .setText ("You must add a task.")#line:207
                else :#line:208
                    O000O0O0O00OO0O0O .ui .ResultSaveUrl .setText ("You must add a task.")#line:209
            O000O0O0O00OO0O0O .m_thread =QtCore .QThread (O000O0O0O00OO0O0O )#line:211
            O000O0O0O00OO0O0O .m_modbus_worker =ModbusWorker (O000O0O0O00OO0O0O .user )#line:212
            O000O0O0O00OO0O0O .m_modbus_worker .moveToThread (O000O0O0O00OO0O0O .m_thread )#line:213
            O000O0O0O00OO0O0O .m_thread .start ()#line:214
            QtCore .QTimer .singleShot (0 ,O000O0O0O00OO0O0O .m_modbus_worker .do_work )#line:215
            if O000O0O0O00OO0O0O .current_window ==3 :#line:217
                O000O0O0O00OO0O0O .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:218
                O000O0O0O00OO0O0O .ui .ResultStartLikes_R .setText ("  Started!")#line:219
            else :#line:220
                O000O0O0O00OO0O0O .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:221
                O000O0O0O00OO0O0O .ui .ResultStartLikes .setText ("  Started!")#line:222
    @QtCore .pyqtSlot ()#line:224
    def stop (OOO00O0O0000O0OO0 ):#line:225
        if OOO00O0O0000O0OO0 .m_modbus_worker :#line:226
            OOO00O0O0000O0OO0 .m_modbus_worker .stop ()#line:227
            OOO00O0O0000O0OO0 .m_modbus_worker .terminate ()#line:228
        if OOO00O0O0000O0OO0 .m_thread :#line:229
            OOO00O0O0000O0OO0 .m_thread .requestInterruption ()#line:230
            OOO00O0O0000O0OO0 .ui .ResultStartLikes .setStyleSheet ("color: rgb(195, 15, 18);")#line:231
            OOO00O0O0000O0OO0 .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:232
            OOO00O0O0000O0OO0 .ui .ResultStartLikes .setText (" Wait!")#line:233
            OOO00O0O0000O0OO0 .ui .ResultStartLikes_R .setText (" Wait!")#line:234
            OOO00O0O0000O0OO0 .user .delete_repost ()#line:235
            OOO00O0O0000O0OO0 .user .unban_users ()#line:236
            OOO00O0O0000O0OO0 .ui .ResultStartLikes_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:237
            OOO00O0O0000O0OO0 .ui .ResultStartLikes .setStyleSheet ("color: rgb(154, 255, 152);")#line:238
            OOO00O0O0000O0OO0 .ui .ResultStartLikes .setText (" Stopped")#line:239
            OOO00O0O0000O0OO0 .ui .ResultStartLikes_R .setText (" Stopped")#line:240
            OOO00O0O0000O0OO0 .m_thread .quit ()#line:241
            OOO00O0O0000O0OO0 .m_thread .wait ()#line:242
            sys .exit (OOO00O0O0000O0OO0 .m_thread .exec ())#line:243
    def save_url (O0O00OOO0000O000O ):#line:245
        if not O0O00OOO0000O000O .user :#line:246
            O0O00OOO0000O000O .err_dialog .set_text ("You must log in")#line:247
            O0O00OOO0000O000O .err_dialog .exec_ ()#line:248
        else :#line:249
            if O0O00OOO0000O000O .current_window ==3 :#line:250
                O0OO0OO00OOOO0O0O =O0O00OOO0000O000O .ui .LabelRepostsUrl .text ()#line:251
            else :#line:252
                O0OO0OO00OOOO0O0O =O0O00OOO0000O000O .ui .LabelLikesUrl .text ()#line:253
            if O0OO0OO00OOOO0O0O is None :#line:255
                O0OO0OO00OOOO0O0O =O0O00OOO0000O000O .ui .LabelRepostsUrl .text ()#line:256
            O0O00OOO0000O000O .data_result =O0O00OOO0000O000O .user .get_data_from_link (O0OO0OO00OOOO0O0O )#line:258
            O00OO0OOOOO0OO0OO ={}#line:259
            if not O0OO0OO00OOOO0O0O :#line:261
                O0O00OOO0000O000O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:262
                O0O00OOO0000O000O .ui .ResultSaveUrl .setText ("Enter Url")#line:263
                if O0O00OOO0000O000O .current_window ==3 :#line:264
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:265
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setText ("Enter Url")#line:266
            elif not O0O00OOO0000O000O .data_result :#line:267
                O0O00OOO0000O000O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(195, 15, 18);")#line:268
                O0O00OOO0000O000O .ui .ResultSaveUrl .setText ("Invalid url.")#line:269
                if O0O00OOO0000O000O .current_window ==3 :#line:270
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(195, 15, 18);")#line:271
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setText ("Invalid url.")#line:272
            else :#line:273
                O00OO0OOOOO0OO0OO =save_data_to_file (url_tolike =O0OO0OO00OOOO0O0O ,post_id =O0O00OOO0000O000O .data_result [1 ])#line:275
                O0O00OOO0000O000O .ui .ResultSaveUrl .setStyleSheet ("color: rgb(154, 255, 152);")#line:276
                O0O00OOO0000O000O .ui .ResultSaveUrl .setText ("Saved")#line:277
                if O0O00OOO0000O000O .current_window ==3 :#line:278
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setStyleSheet ("color: rgb(154, 255, 152);")#line:279
                    O0O00OOO0000O000O .ui .ResultSaveUrl_R .setText ("Saved")#line:280
                logging .info (O0O00OOO0000O000O .data_result )#line:281
            O0O00OOO0000O000O .ui .LabelLikesUrl .clear ()#line:283
            O0O00OOO0000O000O .ui .LabelRepostsUrl .clear ()#line:284
            if ('login'and 'password'and 'url')in O00OO0OOOOO0OO0OO :#line:285
                logging .info (O00OO0OOOOO0OO0OO )#line:286
    def set_page_view_likes (OO0OOOOO00O00O0O0 ):#line:288
        OO0OOOOO00O00O0O0 .current_window =2 #line:289
        OO0OOOOO00O00O0O0 .ui .stackedWidget .setCurrentIndex (2 )#line:290
    def set_page_view_repost (O0O00O0000O0OOO0O ):#line:292
        O0O00O0000O0OOO0O .current_window =3 #line:293
        O0O00O0000O0OOO0O .ui .stackedWidget .setCurrentIndex (3 )#line:294
    def set_page_view_logs (OOO0000O00OO0O000 ):#line:296
        OOO0000O00OO0O000 .current_window =1 #line:297
        OOO0000O00OO0O000 .ui .stackedWidget .setCurrentIndex (1 )#line:298
    def set_page_view_vklogin (OO00O000000O0OO0O ):#line:300
        OO00O000000O0OO0O .current_window =0 #line:301
        OO00O000000O0OO0O .ui .stackedWidget .setCurrentIndex (0 )#line:302
    def vk_login (O0O0O000O000OOOO0 ):#line:304
        OOOOO0OOO00O0O000 =O0O0O000O000OOOO0 .ui .lineEdit .text ()#line:305
        O0OOOO0000OOOO00O =O0O0O000O000OOOO0 .ui .lineEdit_2 .text ()#line:306
        if not (OOOOO0OOO00O0O000 and O0OOOO0000OOOO00O ):#line:307
            O0O0O000O000OOOO0 .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:308
            O0O0O000O000OOOO0 .ui .ResultOfLogin .setText ("Empty data")#line:309
        else :#line:310
            O0O0O000O000OOOO0 .user =User (OOOOO0OOO00O0O000 ,O0OOOO0000OOOO00O )#line:311
            O0O0OO0O000OO0O00 =O0O0O000O000OOOO0 .user .login ()#line:312
            if not O0O0OO0O000OO0O00 :#line:314
                O0O0O000O000OOOO0 .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:315
                O0O0O000O000OOOO0 .ui .ResultOfLogin .setText ("Unsuccessful login.\nInvalid email of password.")#line:316
            else :#line:317
                O0O0O000O000OOOO0 .token =O0O0O000O000OOOO0 .user .get_token ()#line:318
                O0O0O000O000OOOO0 .data =save_data_to_file (login =OOOOO0OOO00O0O000 ,password =O0OOOO0000OOOO00O ,token =O0O0O000O000OOOO0 .user .token ,user_id =O0O0O000O000OOOO0 .user .user_id )#line:324
                O0O0O000O000OOOO0 .check_login_result (O0O0O000O000OOOO0 .data )#line:325
    def check_login_result (OOOO0OO0OOOO00000 ,OOOOO00O0OO0O00O0 ):#line:327
        if not OOOO0OO0OOOO00000 .data or not OOOO0OO0OOOO00000 .data ['token']:#line:328
            OOOO0OO0OOOO00000 .ui .ResultOfLogin .setStyleSheet ("color: rgb(255, 121, 123);")#line:329
            OOOO0OO0OOOO00000 .ui .ResultOfLogin .setText ("Unsuccessful login")#line:330
        elif OOOO0OO0OOOO00000 .data ['token']:#line:331
            OOOO0OO0OOOO00000 .user .login_likest ()#line:332
            OOOO0OO0OOOO00000 .ui .ResultOfLogin .setStyleSheet ("color: rgb(154, 255, 152);")#line:333
            OOOO0OO0OOOO00000 .ui .ResultOfLogin .setText ("Successful login\nData saved to data.txt")#line:334
class ModbusWorker (QThread ):#line:337
    def __init__ (O0O00OO000O0O0OO0 ,O00000000O0OOOO00 ):#line:338
        super ().__init__ ()#line:339
        O0O00OO000O0O0OO0 .user =O00000000O0OOOO00 #line:340
        O0O00OO000O0O0OO0 .threadactive =True #line:341
    @QtCore .pyqtSlot ()#line:343
    def do_work (O00OO00OOO0OOO0O0 ):#line:344
        while not QtCore .QThread .currentThread ().isInterruptionRequested ()or O00OO00OOO0OOO0O0 .threadactive :#line:345
            O00OO00OOO0OOO0O0 .user .ban_user_report ()#line:347
    def stop (OOOO0000OOOO00OO0 ):#line:349
        OOOO0000OOOO00OO0 .threadactive =False #line:350
        OOOO0000OOOO00OO0 .wait ()#line:351
def check_hwid ():#line:354
    O00O0O0O00OO00O00 =requests .get ("https://pastebin.com/raw/GFQrRHcS")#line:355
    O0OOO0O00OOOO0OO0 =str (subprocess .check_output ('wmic csproduct get uuid')).split ('\\r\\n')[1 ].strip ('\\r').strip ()#line:356
    if O0OOO0O00OOOO0OO0 in O00O0O0O00OO00O00 .text :#line:357
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