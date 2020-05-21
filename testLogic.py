""#line:1
import json #line:2
import logging #line:3
import os #line:4
import pickle #line:5
import multiprocessing as mp #line:6
import re #line:7
import sys #line:8
import time #line:9
import random #line:10
import string #line:11
from multiprocessing import Pool #line:12
import requests #line:14
from bs4 import BeautifulSoup as BS #line:15
with open ('mylog.log','w')as f :#line:20
    f .writelines ('')#line:21
logging .basicConfig (format =u'%(filename)s[LINE:%(lineno)-2s]# %(levelname)-8s [%(asctime)s] %(message)s',level =logging .DEBUG ,filename =u'mylog.log')#line:24
class User :#line:28
    ""#line:29
    def __init__ (O0000000OO0O00O0O ,O000OO00OO00OO0O0 ,OOOOOOOO0O000O000 ):#line:31
        O0000000OO0O00O0O .username =O000OO00OO00OO0O0 #line:32
        O0000000OO0O00O0O .password =OOOOOOOO0O000O000 #line:33
        O0000000OO0O00O0O .banned_users =[]#line:34
        O0000000OO0O00O0O .token =None #line:35
        O0000000OO0O00O0O .session =requests .Session ()#line:36
        O0000000OO0O00O0O .headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)' ' AppleWebKit/537.36 (KHTML, like Gecko)' ' Chrome/79.0.3945.130 Safari/537.36','Accept':'*/*','Accept-Language':'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:45
        O0000000OO0O00O0O .item_id =None #line:47
        O0000000OO0O00O0O .user_id =None #line:48
    def method (O0O0O0OO0OO0OO0O0 ,OO0O0O00000000000 ,values =None ):#line:50
        ""#line:55
        try :#line:56
            if values is None :#line:57
                values ={}#line:58
            values ['v']='5.103'#line:59
            if O0O0O0OO0OO0OO0O0 .token :#line:60
                values ['access_token']=O0O0O0OO0OO0OO0O0 .token #line:61
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OO0OOO0OOOOO00000 :#line:63
            logging .error (OO0OOO0OOOOO00000 )#line:64
        else :#line:65
            return O0O0O0OO0OO0OO0O0 .session .post ('https://api.vk.com/method/'+OO0O0O00000000000 ,values )#line:69
    def login (OOOOO0OOOOO00OOOO ):#line:71
        ""#line:76
        try :#line:77
            if os .path .isfile ("cookies"):#line:78
                with open ('cookies','rb')as O0000O0OOO0OO00OO :#line:79
                    OOOOO0OOOOO00OOOO .session .cookies .update (pickle .load (O0000O0OOO0OO00OO ))#line:80
            O000O00O0O0O00O0O =OOOOO0OOOOO00OOOO .session .get ('https://m.vk.com/login')#line:82
            O0O00OOOOOO0OOO0O =BS (O000O00O0O0O00O0O .content ,'lxml')#line:83
            O00O0O00OOO00O00O =O0O00OOOOOO0OOO0O .select ('a[class=op_owner]')#line:84
            if not O00O0O00OOO00O00O :#line:85
                logging .info ("Updating cookies! Trying to login.")#line:86
                OO0OOOO0O0O0OOO00 =O0O00OOOOOO0OOO0O .find ('form')['action']#line:87
                OOO00O0O0OO0000O0 =OOOOO0OOOOO00OOOO .session .post (OO0OOOO0O0O0OOO00 ,data ={'email':OOOOO0OOOOO00OOOO .username ,'pass':OOOOO0OOOOO00OOOO .password },headers =OOOOO0OOOOO00OOOO .headers )#line:91
                O0O00OOOOOO0OOO0O =BS (OOO00O0O0OO0000O0 .content ,'lxml')#line:92
                O00O0O00OOO00O00O =O0O00OOOOOO0OOO0O .select ('a[class=op_owner]')#line:93
                if not O00O0O00OOO00O00O :#line:94
                    raise KeyError #line:95
            else :#line:96
                logging .info ("Logged by cookies!")#line:97
                logging .info ('Successfully login as: %s',O00O0O00OOO00O00O [0 ]["data-name"])#line:98
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as O0O0O0000OOOO0OOO :#line:99
            logging .error ('Shit happend. Login fail. %s',O0O0O0000OOOO0OOO )#line:100
        else :#line:101
            OOOOO0OOOOO00OOOO .get_token ()#line:102
            with open ('cookies','wb')as O0000O0OOO0OO00OO :#line:103
                pickle .dump (OOOOO0OOOOO00OOOO .session .cookies ,O0000O0OOO0OO00OO )#line:104
            return O00O0O00OOO00O00O [0 ]["data-name"]#line:105
    def make_repost (OO0OO0O0OO00OOO0O ,OO0OO00O0O000OO00 ):#line:107
        ""#line:110
        try :#line:111
            logging .info (f'Making report: {OO0OO00O0O000OO00}')#line:112
            OOOOO00O00OOOOOOO =OO0OO0O0OO00OOO0O .method ('wall.repost',({'object':OO0OO00O0O000OO00 })).json ()#line:113
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as O0OOOO0O00OOOOOO0 :#line:114
            logging .error (O0OOOO0O00OOOOOO0 )#line:115
        else :#line:116
            logging .info (OOOOO00O00OOOOOOO )#line:117
            if 'response'in OOOOO00O00OOOOOOO :#line:118
                OO0OO0O0OO00OOO0O .item_id =OOOOO00O00OOOOOOO ['response']['post_id']#line:119
            return OOOOO00O00OOOOOOO #line:120
    def delete_repost (OO0000O0OOOO0OO0O ):#line:122
        ""#line:125
        try :#line:126
            OO0O000000O00O00O =OO0000O0OOOO0OO0O .method ('wall.get',({'owner_id':OO0000O0OOOO0OO0O .user_id })).json ()#line:127
            if 'response'in OO0O000000O00O00O :#line:128
                OO0O000000O00O00O =OO0000O0OOOO0OO0O .method ('wall.delete',({'owner_id':OO0000O0OOOO0OO0O .user_id ,'post_id':OO0000O0OOOO0OO0O .item_id })).json ()#line:131
            logging .info (OO0O000000O00O00O )#line:132
        except (ConnectionError ,RuntimeError ,KeyError )as OOOOOOOO0OO0O0O00 :#line:133
            logging .error (OOOOOOOO0OO0O0O00 )#line:134
    def get_user_id_to_ban (O000O0OO0O0OO0OO0 ,O00O00O000OOO0O00 ):#line:136
        O0OO00OOO0000OO00 =None #line:137
        try :#line:138
            O00O00O000OOO0O00 =O00O00O000OOO0O00 .replace ("/","")#line:139
            O0OOO00000O0000O0 =O000O0OO0O0OO0OO0 .session .get (f"https://vk.com/{O00O00O000OOO0O00}")#line:140
            O0O000O0OO0OO0O00 =BS (O0OOO00000O0000O0 .text ,'html.parser')#line:141
            for OOOO0OOOO000OO0O0 in O0O000O0OO0OO0O00 .find_all ("a",attrs ={"class":"BtnStack__btn button wide_button acceptFriendBtn Btn Btn_theme_regular"}):#line:143
                O0OO00OOO0000OO00 =OOOO0OOOO000OO0O0 ['data-uid']#line:144
                break #line:145
            if O0OO00OOO0000OO00 is None :#line:149
                O0OO00OOO0000OO00 =O000O0OO0O0OO0OO0 .method ('users.get',({'user_ids':O00O00O000OOO0O00 })).json ()#line:150
                return O0OO00OOO0000OO00 ['response'][0 ]['id']#line:151
        except Exception as O0O0O0OOOOO00OOO0 :#line:152
            logging .error (O0O0O0OOOOO00OOO0 )#line:153
        else :#line:154
            return O0OO00OOO0000OO00 #line:155
    def get_user_id (OOO00OOO0OO0O0OOO ):#line:157
        ""#line:160
        O0O0O00OOO00O00O0 =OOO00OOO0OO0O0OOO .method ('users.get').json ()#line:161
        if 'response'in O0O0O00OOO00O00O0 :#line:162
            OOO00OOO0OO0O0OOO .user_id =O0O0O00OOO00O00O0 ['response'][0 ]['id']#line:163
            logging .info ("user_id = %s",OOO00OOO0OO0O0OOO .user_id )#line:164
        return OOO00OOO0OO0O0OOO .user_id #line:165
    def get_token (OO000OO0OO0OO0OO0 ):#line:167
        ""#line:171
        O0OOOOO0000OOO000 =2274003 #line:172
        OO0O0OO000O0O00O0 ='hHbZxrka2uZ6jB1inYsH'#line:173
        OOO0OOO00OOO0000O ={}#line:174
        OO0OOOOOO00000O0O =f'https://oauth.vk.com/token?grant_type=password&client_id={O0OOOOO0000OOO000}&client_secret={OO0O0OO000O0O00O0}&username={OO000OO0OO0OO0OO0.username}&password={OO000OO0OO0OO0OO0.password}&v=5.103&2fa_supported=1'#line:176
        try :#line:177
            OOO0OOO00OOO0000O =requests .get (OO0OOOOOO00000O0O ).json ()#line:178
            OO000OO0OO0OO0OO0 .token =OOO0OOO00OOO0000O ['access_token']#line:179
        except KeyError as O00OO00O0OOO00OO0 :#line:181
            logging .info ('Didn`t get: %s',O00OO00O0OOO00OO0 .args [0 ])#line:182
            if 'error'in OOO0OOO00OOO0000O :#line:183
                logging .info ("Причина: %s",OOO0OOO00OOO0000O ['error_description'])#line:184
        except ConnectionError as O00OO00O0OOO00OO0 :#line:185
            logging .error ("Connection error")#line:186
        else :#line:187
            OO000OO0OO0OO0OO0 .user_id =OO000OO0OO0OO0OO0 .get_user_id ()#line:188
            return OO000OO0OO0OO0OO0 .token #line:189
    def login_likest (OOOO00OOO0000O000 ):#line:191
        ""#line:194
        O000OOOO00O0000O0 ={}#line:195
        logging .info ('Trying to login to likest')#line:196
        try :#line:197
            O00O0OO00OOO0O000 =requests .head ("https://ulogin.ru/auth.php?name=vkontakte")#line:198
            logging .info (O00O0OO00OOO0O000 .status_code )#line:199
            if O00O0OO00OOO0O000 .status_code ==500 :#line:200
                return False #line:201
            O00OOOO00OOOO0OOO =OOOO00OOO0000O000 .session .get ('https://ulogin.ru/auth.php?name=vkontakte')#line:203
            OO0000OOOOO0O0O00 =BS (O00OOOO00OOOO0OOO .content ,'lxml')#line:204
            OO0OOOOOOOOOOO0O0 =OO0000OOOOO0O0O00 .select ('script')#line:205
            O000O00OO00O00000 ="token = \'(.+)\'"#line:207
            if OO0OOOOOOOOOOO0O0 :#line:208
                O0OO0OO00O0000OO0 =re .search (O000O00OO00O00000 ,str (OO0OOOOOOOOOOO0O0 )).group (1 )#line:209
                logging .info (f'Likest token: {O0OO0OO00O0000OO0}')#line:210
            else :#line:211
                logging .error ("Can`t find <script token=...>")#line:212
            if O0OO0OO00O0000OO0 :#line:214
                O000OOOO00O0000O0 =OOOO00OOO0000O000 .session .post ('https://likest.ru/user/login-ulogin/token',headers =OOOO00OOO0000O000 .headers ,data ={'token':O0OO0OO00O0000OO0 })#line:218
        except (NameError ,KeyError ,Exception )as OO0OOO0O0O000000O :#line:220
            logging .info ('Failed login likest')#line:221
            logging .error (OO0OOO0O0O000000O )#line:222
            return False #line:223
        else :#line:224
            logging .info ("Succ logged Likest")#line:225
            return True #line:226
    def get_likes_balance (O0O0OOO0OOOOOOO00 ):#line:228
        ""#line:231
        try :#line:232
            O00O0OOO0O0000OOO =O0O0OOO0OOOOOOO00 .session .get (f'http://likest.ru/api/balance.get',headers =O0O0OOO0OOOOOOO00 .headers ).json ()#line:234
        except (TimeoutError ,ConnectionError ,RuntimeError )as O0O00OOO00000OO0O :#line:235
            logging .error (O0O00OOO00000OO0O )#line:236
        else :#line:237
            logging .info ('Likest balance %s',O00O0OOO0O0000OOO )#line:238
            return O00O0OOO0O0000OOO #line:239
    def activate_coupon (OOOOO00OO0OOO0O00 ,OO00O00OOOO000O0O ):#line:241
        ""#line:244
        try :#line:245
            O00OO0OO000O0OO0O =OOOOO00OO0OOO0O00 .session .post ('http://likest.ru/api/coupons.use',data ={'coupons':str (OO00O00OOOO000O0O )},headers =OOOOO00OO0OOO0O00 .headers ).json ()#line:248
        except (TimeoutError ,ConnectionError ,RuntimeError )as O0OO0O000O00O0O0O :#line:250
            logging .error (O0OO0O000O00O0O0O )#line:251
        else :#line:252
            logging .info ('Result %s',O00OO0OO000O0OO0O )#line:253
            return O00OO0OO000O0OO0O #line:254
    def add_likest_task (O0OO0O00OO0O00O0O ,OOOOOO000OO000O0O ,OO00O0OO000OOO000 ,OOOOO0OO0OO00OOO0 ,reward =''):#line:256
        ""#line:260
        O00OO0OOOOOO00OO0 ='https://likest.ru/system/ajax'#line:261
        OOO0O00000O00OO00 =''#line:262
        try :#line:263
            if OOOOO0OO0OO00OOO0 =='l':#line:264
                O0OOO0O0OOOOOOOOO =O0OO0O00OO0O00O0O .session .get ('https://likest.ru/buy-likes',headers =O0OO0O00OO0O00O0O .headers )#line:266
                OOO0O00000O00OO00 ='hpoints_buy_likes_form'#line:267
                _OO000O0OO0OOOOO0O ='Заказать'#line:268
            else :#line:271
                O0OOO0O0OOOOOOOOO =O0OO0O00OO0O00O0O .session .get ('https://likest.ru/reposts/add',headers =O0OO0O00OO0O00O0O .headers )#line:273
                OOO0O00000O00OO00 ='hpoints_reposts_add_form'#line:274
                _OO000O0OO0OOOOO0O ='Получить репосты'#line:275
            OO00OOO00OOO0OO0O =BS (O0OOO0O0OOOOOOOOO .content ,'lxml')#line:277
            O000O00OOO0O0OOO0 =OO00OOO00OOO0OO0O .select ('input[name=form_build_id]')#line:278
            O0O000O00OO0O00O0 =OO00OOO00OOO0OO0O .select ('input[name=form_token]')#line:279
            O000O00OOO0O0OOO0 =str (O000O00OOO0O0OOO0 ).split ('"')[5 ]#line:281
            O0O000O00OO0O00O0 =str (O0O000O00OO0O00O0 ).split ('"')[5 ]#line:282
            OOOO0OOO0OO000O0O ={"title":OO00O0OO000OOO000 ,"link":OO00O0OO000OOO000 ,"reward":reward ,"amount":OOOOOO000OO000O0O ,"sex":"0","country":"0","age_min":"0","age_max":"255","friends_min":"0","lim_5":"0","lim_30":"0","lim_60":"0","sleepy_factor":"0","form_build_id":O000O00OOO0O0OOO0 ,"form_token":O0O000O00OO0O00O0 ,"form_id":OOO0O00000O00OO00 ,"_triggering_element_name":"op","_triggering_element_value":_OO000O0OO0OOOOO0O }#line:303
            if OOOOO0OO0OO00OOO0 =='l':#line:305
                O0OO0O00OO0O00O0O .session .head ('https://likest.ru/buy-likes')#line:306
            else :#line:307
                O0OO0O00OO0O00O0O .session .head ('https://likest.ru/reposts/add')#line:308
            O00O0OOO0OOO00OO0 =O0OO0O00OO0O00O0O .session .post (O00OO0OOOOOO00OO0 ,data =OOOO0OOO0OO000O0O ,headers =O0OO0O00OO0O00O0O .headers )#line:311
            logging .info (O00O0OOO0OOO00OO0 )#line:312
        except (ConnectionError ,TimeoutError ,ValueError ,RuntimeError )as OO00OOOOO00000O0O :#line:314
            logging .error (OO00OOOOO00000O0O )#line:315
        else :#line:316
            logging .info ('Task added!!!!')#line:317
    def get_likes_list (O0O00OOOO0OO00OOO ):#line:319
        try :#line:320
            O0000O0000OO0OO00 ="https://vk.com/wkview.php"#line:321
            O0000OO0O00O0OO0O ={"act":"show","al":1 ,"loc":f"wall{O0O00OOOO0OO00OOO.user_id}_{O0O00OOOO0OO00OOO.item_id}","location_owner_id":O0O00OOOO0OO00OOO .user_id ,"w":f"likes/wall{O0O00OOOO0OO00OOO.user_id}_{O0O00OOOO0OO00OOO.item_id}"}#line:328
            OO000OOO00O0O0O0O =[]#line:329
            O0OOO0O0O0O0OO00O =requests .post (O0000O0000OO0OO00 ,O0000OO0O00O0OO0O )#line:330
            O0OOO0O0O0O0OO00O =O0OOO0O0O0O0OO00O .text .replace ("\\","")#line:331
            O0O00OO0OO0O0O000 =BS (O0OOO0O0O0O0OO00O ,'html.parser')#line:332
            for OOO00000OO00000O0 in O0O00OO0OO0O0O000 .find_all ("a",attrs ={"class":"fans_fan_ph"}):#line:334
                OO000OOO00O0O0O0O .append (OOO00000OO00000O0 ["href"])#line:335
        except Exception as OO0OO0O00O00O00OO :#line:336
            logging .error (OO0OO0O00O00O00OO )#line:337
        else :#line:338
            return OO000OOO00O0O0O0O #line:339
    def ban_user_report (O0000OOO00O00O0O0 ):#line:341
        ""#line:344
        O00O00OO0OOOOOO0O =[]#line:345
        try :#line:346
            O00O00OO0OOOOOO0O =O0000OOO00O00O0O0 .get_likes_list ()#line:347
        except KeyError as OO000O00OOO0OOOO0 :#line:348
            logging .error (OO000O00OOO0OOOO0 )#line:349
        try :#line:350
            if not O00O00OO0OOOOOO0O :#line:351
                return None #line:352
            for OOOOO0OO00O0O0OO0 in O00O00OO0OOOOOO0O :#line:353
                if re .match ('id([0-9])+',OOOOO0OO00O0O0OO0 )is None :#line:354
                    OOOOO0OO00O0O0OO0 =O0000OOO00O00O0O0 .get_user_id_to_ban (OOOOO0OO00O0O0OO0 )#line:355
                else :#line:357
                    OOOOO0OO00O0O0OO0 =OOOOO0OO00O0O0OO0 .replace ("/id","")#line:358
                O00000OOO00O0OO0O ={'act':'spam','al':'1','mid':OOOOO0OO00O0O0OO0 ,'object':'wall'+str (O0000OOO00O00O0O0 .user_id )+'_'+str (O0000OOO00O00O0O0 .item_id )}#line:364
                OOOO00000O00O0000 =O0000OOO00O00O0O0 .session .post ('https://vk.com/like.php',data =O00000OOO00O0OO0O )#line:367
                O0OO0O0OOO0000000 =re .findall ('hash: \'(?:[a-zA-Z]|[0-9])+',str (OOOO00000O00O0000 .text ))[0 ]#line:369
                O0OO0O0OOO0000000 =O0OO0O0OOO0000000 .replace ('hash: \'','')#line:370
                O0000O0O00O0OO000 =O0OO0O0OOO0000000 .replace ('"','')#line:371
                O00000OOO00O0OO0O ={'act':'do_spam','al':'1','hash':O0000O0O00O0OO000 ,'mid':OOOOO0OO00O0O0OO0 ,'object':'wall'+str (O0000OOO00O00O0O0 .user_id )+'_'+str (O0000OOO00O00O0O0 .item_id )}#line:379
                O0000OOO00O00O0O0 .session .post ('https://vk.com/like.php',data =O00000OOO00O0OO0O )#line:382
                O0000OOO00O00O0O0 .banned_users .append (OOOOO0OO00O0O0OO0 )#line:383
        except Exception as O0O0O00O000OO0000 :#line:384
            logging .log (O0O0O00O000OO0000 )#line:385
        O00O00OO0OOOOOO0O =[]#line:386
        time .sleep (0.4 )#line:387
    def unban_users (OO0O00O0OO0O00O0O ):#line:389
        O0000O0000OO0OO0O =OO0O00O0OO0O00O0O .session .post ('https://vk.com/settings?act=blacklist')#line:390
        OOO000000O000O000 =re .findall (f'Settings.delFromBl\((?:[0-9]+), \'(?:[a-zA-Z]|[0-9])+',str (O0000O0000OO0OO0O .text ))#line:392
        for OOOO00O00O0OO000O in OOO000000O000O000 :#line:394
            OOOO00O00O0OO000O =OOOO00O00O0OO000O .replace (f'Settings.delFromBl(','').replace (" \\","").replace ("'","").replace (" ","").split (",")#line:395
            OO0000OO00O0OO0OO =OOOO00O00O0OO000O [0 ]#line:396
            O0O0O0OOO00OO00OO =OOOO00O00O0OO000O [1 ]#line:397
            OOO0OOOO00O0O0OO0 ={'act':'a_del_from_bl','al':'1','from':'settings','hash':O0O0O0OOO00OO00OO ,'id':OO0000OO00O0OO0OO }#line:405
            print (OOO0OOOO00O0O0OO0 )#line:406
            OO0O00O0OO0O00O0O .session .post ('https://vk.com/al_settings.php',data =OOO0OOOO00O0O0OO0 )#line:408
    def get_data_from_link (O0000OOOOO0000O0O ,O000O000OO000OOOO ):#line:410
        ""#line:413
        try :#line:414
            OO0O00O00OO0O0O00 =(re .findall ('wall-?(.+)_(\\d+)',O000O000OO000OOOO ))#line:415
            if not OO0O00O00OO0O0O00 :#line:416
                raise IndexError #line:417
        except IndexError as O00OOO00OO00O0O0O :#line:418
            logging .error ("Invalid url! %s",O00OOO00OO00O0O0O )#line:419
        else :#line:420
            O0000OOOOO0000O0O .item_id =OO0O00O00OO0O0O00 [0 ][1 ]#line:421
            return OO0O00O00OO0O0O00 [0 ]#line:422
def save_data_to_file (**OOOOO00O000O0OO00 ):#line:425
    ""#line:429
    try :#line:430
        OO0000OOO0O0O0O0O ={}#line:431
        with open ('data.txt','r+')as O0O0OOO0O0O0O0000 :#line:432
            OO0000OOO0O0O0O0O =json .load (O0O0OOO0O0O0O0000 )#line:433
        for OO0O0O00OOOOO0OOO in OOOOO00O000O0OO00 :#line:435
            OO0000OOO0O0O0O0O [OO0O0O00OOOOO0OOO ]=OOOOO00O000O0OO00 [OO0O0O00OOOOO0OOO ]#line:436
        with open ('data.txt','w+')as O0O0OOO0O0O0O0000 :#line:438
            json .dump (OO0000OOO0O0O0O0O ,O0O0OOO0O0O0O0000 )#line:439
        return OO0000OOO0O0O0O0O #line:441
    except KeyError as O00O0OOO0O0OO0OO0 :#line:442
        if O00O0OOO0O0OO0OO0 .args [0 ]in ['link','login','password','token']:#line:443
            logging .info ('Cannot find: %s',O00O0OOO0O0OO0OO0 .args [0 ])#line:444
    except IOError as O00O0OOO0O0OO0OO0 :#line:446
        logging .info (O00O0OOO0O0OO0OO0 )#line:447
def load_data_from_file ():#line:450
    ""#line:454
    OO00000000OO000OO ={}#line:455
    try :#line:456
        if not os .path .exists ('data.txt'):#line:457
            with open ('data.txt','w')as O0O000O000O0OO00O :#line:458
                O0O000O000O0OO00O .write ('{}')#line:459
        with open ('data.txt')as OOOOOO0O000O00OOO :#line:461
            OO000000OOO0OO0OO =json .load (OOOOOO0O000O00OOO )#line:462
        if 'login'in OO000000OOO0OO0OO :#line:464
            OO00000000OO000OO ['login']=OO000000OOO0OO0OO ['login']#line:465
        if 'password'in OO000000OOO0OO0OO :#line:466
            OO00000000OO000OO ['password']=OO000000OOO0OO0OO ['password']#line:467
        if 'token'in OO000000OOO0OO0OO :#line:468
            OO00000000OO000OO ['token']=OO000000OOO0OO0OO ['token']#line:469
        if 'url'in OO000000OOO0OO0OO :#line:470
            OO00000000OO000OO ['url']=OO000000OOO0OO0OO ['url']#line:471
        if 'user_id'in OO000000OOO0OO0OO :#line:472
            OO00000000OO000OO ['user_id']=OO000000OOO0OO0OO ['user_id']#line:473
    except KeyError as OO0OOOO00OOOO0O0O :#line:475
        if OO0OOOO00OOOO0O0O .args [0 ]in ['link','login','password','token']:#line:476
            logging .error ('Cannot find: %s',OO0OOOO00OOOO0O0O .args [0 ])#line:477
    except Exception as OO0OOOO00OOOO0O0O :#line:478
        raise OO0OOOO00OOOO0O0O #line:479
    else :#line:480
        return OO00000000OO000OO #line:481
