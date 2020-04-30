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
    def __init__ (O000O0O000OO00OOO ,O00000OO0O000OOO0 ,OOOO0000O0OO0O000 ):#line:28
        O000O0O000OO00OOO .username =O00000OO0O000OOO0 #line:29
        O000O0O000OO00OOO .password =OOOO0000O0OO0O000 #line:30
        O000O0O000OO00OOO .banned_users =[]#line:31
        O000O0O000OO00OOO .token =None #line:32
        O000O0O000OO00OOO .session =requests .Session ()#line:33
        O000O0O000OO00OOO .headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64)' ' AppleWebKit/537.36 (KHTML, like Gecko)' ' Chrome/79.0.3945.130 Safari/537.36','Accept':'*/*','Accept-Language':'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7','Accept-Encoding':'gzip, deflate, br','Connection':'keep-alive'}#line:42
        O000O0O000OO00OOO .item_id =None #line:44
        O000O0O000OO00OOO .user_id =None #line:45
    def method (O0OO0OO000OOO000O ,O0OOO00O0O000OOO0 ,values =None ):#line:47
        ""#line:52
        try :#line:53
            if values is None :#line:54
                values ={}#line:55
            values ['v']='5.103'#line:56
            if O0OO0OO000OOO000O .token :#line:57
                values ['access_token']=O0OO0OO000OOO000O .token #line:58
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OOOO00O0OO000OO00 :#line:60
            logging .error (OOOO00O0OO000OO00 )#line:61
        else :#line:62
            return O0OO0OO000OOO000O .session .post ('https://api.vk.com/method/'+O0OOO00O0O000OOO0 ,values )#line:66
    def login (OOO00O0O0O00OO000 ):#line:68
        ""#line:73
        try :#line:74
            if os .path .isfile ("cookies"):#line:75
                with open ('cookies','rb')as O000O0OOOO0O0000O :#line:76
                    OOO00O0O0O00OO000 .session .cookies .update (pickle .load (O000O0OOOO0O0000O ))#line:77
            OO000O00OO000O0OO =OOO00O0O0O00OO000 .session .get ('https://m.vk.com/login')#line:79
            OO0O0OOO000OOO00O =BS (OO000O00OO000O0OO .content ,'lxml')#line:80
            OOO0O0OOO000OOOO0 =OO0O0OOO000OOO00O .select ('a[class=op_owner]')#line:81
            if not OOO0O0OOO000OOOO0 :#line:82
                logging .info ("Updating cookies! Trying to login.")#line:83
                O00O0OO000OOO0000 =OO0O0OOO000OOO00O .find ('form')['action']#line:84
                OOO0O00O0OO0OO0O0 =OOO00O0O0O00OO000 .session .post (O00O0OO000OOO0000 ,data ={'email':OOO00O0O0O00OO000 .username ,'pass':OOO00O0O0O00OO000 .password },headers =OOO00O0O0O00OO000 .headers )#line:88
                OO0O0OOO000OOO00O =BS (OOO0O00O0OO0OO0O0 .content ,'lxml')#line:89
                OOO0O0OOO000OOOO0 =OO0O0OOO000OOO00O .select ('a[class=op_owner]')#line:90
                if not OOO0O0OOO000OOOO0 :#line:91
                    raise KeyError #line:92
            else :#line:93
                logging .info ("Logged by cookies!")#line:94
                logging .info ('Successfully login as: %s',OOO0O0OOO000OOOO0 [0 ]["data-name"])#line:95
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OO0OOO00OOOOOOO0O :#line:96
            logging .info ('Shit happend. Login fail. %s',OO0OOO00OOOOOOO0O )#line:97
        else :#line:98
            OOO00O0O0O00OO000 .get_token ()#line:99
            with open ('cookies','wb')as O000O0OOOO0O0000O :#line:100
                pickle .dump (OOO00O0O0O00OO000 .session .cookies ,O000O0OOOO0O0000O )#line:101
            return OOO0O0OOO000OOOO0 [0 ]["data-name"]#line:102
    def make_repost (OO0OOOO000OOO0OOO ,O0O00O00000000O00 ):#line:104
        ""#line:107
        try :#line:108
            logging .info (f'Making report: {O0O00O00000000O00}')#line:109
            O0000O0OOO0OOO000 =OO0OOOO000OOO0OOO .method ('wall.repost',({'object':O0O00O00000000O00 })).json ()#line:110
        except (TimeoutError ,ConnectionError ,RuntimeError ,KeyError )as OO00OO00O0O00O00O :#line:111
            logging .error (OO00OO00O0O00O00O )#line:112
        else :#line:113
            logging .info (O0000O0OOO0OOO000 )#line:114
            if 'response'in O0000O0OOO0OOO000 :#line:115
                OO0OOOO000OOO0OOO .item_id =O0000O0OOO0OOO000 ['response']['post_id']#line:116
            return O0000O0OOO0OOO000 #line:117
    def delete_repost (OO0000O0OO0OOO00O ):#line:119
        ""#line:122
        try :#line:123
            O00O0000O00O0O0OO =OO0000O0OO0OOO00O .method ('wall.get',({'owner_id':OO0000O0OO0OOO00O .user_id })).json ()#line:124
            if 'response'in O00O0000O00O0O0OO :#line:125
                O00O0000O00O0O0OO =OO0000O0OO0OOO00O .method ('wall.delete',({'owner_id':OO0000O0OO0OOO00O .user_id ,'post_id':OO0000O0OO0OOO00O .item_id })).json ()#line:128
            logging .info (O00O0000O00O0O0OO )#line:129
        except (ConnectionError ,RuntimeError ,KeyError )as O00000OO0OO0O0OO0 :#line:130
            logging .error (O00000OO0OO0O0OO0 )#line:131
    def get_user_id_to_ban (O00OO0OOOO0O0OO0O ,OO0O000O000O0OOO0 ):#line:133
        OO0O000OOO0O00OO0 =None #line:134
        try :#line:135
            OO0O000O000O0OOO0 .replace ("/","")#line:136
            O00000O00O0OOOOO0 =O00OO0OOOO0O0OO0O .session .get (f"https://vk.com/{OO0O000O000O0OOO0}")#line:137
            OO00OO00000O00O0O =BS (O00000O00O0OOOOO0 .text ,'html.parser')#line:139
            for O0O0000O00OO0O0O0 in OO00OO00000O00O0O .find_all ("a",attrs ={"class":"BtnStack__btn button wide_button acceptFriendBtn Btn Btn_theme_regular"}):#line:141
                OO0O000OOO0O00OO0 =O0O0000O00OO0O0O0 ['data-uid']#line:142
                break #line:143
            if OO0O000OOO0O00OO0 is None :#line:147
                OO0O000OOO0O00OO0 =O00OO0OOOO0O0OO0O .method ('users.get',({'user_ids':OO0O000O000O0OOO0 })).json ()#line:148
                OO0O000OOO0O00OO0 =OO0O000OOO0O00OO0 ['response']['id']#line:149
        except Exception as O00OOO0OO0OO000OO :#line:150
            logging .error (O00OOO0OO0OO000OO )#line:151
        else :#line:152
            return OO0O000OOO0O00OO0 #line:153
    def get_user_id (OO00O00OOOOOO0O0O ):#line:155
        ""#line:158
        O0000OO0OOO00OOOO =OO00O00OOOOOO0O0O .method ('users.get').json ()#line:159
        if 'response'in O0000OO0OOO00OOOO :#line:160
            OO00O00OOOOOO0O0O .user_id =O0000OO0OOO00OOOO ['response'][0 ]['id']#line:161
            logging .info ("user_id = %s",OO00O00OOOOOO0O0O .user_id )#line:162
        return OO00O00OOOOOO0O0O .user_id #line:163
    def get_token (O0OO00O00OOOO0OO0 ):#line:165
        ""#line:169
        O00000O000O000O0O =2274003 #line:170
        OO0OOO0O0000OOO0O ='hHbZxrka2uZ6jB1inYsH'#line:171
        OOO0OO0O00OO0O00O ={}#line:172
        OOO00O00000OOO000 =f'https://oauth.vk.com/token?grant_type=password&client_id={O00000O000O000O0O}&client_secret={OO0OOO0O0000OOO0O}&username={O0OO00O00OOOO0OO0.username}&password={O0OO00O00OOOO0OO0.password}&v=5.103&2fa_supported=1'#line:174
        try :#line:175
            OOO0OO0O00OO0O00O =requests .get (OOO00O00000OOO000 ).json ()#line:176
            O0OO00O00OOOO0OO0 .token =OOO0OO0O00OO0O00O ['access_token']#line:177
        except KeyError as O0OOOO00O0O0000OO :#line:179
            logging .info ('Didn`t get: %s',O0OOOO00O0O0000OO .args [0 ])#line:180
            if 'error'in OOO0OO0O00OO0O00O :#line:181
                logging .info ("Причина: %s",OOO0OO0O00OO0O00O ['error_description'])#line:182
        except ConnectionError as O0OOOO00O0O0000OO :#line:183
            logging .error ("Connection error")#line:184
        else :#line:185
            O0OO00O00OOOO0OO0 .user_id =O0OO00O00OOOO0OO0 .get_user_id ()#line:186
            return O0OO00O00OOOO0OO0 .token #line:187
    def login_likest (O000OOO000O00OO00 ):#line:189
        ""#line:192
        OOO0OOOOOO0O00O00 ={}#line:193
        logging .info ('Trying to login to likest')#line:194
        try :#line:195
            OOO0000000OOOO0OO =O000OOO000O00OO00 .session .get ('https://ulogin.ru/auth.php?name=vkontakte')#line:196
            OOOO00OOO00O0OOOO =BS (OOO0000000OOOO0OO .content ,'lxml')#line:197
            OO0O0O0O0000OOOOO =OOOO00OOO00O0OOOO .select ('script')#line:198
            O0000O0O000OO00OO ="token = \'(.+)\'"#line:200
            if OO0O0O0O0000OOOOO :#line:201
                OO00O00OO0O0OOOO0 =re .search (O0000O0O000OO00OO ,str (OO0O0O0O0000OOOOO )).group (1 )#line:202
                logging .info (f'Likest token: {OO00O00OO0O0OOOO0}')#line:203
            else :#line:204
                logging .error ("Can`t find <script token=...>")#line:205
            if OO00O00OO0O0OOOO0 :#line:207
                OOO0OOOOOO0O00O00 =O000OOO000O00OO00 .session .post ('https://likest.ru/user/login-ulogin/token',headers =O000OOO000O00OO00 .headers ,data ={'token':OO00O00OO0O0OOOO0 })#line:211
        except (NameError ,KeyError ,Exception )as OOO00O000OOOO00OO :#line:213
            logging .info ('Failed login likest')#line:214
            logging .error (OOO00O000OOOO00OO )#line:215
        else :#line:216
            logging .info ("Succ logged Likest")#line:217
            return OOO0OOOOOO0O00O00 .status_code #line:218
    def get_likes_balance (O0OO0O00O0O0OOO0O ):#line:220
        ""#line:223
        try :#line:224
            OOOOO0000O0OO000O =O0OO0O00O0O0OOO0O .session .get (f'http://likest.ru/api/balance.get',headers =O0OO0O00O0O0OOO0O .headers ).json ()#line:226
        except (TimeoutError ,ConnectionError ,RuntimeError )as OO00OOO0OO0O00000 :#line:227
            logging .error (OO00OOO0OO0O00000 )#line:228
        else :#line:229
            logging .info ('Likest balance %s',OOOOO0000O0OO000O )#line:230
            return OOOOO0000O0OO000O #line:231
    def activate_coupon (OOO0OO0OOOOOO000O ,OOO0OOO0O0OO000O0 ):#line:233
        ""#line:236
        try :#line:237
            O0OOO0O0OO0O00OO0 =OOO0OO0OOOOOO000O .session .post ('http://likest.ru/api/coupons.use',data ={'coupons':str (OOO0OOO0O0OO000O0 )},headers =OOO0OO0OOOOOO000O .headers ).json ()#line:240
        except (TimeoutError ,ConnectionError ,RuntimeError )as OO0000OO00OO00OO0 :#line:242
            logging .error (OO0000OO00OO00OO0 )#line:243
        else :#line:244
            logging .info ('Result %s',O0OOO0O0OO0O00OO0 )#line:245
            return O0OOO0O0OO0O00OO0 #line:246
    def add_likest_task (OOOO00OO00OOO00O0 ,O00O000O00O0OO0OO ,O00OOOO0O00OOO00O ,O0OOO0OOOOOO000OO ,reward =''):#line:248
        ""#line:252
        O00OOO0O000O0OOOO ='https://likest.ru/system/ajax'#line:253
        O0O0OOOO0O00O00O0 =''#line:254
        try :#line:255
            if O0OOO0OOOOOO000OO =='l':#line:256
                OOOO00OOO0O0O00OO =OOOO00OO00OOO00O0 .session .get ('https://likest.ru/buy-likes',headers =OOOO00OO00OOO00O0 .headers )#line:258
                O0O0OOOO0O00O00O0 ='hpoints_buy_likes_form'#line:259
                _OO0OOOO0O0OOOOO00 ='Заказать'#line:260
            else :#line:263
                OOOO00OOO0O0O00OO =OOOO00OO00OOO00O0 .session .get ('https://likest.ru/reposts/add',headers =OOOO00OO00OOO00O0 .headers )#line:265
                O0O0OOOO0O00O00O0 ='hpoints_reposts_add_form'#line:266
                _OO0OOOO0O0OOOOO00 ='Получить репосты'#line:267
            O00O00O0OO0O00OOO =BS (OOOO00OOO0O0O00OO .content ,'lxml')#line:269
            O0O00OOOO000OOO00 =O00O00O0OO0O00OOO .select ('input[name=form_build_id]')#line:270
            O000O0OOO0O0O0OOO =O00O00O0OO0O00OOO .select ('input[name=form_token]')#line:271
            O0O00OOOO000OOO00 =str (O0O00OOOO000OOO00 ).split ('"')[5 ]#line:273
            O000O0OOO0O0O0OOO =str (O000O0OOO0O0O0OOO ).split ('"')[5 ]#line:274
            OO00O0O000O00O000 ={"title":O00OOOO0O00OOO00O ,"link":O00OOOO0O00OOO00O ,"reward":reward ,"amount":O00O000O00O0OO0OO ,"sex":"0","country":"0","age_min":"0","age_max":"255","friends_min":"0","lim_5":"0","lim_30":"0","lim_60":"0","sleepy_factor":"0","form_build_id":O0O00OOOO000OOO00 ,"form_token":O000O0OOO0O0O0OOO ,"form_id":O0O0OOOO0O00O00O0 ,"_triggering_element_name":"op","_triggering_element_value":_OO0OOOO0O0OOOOO00 }#line:295
            if O0OOO0OOOOOO000OO =='l':#line:297
                OOOO00OO00OOO00O0 .session .head ('https://likest.ru/buy-likes')#line:298
            else :#line:299
                OOOO00OO00OOO00O0 .session .head ('https://likest.ru/reposts/add')#line:300
            OOOOO0OO0O0O000O0 =OOOO00OO00OOO00O0 .session .post (O00OOO0O000O0OOOO ,data =OO00O0O000O00O000 ,headers =OOOO00OO00OOO00O0 .headers )#line:303
            logging .info (OOOOO0OO0O0O000O0 )#line:304
        except (ConnectionError ,TimeoutError ,ValueError ,RuntimeError )as OO0OO0OO0OO0O0O0O :#line:306
            logging .error (OO0OO0OO0OO0O0O0O )#line:307
        else :#line:308
            logging .info ('Task added!!!!')#line:309
    def get_likes_list (O0O0OO00O00OO0000 ):#line:311
        try :#line:312
            O000O00O0OOO0O0OO ="https://vk.com/wkview.php"#line:313
            OOO0O0O0OO0O00OOO ={"act":"show","al":1 ,"loc":f"wall{O0O0OO00O00OO0000.user_id}_{O0O0OO00O00OO0000.item_id}","location_owner_id":O0O0OO00O00OO0000 .user_id ,"w":f"likes/wall{O0O0OO00O00OO0000.user_id}_{O0O0OO00O00OO0000.item_id}"}#line:320
            OO0O0O0O0000OOOO0 =[]#line:321
            OOO0O00O000OO0O00 =requests .post (O000O00O0OOO0O0OO ,OOO0O0O0OO0O00OOO )#line:322
            OOO0O00O000OO0O00 =OOO0O00O000OO0O00 .text .replace ("\\","")#line:323
            O0O0O0O000OO000OO =BS (OOO0O00O000OO0O00 ,'html.parser')#line:324
            for O0000OO000O000000 in O0O0O0O000OO000OO .find_all ("a",attrs ={"class":"fans_fan_lnk"}):#line:326
                OO0O0O0O0000OOOO0 .append (O0000OO000O000000 ["href"])#line:327
        except Exception as OOOO00OOOO00O00O0 :#line:328
            logging .error (OOOO00OOOO00O00O0 )#line:329
        else :#line:330
            return OO0O0O0O0000OOOO0 #line:331
    def ban_user_report (O00O0O000OOO0OO0O ):#line:333
        ""#line:336
        O0OO0O0O00O0OO00O =[]#line:337
        try :#line:338
            O0OO0O0O00O0OO00O =O00O0O000OOO0OO0O .get_likes_list ()#line:339
        except KeyError as O0OO0000OOOOOOOOO :#line:340
            logging .error (O0OO0000OOOOOOOOO )#line:341
        for OOO00OO0O0000OO0O in O0OO0O0O00O0OO00O :#line:343
            if "/id"not in OOO00OO0O0000OO0O :#line:344
                OOO00OO0O0000OO0O =O00O0O000OOO0OO0O .get_user_id_to_ban (OOO00OO0O0000OO0O )#line:345
            OOO00OO0O0000OO0O =OOO00OO0O0000OO0O .replace ("/id","")#line:346
            OOOO0O0O000O0O0O0 ={'act':'spam','al':'1','mid':OOO00OO0O0000OO0O ,'object':'wall'+str (O00O0O000OOO0OO0O .user_id )+'_'+str (O00O0O000OOO0OO0O .item_id )}#line:352
            OOOO000O00OOOOOOO =O00O0O000OOO0OO0O .session .post ('https://vk.com/like.php',data =OOOO0O0O000O0O0O0 )#line:355
            O0OOOO0O0OO00O0OO =re .findall ('hash: \'(?:[a-zA-Z]|[0-9])+',str (OOOO000O00OOOOOOO .text ))[0 ]#line:356
            O0OOOO0O0OO00O0OO =O0OOOO0O0OO00O0OO .replace ('hash: \'','')#line:357
            O0O0OO0OO0O00OO0O =O0OOOO0O0OO00O0OO .replace ('"','')#line:358
            OOOO0O0O000O0O0O0 ={'act':'do_spam','al':'1','hash':O0O0OO0OO0O00OO0O ,'mid':OOO00OO0O0000OO0O ,'object':'wall'+str (O00O0O000OOO0OO0O .user_id )+'_'+str (O00O0O000OOO0OO0O .item_id )}#line:366
            O00O0O000OOO0OO0O .session .post ('https://vk.com/like.php',data =OOOO0O0O000O0O0O0 )#line:369
            O00O0O000OOO0OO0O .banned_users .append (OOO00OO0O0000OO0O )#line:370
        time .sleep (0.1 )#line:371
    def unban_users (OOO0O00000O0O0O0O ):#line:373
        O0OO0OO00000OO000 =OOO0O00000O0O0O0O .session .post ('https://vk.com/settings?act=blacklist')#line:374
        O0O0OO0OOO000OOOO =re .findall (f'Settings.delFromBl\((?:[0-9]+), \'(?:[a-zA-Z]|[0-9])+',str (O0OO0OO00000OO000 .text ))#line:376
        for O0OOO00O0OOO0000O in O0O0OO0OOO000OOOO :#line:378
            O0OOO00O0OOO0000O =O0OOO00O0OOO0000O .replace (f'Settings.delFromBl(','').replace (" \\","").replace ("'","").replace (" ","").split (",")#line:379
            OO000O00OOOOOOOOO =O0OOO00O0OOO0000O [0 ]#line:380
            OO000O0000OO00OOO =O0OOO00O0OOO0000O [1 ]#line:381
            O0OO0OOOO000000O0 ={'act':'a_del_from_bl','al':'1','from':'settings','hash':OO000O0000OO00OOO ,'id':OO000O00OOOOOOOOO }#line:389
            print (O0OO0OOOO000000O0 )#line:390
            OOO0O00000O0O0O0O .session .post ('https://vk.com/al_settings.php',data =O0OO0OOOO000000O0 )#line:392
    def ban_users (O0OO00000O0OOO0O0 ):#line:394
        ""#line:397
        OOOO000O0OOOO00OO =[]#line:398
        try :#line:399
            OO0O0OOOO000OO0OO =O0OO00000O0OOO0O0 .method ('likes.getList',({'owner_id':O0OO00000O0OOO0O0 .user_id ,'item_id':O0OO00000O0OOO0O0 .item_id ,'type':'post'})).json ()#line:404
            logging .info (OO0O0OOOO000OO0OO )#line:406
            if 'response'in OO0O0OOOO000OO0OO :#line:407
                if OO0O0OOOO000OO0OO ['response']['count']!=0 :#line:408
                    logging .info (OO0O0OOOO000OO0OO )#line:409
                    OOOO000O0OOOO00OO =OO0O0OOOO000OO0OO ['response']['items']#line:410
            elif 'error'in OO0O0OOOO000OO0OO :#line:411
                return OO0O0OOOO000OO0OO #line:412
        except KeyError as OO0O00OOO000O000O :#line:414
            logging .error (OO0O00OOO000O000O )#line:415
            logging .error (OO0O0OOOO000OO0OO )#line:416
        for O00O000O0OOOOOO00 in OOOO000O0OOOO00OO :#line:418
            O0OOOOO000O0OOOOO ={'act':'spam','al':'1','mid':O00O000O0OOOOOO00 ,'object':'wall'+str (O0OO00000O0OOO0O0 .user_id )+'_'+str (O0OO00000O0OOO0O0 .item_id )}#line:424
            O00OO00OOOO0OO00O =O0OO00000O0OOO0O0 .session .post ('https://vk.com/like.php',data =O0OOOOO000O0OOOOO )#line:427
            O0OO00000OOOO00OO =re .findall ('hash: \'(?:[a-zA-Z]|[0-9])+',str (O00OO00OOOO0OO00O .text ))[0 ]#line:428
            O0OO00000OOOO00OO =O0OO00000OOOO00OO .replace ('hash: \'','')#line:429
            O000O0OO0OOO0O00O =O0OO00000OOOO00OO .replace ('"','')#line:430
            O0OOOOO000O0OOOOO ={'act':'do_spam','al':'1','hash':O000O0OO0OOO0O00O ,'mid':O00O000O0OOOOOO00 ,'object':'wall'+str (O0OO00000O0OOO0O0 .user_id )+'_'+str (O0OO00000O0OOO0O0 .item_id )}#line:438
            O0OO00000O0OOO0O0 .session .post ('https://vk.com/like.php',data =O0OOOOO000O0OOOOO )#line:441
        for O00O000O0OOOOOO00 in OOOO000O0OOOO00OO :#line:443
            O00OO00OOOO0OO00O =requests .get ('https://api.vk.com/method/account.unban?access_token={self.token}&owner_id={user}&v=5.103').json ()#line:444
            logging .info (O00OO00OOOO0OO00O )#line:445
            time .sleep (0.6 )#line:446
        time .sleep (1 )#line:447
        OOOO000O0OOOO00OO =[]#line:448
    def get_data_from_link (OO0OOO00OO00OOOOO ,OOOO0OOO0000OOO00 ):#line:450
        ""#line:453
        try :#line:454
            O0OOOOO0O00OO0O00 =(re .findall ('wall-?(.+)_(\\d+)',OOOO0OOO0000OOO00 ))#line:455
            if not O0OOOOO0O00OO0O00 :#line:456
                raise IndexError #line:457
        except IndexError as O0O0O0000OO0OOO00 :#line:458
            logging .error ("Invalid url! %s",O0O0O0000OO0OOO00 )#line:459
        else :#line:460
            OO0OOO00OO00OOOOO .item_id =O0OOOOO0O00OO0O00 [0 ][1 ]#line:461
            return O0OOOOO0O00OO0O00 [0 ]#line:462
def save_data_to_file (**O000000000O00O00O ):#line:465
    ""#line:469
    try :#line:470
        OO000OOOO0000OO0O ={}#line:471
        with open ('data.txt','r+')as O0O0O0O00O0O00O00 :#line:472
            OO000OOOO0000OO0O =json .load (O0O0O0O00O0O00O00 )#line:473
        for O0O00O00000OO00O0 in O000000000O00O00O :#line:475
            OO000OOOO0000OO0O [O0O00O00000OO00O0 ]=O000000000O00O00O [O0O00O00000OO00O0 ]#line:476
        with open ('data.txt','w+')as O0O0O0O00O0O00O00 :#line:478
            json .dump (OO000OOOO0000OO0O ,O0O0O0O00O0O00O00 )#line:479
        return OO000OOOO0000OO0O #line:481
    except KeyError as OOO0OOO0O0O000O00 :#line:482
        if OOO0OOO0O0O000O00 .args [0 ]in ['link','login','password','token']:#line:483
            logging .info ('Cannot find: %s',OOO0OOO0O0O000O00 .args [0 ])#line:484
    except IOError as OOO0OOO0O0O000O00 :#line:486
        logging .info (OOO0OOO0O0O000O00 )#line:487
def load_data_from_file ():#line:490
    ""#line:494
    OOO00OOOOOO00OO0O ={}#line:495
    try :#line:496
        if not os .path .exists ('data.txt'):#line:497
            with open ('data.txt','w')as O000OO00OOOO000OO :#line:498
                O000OO00OOOO000OO .write ('{}')#line:499
        with open ('data.txt')as O00OO00OOOOOO0O00 :#line:501
            OO000OO0OO000O00O =json .load (O00OO00OOOOOO0O00 )#line:502
        if 'login'in OO000OO0OO000O00O :#line:504
            OOO00OOOOOO00OO0O ['login']=OO000OO0OO000O00O ['login']#line:505
        if 'password'in OO000OO0OO000O00O :#line:506
            OOO00OOOOOO00OO0O ['password']=OO000OO0OO000O00O ['password']#line:507
        if 'token'in OO000OO0OO000O00O :#line:508
            OOO00OOOOOO00OO0O ['token']=OO000OO0OO000O00O ['token']#line:509
        if 'url'in OO000OO0OO000O00O :#line:510
            OOO00OOOOOO00OO0O ['url']=OO000OO0OO000O00O ['url']#line:511
        if 'user_id'in OO000OO0OO000O00O :#line:512
            OOO00OOOOOO00OO0O ['user_id']=OO000OO0OO000O00O ['user_id']#line:513
    except KeyError as O0O0OOO00O0OO0OOO :#line:515
        if O0O0OOO00O0OO0OOO .args [0 ]in ['link','login','password','token']:#line:516
            logging .error ('Cannot find: %s',O0O0OOO00O0OO0OOO .args [0 ])#line:517
    except Exception as O0O0OOO00O0OO0OOO :#line:518
        raise O0O0OOO00O0OO0OOO #line:519
    else :#line:520
        return OOO00OOOOOO00OO0O #line:521
