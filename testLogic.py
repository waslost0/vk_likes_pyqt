""#line:1
import json #line:2
import logging #line:3
import os #line:4
import pickle #line:5
import re #line:6
import sys #line:7
import time #line:8
import random #line:9
import string #line:10
import requests #line:12
from bs4 import BeautifulSoup as BS #line:13
with open ('mylog.log','w')as f :#line:18
    f .writelines ('')#line:19
logging .basicConfig (format =u'%(filename)s[LINE:%(lineno)-2s]# %(levelname)-8s [%(asctime)s] %(message)s',level =logging .DEBUG ,filename =u'mylog.log')#line:22
class User :#line:25
    ""#line:26
    def __init__ (O0O0O0000O00O0O0O ,OO0O0OO0OO0OOO000 ,O00OO0OOO0000OO0O ):#line:28
        O0O0O0000O00O0O0O .username =OO0O0OO0OO0OOO000 #line:29
        O0O0O0000O00O0O0O .password =O00OO0OOO0000OO0O #line:30
        O0O0O0000O00O0O0O .banned_users =[]#line:31
        O0O0O0000O00O0O0O .token =None #line:32
        O0O0O0000O00O0O0O .session =requests .Session ()#line:33
        O0O0O0000O00O0O0O .headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)' ' AppleWebKit/537.36 (KHTML, like Gecko)' ' Chrome/79.0.3945.130 Safari/537.36','Accept':'*/*','Accept-Language':'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:42
        O0O0O0000O00O0O0O .item_id =None #line:44
        O0O0O0000O00O0O0O .user_id =None #line:45
    def method (OOO00O0OO00OO00OO ,O0OOO0O00O0OO0000 ,O00O00OOOO0OOO0OO =None ):#line:47
        ""#line:52
        try :#line:53
            if O00O00OOOO0OOO0OO is None :#line:54
                O00O00OOOO0OOO0OO ={}#line:55
            O00O00OOOO0OOO0OO ['v']='5.103'#line:56
            if OOO00O0OO00OO00OO .token :#line:57
                O00O00OOOO0OOO0OO ['access_token']=OOO00O0OO00OO00OO .token #line:58
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OO000O0O000O000OO :#line:60
            logging .error (OO000O0O000O000OO )#line:61
        else :#line:62
            return OOO00O0OO00OO00OO .session .post ('https://api.vk.com/method/'+O0OOO0O00O0OO0000 ,O00O00OOOO0OOO0OO )#line:66
    def login (OO0O0OOO0OOOO00O0 ):#line:68
        ""#line:73
        try :#line:74
            if os .path .isfile ("cookies"):#line:75
                with open ('cookies','rb')as OOO0OOOOO00O0OO0O :#line:76
                    OO0O0OOO0OOOO00O0 .session .cookies .update (pickle .load (OOO0OOOOO00O0OO0O ))#line:77
            O0O000O0O0O0OOO00 =OO0O0OOO0OOOO00O0 .session .get ('https://m.vk.com/login')#line:79
            OO000OOO00O0000O0 =BS (O0O000O0O0O0OOO00 .content ,'lxml')#line:80
            O00O00OOO0O000000 =OO000OOO00O0000O0 .select ('a[class=op_owner]')#line:81
            if not O00O00OOO0O000000 :#line:82
                logging .info ("Updating cookies! Trying to login.")#line:83
                O000OO0OO000O0000 =OO000OOO00O0000O0 .find ('form')['action']#line:84
                OO0OOO00O000O000O =OO0O0OOO0OOOO00O0 .session .post (O000OO0OO000O0000 ,data ={'email':OO0O0OOO0OOOO00O0 .username ,'pass':OO0O0OOO0OOOO00O0 .password },headers =OO0O0OOO0OOOO00O0 .headers )#line:88
                OO000OOO00O0000O0 =BS (OO0OOO00O000O000O .content ,'lxml')#line:89
                O00O00OOO0O000000 =OO000OOO00O0000O0 .select ('a[class=op_owner]')#line:90
                if not O00O00OOO0O000000 :#line:91
                    raise KeyError #line:92
            else :#line:93
                logging .info ("Logged by cookies!")#line:94
                logging .info ('Successfully login as: %s',O00O00OOO0O000000 [0 ]["data-name"])#line:95
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OO0OO000O0OOO0OO0 :#line:96
            logging .info ('Shit happend. Login fail. %s',OO0OO000O0OOO0OO0 )#line:97
        else :#line:98
            OO0O0OOO0OOOO00O0 .get_token ()#line:99
            with open ('cookies','wb')as OOO0OOOOO00O0OO0O :#line:100
                pickle .dump (OO0O0OOO0OOOO00O0 .session .cookies ,OOO0OOOOO00O0OO0O )#line:101
            return O00O00OOO0O000000 [0 ]["data-name"]#line:102
    def make_repost (O00O0O00O0OOOO00O ,O0OO0OO0OO00OOOO0 ):#line:104
        ""#line:107
        try :#line:108
            logging .info (f'Making report: {O0OO0OO0OO00OOOO0}')#line:109
            O0OOOOOOO00O0OO0O =O00O0O00O0OOOO00O .method ('wall.repost',({'object':O0OO0OO0OO00OOOO0 })).json ()#line:110
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OOOOOOO00000OOO0O :#line:111
            logging .error (OOOOOOO00000OOO0O )#line:112
        else :#line:113
            logging .info (O0OOOOOOO00O0OO0O )#line:114
            if 'response'in O0OOOOOOO00O0OO0O :#line:115
                O00O0O00O0OOOO00O .item_id =O0OOOOOOO00O0OO0O ['response']['post_id']#line:116
            return O0OOOOOOO00O0OO0O #line:117
    def delete_repost (OOOO00O000O0OO00O ):#line:119
        ""#line:122
        try :#line:123
            O0O0OO00000000000 =OOOO00O000O0OO00O .method ('wall.get',({'owner_id':OOOO00O000O0OO00O .user_id })).json ()#line:124
            if 'response'in O0O0OO00000000000 :#line:125
                O0O0OO00000000000 =OOOO00O000O0OO00O .method ('wall.delete',({'owner_id':OOOO00O000O0OO00O .user_id ,'post_id':OOOO00O000O0OO00O .item_id })).json ()#line:128
            logging .info (O0O0OO00000000000 )#line:129
        except (ConnectionError ,RuntimeError ,KeyError )as O00OOO0OO0O0OO000 :#line:130
            logging .error (O00OOO0OO0O0OO000 )#line:131
    def get_user_id_to_ban (O0O0O0O000OOOOOO0 ,O0OOO00OO00000000 ):#line:133
        try :#line:134
            O0O00OOOO000000OO =O0O0O0O000OOOOOO0 .session .get (f"https://vk.com{O0OOO00OO00000000}")#line:135
            OO0000O0OO00O00OO =BS (O0O00OOOO000000OO .text ,'html.parser')#line:136
            O000O00O0OOO00O00 =OO0000O0OO00O00OO .find_all ("a",attrs ={"class":"BtnStack__btn button wide_button acceptFriendBtn Btn Btn_theme_regular"})#line:138
        except Exception as OO0O00O00OO0O0OO0 :#line:139
            logging .error (OO0O00O00OO0O0OO0 )#line:140
        else :#line:141
            return O000O00O0OOO00O00 #line:142
    def get_user_id (OOOO0OOO00O00O00O ):#line:144
        ""#line:147
        O0O0O0000OOO0OOOO =OOOO0OOO00O00O00O .method ('users.get').json ()#line:148
        if 'response'in O0O0O0000OOO0OOOO :#line:149
            OOOO0OOO00O00O00O .user_id =O0O0O0000OOO0OOOO ['response'][0 ]['id']#line:150
            logging .info ("user_id = %s",OOOO0OOO00O00O00O .user_id )#line:151
        return OOOO0OOO00O00O00O .user_id #line:152
    def get_token (O00000OO000O00OO0 ):#line:154
        ""#line:158
        OOOO0O0O0O00O00O0 =2274003 #line:159
        O0OO0O0O0O0O0OOOO ='hHbZxrka2uZ6jB1inYsH'#line:160
        OO0O0OOO000000000 ={}#line:161
        OOOOOOOOOO0OOOOOO =f'https://oauth.vk.com/token?grant_type=password&client_id={OOOO0O0O0O00O00O0}&client_secret={O0OO0O0O0O0O0OOOO}&username={O00000OO000O00OO0.username}&password={O00000OO000O00OO0.password}&v=5.103&2fa_supported=1'#line:163
        try :#line:164
            OO0O0OOO000000000 =requests .get (OOOOOOOOOO0OOOOOO ).json ()#line:165
            O00000OO000O00OO0 .token =OO0O0OOO000000000 ['access_token']#line:166
        except KeyError as O0000OOO00OOO00OO :#line:168
            logging .info ('Didn`t get: %s',O0000OOO00OOO00OO .args [0 ])#line:169
            if 'error'in OO0O0OOO000000000 :#line:170
                logging .info ("Причина: %s",OO0O0OOO000000000 ['error_description'])#line:171
        except ConnectionError as O0000OOO00OOO00OO :#line:172
            logging .error ("Connection error")#line:173
        else :#line:174
            O00000OO000O00OO0 .user_id =O00000OO000O00OO0 .get_user_id ()#line:175
            return O00000OO000O00OO0 .token #line:176
    def login_likest (O000O0OO00OO0OO0O ):#line:178
        ""#line:181
        OO00000O0OO00OOO0 ={}#line:182
        logging .info ('Trying to login to likest')#line:183
        try :#line:184
            OOO00000OO000O00O =O000O0OO00OO0OO0O .session .get ('https://ulogin.ru/auth.php?name=vkontakte')#line:185
            OO00O0O0OOO00OO00 =BS (OOO00000OO000O00O .content ,'lxml')#line:186
            O0O0O0O000OO00000 =OO00O0O0OOO00OO00 .select ('script')#line:187
            O000O000OOOOO0O00 ="token = \'(.+)\'"#line:189
            if O0O0O0O000OO00000 :#line:190
                OO0000OOO00OO0O00 =re .search (O000O000OOOOO0O00 ,str (O0O0O0O000OO00000 )).group (1 )#line:191
                logging .info (f'Likest token: {OO0000OOO00OO0O00}')#line:192
            else :#line:193
                logging .error ("Can`t find <script token=...>")#line:194
            if OO0000OOO00OO0O00 :#line:196
                OO00000O0OO00OOO0 =O000O0OO00OO0OO0O .session .post ('https://likest.ru/user/login-ulogin/token',headers =O000O0OO00OO0OO0O .headers ,data ={'token':OO0000OOO00OO0O00 })#line:200
        except (NameError ,KeyError ,Exception )as OOOOO0O00OO0O0OOO :#line:202
            logging .info ('Failed login likest')#line:203
            logging .error (OOOOO0O00OO0O0OOO )#line:204
        else :#line:205
            logging .info ("Succ logged Likest")#line:206
            return OO00000O0OO00OOO0 .status_code #line:207
    def get_likes_balance (O0O00O0OO0O0O0000 ):#line:209
        ""#line:212
        try :#line:213
            OOO0000OO0OOOO0OO =O0O00O0OO0O0O0000 .session .get (f'http://likest.ru/api/balance.get',headers =O0O00O0OO0O0O0000 .headers ).json ()#line:215
        except (TimeoutError ,ConnectionError ,RuntimeError )as OOO00O00O0O0O0O00 :#line:216
            logging .error (OOO00O00O0O0O0O00 )#line:217
        else :#line:218
            logging .info ('Likest balance %s',OOO0000OO0OOOO0OO )#line:219
            return OOO0000OO0OOOO0OO #line:220
    def activate_coupon (OOO0O00O0OOOOO000 ,OOO00OO0OOOO0OOOO ):#line:222
        ""#line:225
        try :#line:226
            OOO0OOO0OOOO00OO0 =OOO0O00O0OOOOO000 .session .post ('http://likest.ru/api/coupons.use',data ={'coupons':str (OOO00OO0OOOO0OOOO )},headers =OOO0O00O0OOOOO000 .headers ).json ()#line:229
        except (TimeoutError ,ConnectionError ,RuntimeError )as O00OOOOO0000OO0O0 :#line:231
            logging .error (O00OOOOO0000OO0O0 )#line:232
        else :#line:233
            logging .info ('Result %s',OOO0OOO0OOOO00OO0 )#line:234
            return OOO0OOO0OOOO00OO0 #line:235
    def add_likest_task (OO0OO0OOO0000OOOO ,OO00O0O0O0OOO0000 ,OOO0OO0O0O0O00O00 ,OOO0OOOOOOO0OO0O0 ,OO0O00OO0O0000O0O =''):#line:237
        ""#line:241
        OOOOOO0O000O0OOOO ='https://likest.ru/system/ajax'#line:242
        O0OO00000O0OOOO0O =''#line:243
        try :#line:244
            if OOO0OOOOOOO0OO0O0 =='l':#line:245
                O0000000OOO00OOO0 =OO0OO0OOO0000OOOO .session .get ('https://likest.ru/buy-likes',headers =OO0OO0OOO0000OOOO .headers )#line:247
                O0OO00000O0OOOO0O ='hpoints_buy_likes_form'#line:248
                _O0OOOO0OOOO00O0O0 ='Заказать'#line:249
            else :#line:252
                O0000000OOO00OOO0 =OO0OO0OOO0000OOOO .session .get ('https://likest.ru/reposts/add',headers =OO0OO0OOO0000OOOO .headers )#line:254
                O0OO00000O0OOOO0O ='hpoints_reposts_add_form'#line:255
                _O0OOOO0OOOO00O0O0 ='Получить репосты'#line:256
            O0O0OO0O00OO00OOO =BS (O0000000OOO00OOO0 .content ,'lxml')#line:258
            O0000OO00O0OOO000 =O0O0OO0O00OO00OOO .select ('input[name=form_build_id]')#line:259
            O00OOOO00OO0O000O =O0O0OO0O00OO00OOO .select ('input[name=form_token]')#line:260
            O0000OO00O0OOO000 =str (O0000OO00O0OOO000 ).split ('"')[5 ]#line:262
            O00OOOO00OO0O000O =str (O00OOOO00OO0O000O ).split ('"')[5 ]#line:263
            O0O00O0OO0OOOOO0O ={"title":OOO0OO0O0O0O00O00 ,"link":OOO0OO0O0O0O00O00 ,"reward":OO0O00OO0O0000O0O ,"amount":OO00O0O0O0OOO0000 ,"sex":"0","country":"0","age_min":"0","age_max":"255","friends_min":"0","lim_5":"0","lim_30":"0","lim_60":"0","sleepy_factor":"0","form_build_id":O0000OO00O0OOO000 ,"form_token":O00OOOO00OO0O000O ,"form_id":O0OO00000O0OOOO0O ,"_triggering_element_name":"op","_triggering_element_value":_O0OOOO0OOOO00O0O0 }#line:284
            if OOO0OOOOOOO0OO0O0 =='l':#line:286
                OO0OO0OOO0000OOOO .session .head ('https://likest.ru/buy-likes')#line:287
            else :#line:288
                OO0OO0OOO0000OOOO .session .head ('https://likest.ru/reposts/add')#line:289
            O0OO0OO0O0OO0OOO0 =OO0OO0OOO0000OOOO .session .post (OOOOOO0O000O0OOOO ,data =O0O00O0OO0OOOOO0O ,headers =OO0OO0OOO0000OOOO .headers )#line:292
            logging .info (O0OO0OO0O0OO0OOO0 )#line:293
        except (ConnectionError ,TimeoutError ,ValueError ,RuntimeError )as OOOO0O00O0OOOO00O :#line:295
            logging .error (OOOO0O00O0OOOO00O )#line:296
        else :#line:297
            logging .info ('Task added!!!!')#line:298
    def get_likes_list (O00000O0OOOO0000O ):#line:300
        try :#line:301
            OOO0OOO000OO0OOOO ="https://vk.com/wkview.php"#line:302
            O0O00O0O0000000O0 ={"act":"show","al":1 ,"loc":f"wall{O00000O0OOOO0000O.user_id}_{O00000O0OOOO0000O.item_id}","location_owner_id":O00000O0OOOO0000O .user_id ,"w":f"likes/wall{O00000O0OOOO0000O.user_id}_{O00000O0OOOO0000O.item_id}"}#line:309
            O000OO0OOOO00O00O =[]#line:310
            OOOO000OOOOOO0OOO =requests .post (OOO0OOO000OO0OOOO ,O0O00O0O0000000O0 )#line:311
            OOOO000OOOOOO0OOO =OOOO000OOOOOO0OOO .text .replace ("\\","")#line:312
            O0O00O0OOOO00OOO0 =BS (OOOO000OOOOOO0OOO ,'html.parser')#line:313
            for O0000OOO00OOO0OOO in O0O00O0OOOO00OOO0 .find_all ("a",attrs ={"class":"fans_fan_lnk"}):#line:315
                O000OO0OOOO00O00O .append (O0000OOO00OOO0OOO ["href"])#line:316
        except Exception as OOO0O0O00OOO0OO0O :#line:317
            logging .error (OOO0O0O00OOO0OO0O )#line:318
        else :#line:319
            return O000OO0OOOO00O00O #line:320
    def ban_user_report (OO00OOO00000000OO ):#line:322
        ""#line:325
        OO00OOO0O00000000 =[]#line:326
        try :#line:327
            OO00OOO0O00000000 =OO00OOO00000000OO .get_likes_list ()#line:328
        except KeyError as OO0O00OOOO0OO00OO :#line:329
            logging .error (OO0O00OOOO0OO00OO )#line:330
        for O00000OO000OO0O0O in OO00OOO0O00000000 :#line:332
            if "/id"not in O00000OO000OO0O0O :#line:333
                O00000OO000OO0O0O =OO00OOO00000000OO .get_user_id_to_ban (O00000OO000OO0O0O )#line:334
            else :#line:335
                O00000OO000OO0O0O =O00000OO000OO0O0O .replace ("/id","")#line:336
                OOO0OOOO0O0OOO0OO ={'act':'spam','al':'1','mid':O00000OO000OO0O0O ,'object':'wall'+str (OO00OOO00000000OO .user_id )+'_'+str (OO00OOO00000000OO .item_id )}#line:342
                O00000O000O00OO0O =OO00OOO00000000OO .session .post ('https://vk.com/like.php',data =OOO0OOOO0O0OOO0OO )#line:345
                O0OOOO00OO00000O0 =re .findall ('hash: \'(?:[a-zA-Z]|[0-9])+',str (O00000O000O00OO0O .text ))[0 ]#line:346
                O0OOOO00OO00000O0 =O0OOOO00OO00000O0 .replace ('hash: \'','')#line:347
                OOOOO0000OOOO00OO =O0OOOO00OO00000O0 .replace ('"','')#line:348
                OOO0OOOO0O0OOO0OO ={'act':'do_spam','al':'1','hash':OOOOO0000OOOO00OO ,'mid':O00000OO000OO0O0O ,'object':'wall'+str (OO00OOO00000000OO .user_id )+'_'+str (OO00OOO00000000OO .item_id )}#line:356
                OO00OOO00000000OO .session .post ('https://vk.com/like.php',data =OOO0OOOO0O0OOO0OO )#line:359
                OO00OOO00000000OO .banned_users .append (O00000OO000OO0O0O )#line:360
        time .sleep (0.3 )#line:361
    def unban_users (OOOO000O0OO0O0O00 ):#line:363
        OO0O000000O0OO000 =OOOO000O0OO0O0O00 .session .post ('https://vk.com/settings?act=blacklist')#line:364
        OO000O0000OO0O00O =re .findall (f'Settings.delFromBl\((?:[0-9]+), \'(?:[a-zA-Z]|[0-9])+',str (OO0O000000O0OO000 .text ))#line:366
        for O0O0OO0OO0O00O0O0 in OO000O0000OO0O00O :#line:368
            O0O0OO0OO0O00O0O0 =O0O0OO0OO0O00O0O0 .replace (f'Settings.delFromBl(','').replace (" \\","").replace ("'","").replace (" ","").split (",")#line:369
            OO0O0O0000OO0O00O =O0O0OO0OO0O00O0O0 [0 ]#line:370
            O0000O00O0OO00O00 =O0O0OO0OO0O00O0O0 [1 ]#line:371
            O00OOO0OOOOO00O00 ={'act':'a_del_from_bl','al':'1','from':'settings','hash':O0000O00O0OO00O00 ,'id':OO0O0O0000OO0O00O }#line:379
            print (O00OOO0OOOOO00O00 )#line:380
            OOOO000O0OO0O0O00 .session .post ('https://vk.com/al_settings.php',data =O00OOO0OOOOO00O00 )#line:382
    def ban_users (O00OO0OO000OO0OOO ):#line:384
        ""#line:387
        OOOO00OO0O0000O0O =[]#line:388
        try :#line:389
            OO0O00O0OO0OO0OO0 =O00OO0OO000OO0OOO .method ('likes.getList',({'owner_id':O00OO0OO000OO0OOO .user_id ,'item_id':O00OO0OO000OO0OOO .item_id ,'type':'post'})).json ()#line:394
            logging .info (OO0O00O0OO0OO0OO0 )#line:396
            if 'response'in OO0O00O0OO0OO0OO0 :#line:397
                if OO0O00O0OO0OO0OO0 ['response']['count']!=0 :#line:398
                    logging .info (OO0O00O0OO0OO0OO0 )#line:399
                    OOOO00OO0O0000O0O =OO0O00O0OO0OO0OO0 ['response']['items']#line:400
            elif 'error'in OO0O00O0OO0OO0OO0 :#line:401
                return OO0O00O0OO0OO0OO0 #line:402
        except KeyError as O00O0000OO0OOO0O0 :#line:404
            logging .error (O00O0000OO0OOO0O0 )#line:405
            logging .error (OO0O00O0OO0OO0OO0 )#line:406
        for OOO0OO0O00OOO0OOO in OOOO00OO0O0000O0O :#line:408
            O00OO0OOO0O0OO0O0 ={'act':'spam','al':'1','mid':OOO0OO0O00OOO0OOO ,'object':'wall'+str (O00OO0OO000OO0OOO .user_id )+'_'+str (O00OO0OO000OO0OOO .item_id )}#line:414
            O00OO0OO0O0O0OO00 =O00OO0OO000OO0OOO .session .post ('https://vk.com/like.php',data =O00OO0OOO0O0OO0O0 )#line:417
            O000000O0O00000O0 =re .findall ('hash: \'(?:[a-zA-Z]|[0-9])+',str (O00OO0OO0O0O0OO00 .text ))[0 ]#line:418
            O000000O0O00000O0 =O000000O0O00000O0 .replace ('hash: \'','')#line:419
            O0OO0O0O0000OO000 =O000000O0O00000O0 .replace ('"','')#line:420
            O00OO0OOO0O0OO0O0 ={'act':'do_spam','al':'1','hash':O0OO0O0O0000OO000 ,'mid':OOO0OO0O00OOO0OOO ,'object':'wall'+str (O00OO0OO000OO0OOO .user_id )+'_'+str (O00OO0OO000OO0OOO .item_id )}#line:428
            O00OO0OO000OO0OOO .session .post ('https://vk.com/like.php',data =O00OO0OOO0O0OO0O0 )#line:431
        for OOO0OO0O00OOO0OOO in OOOO00OO0O0000O0O :#line:433
            O00OO0OO0O0O0OO00 =requests .get ('https://api.vk.com/method/account.unban?access_token={self.token}&owner_id={user}&v=5.103').json ()#line:434
            logging .info (O00OO0OO0O0O0OO00 )#line:435
            time .sleep (0.6 )#line:436
        time .sleep (1 )#line:437
        OOOO00OO0O0000O0O =[]#line:438
    def get_data_from_link (OO0OO0OO0OO0O0O0O ,O0OO0OOOO0O00OOOO ):#line:440
        ""#line:443
        try :#line:444
            OO00OOOOOOO00O000 =(re .findall ('wall-?(.+)_(\\d+)',O0OO0OOOO0O00OOOO ))#line:445
            if not OO00OOOOOOO00O000 :#line:446
                raise IndexError #line:447
        except IndexError as O0000OO000O0000OO :#line:448
            logging .error ("Invalid url! %s",O0000OO000O0000OO )#line:449
        else :#line:450
            OO0OO0OO0OO0O0O0O .item_id =OO00OOOOOOO00O000 [0 ][1 ]#line:451
            return OO00OOOOOOO00O000 [0 ]#line:452
def save_data_to_file (**OOO000OOOOO0O000O ):#line:455
    ""#line:459
    try :#line:460
        OO0OO00OOO000O0O0 ={}#line:461
        with open ('data.txt','r+')as OO0O00OO0000O0000 :#line:462
            OO0OO00OOO000O0O0 =json .load (OO0O00OO0000O0000 )#line:463
        for O00O0O0OOOOOO0OOO in OOO000OOOOO0O000O :#line:465
            OO0OO00OOO000O0O0 [O00O0O0OOOOOO0OOO ]=OOO000OOOOO0O000O [O00O0O0OOOOOO0OOO ]#line:466
        with open ('data.txt','w+')as OO0O00OO0000O0000 :#line:468
            json .dump (OO0OO00OOO000O0O0 ,OO0O00OO0000O0000 )#line:469
        return OO0OO00OOO000O0O0 #line:471
    except KeyError as OOOOOOOOO0O0O00O0 :#line:472
        if OOOOOOOOO0O0O00O0 .args [0 ]in ['link','login','password','token']:#line:473
            logging .info ('Cannot find: %s',OOOOOOOOO0O0O00O0 .args [0 ])#line:474
    except IOError as OOOOOOOOO0O0O00O0 :#line:476
        logging .info (OOOOOOOOO0O0O00O0 )#line:477
def load_data_from_file ():#line:480
    ""#line:484
    O0OO000O00OO00O0O ={}#line:485
    try :#line:486
        if not os .path .exists ('data.txt'):#line:487
            with open ('data.txt','w')as OO000OO000OO00O0O :#line:488
                OO000OO000OO00O0O .write ('{}')#line:489
        with open ('data.txt')as O000000OO00OO0O0O :#line:491
            OO0000OO00O00O00O =json .load (O000000OO00OO0O0O )#line:492
        if 'login'in OO0000OO00O00O00O :#line:494
            O0OO000O00OO00O0O ['login']=OO0000OO00O00O00O ['login']#line:495
        if 'password'in OO0000OO00O00O00O :#line:496
            O0OO000O00OO00O0O ['password']=OO0000OO00O00O00O ['password']#line:497
        if 'token'in OO0000OO00O00O00O :#line:498
            O0OO000O00OO00O0O ['token']=OO0000OO00O00O00O ['token']#line:499
        if 'url'in OO0000OO00O00O00O :#line:500
            O0OO000O00OO00O0O ['url']=OO0000OO00O00O00O ['url']#line:501
        if 'user_id'in OO0000OO00O00O00O :#line:502
            O0OO000O00OO00O0O ['user_id']=OO0000OO00O00O00O ['user_id']#line:503
    except KeyError as O0OOOO0OOOO0O0O0O :#line:505
        if O0OOOO0OOOO0O0O0O .args [0 ]in ['link','login','password','token']:#line:506
            logging .error ('Cannot find: %s',O0OOOO0OOOO0O0O0O .args [0 ])#line:507
    except Exception as O0OOOO0OOOO0O0O0O :#line:508
        raise O0OOOO0OOOO0O0O0O #line:509
    else :#line:510
        return O0OO000O00OO00O0O #line:511
