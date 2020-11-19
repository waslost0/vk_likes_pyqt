import json
import logging
import multiprocessing
import os
import pickle
import re
import time


import requests
from bs4 import BeautifulSoup as BS

with open('mylog.log', 'w') as f:
    f.writelines('')

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-2s]# %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'mylog.log')


# logging.getLogger("getmac").setLevel(logging.WARNING)


class User:
    """User class."""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.banned_users = []
        self.token = None
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/79.0.3945.130 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        self.item_id = None
        self.user_id = None
        self.is_group = False

    def method(self, method, values=None):
        """
           Vk method.

           Example: self.method('wall.get', ({'owner_id': self.user_id}))
        """
        try:
            if values is None:
                values = {}
            values['v'] = '5.103'
            if self.token:
                values['access_token'] = self.token

        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            logging.error(error)
        else:
            return self.session.post(
                'https://api.vk.com/method/' + method,
                values
            )

    def login(self):
        """
            Login and save cookies.
            Login vk by username:password or cookies.
            On succ login return Username
        """
        try:
            if os.path.isfile("cookies"):
                with open('cookies', 'rb') as file:
                    self.session.cookies.update(pickle.load(file))

            page = self.session.get('https://m.vk.com/login')
            soup = BS(page.content, 'lxml')
            user_name = soup.select('a[class=op_owner]')
            if not user_name:
                logging.info("Updating cookies! Trying to login.")
                url = soup.find('form')['action']
                response = self.session.post(url,
                                             data={'email': self.username,
                                                   'pass': self.password},
                                             headers=self.headers)
                soup = BS(response.content, 'lxml')
                user_name = soup.select('a[class=op_owner]')
                if not user_name:
                    raise KeyError
            else:
                logging.info("Logged by cookies!")
                logging.info('Successfully login as: %s', user_name[0]["data-name"])
        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            logging.error('Shit happend. Login fail. %s', error)
        else:
            self.get_token()
            with open('cookies', 'wb') as file:
                pickle.dump(self.session.cookies, file)
            return user_name[0]["data-name"]

    def make_repost(self, repost_url):
        """
           Make post report by url.
        """
        try:
            logging.info(f'Making report: {repost_url}')
            response = self.method('wall.repost', ({'object': repost_url})).json()
        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            logging.error(error)
        else:
            logging.info(response)
            if 'response' in response:
                self.item_id = response['response']['post_id']
            return response

    def delete_repost(self):
        """
           Delete just last vk post.
        """
        if self.is_group:
            data = {
                'owner_id': f"-{self.post_id}",
                'post_id': self.item_id
            }
        else:
            data = {
                'owner_id': self.user_id,
                'post_id': self.item_id
            }

        try:
            # response = self.method('wall.get', ({'owner_id': self.user_id})).json()
            response = self.method('wall.delete', (data)).json()
            logging.info(response)
        except (ConnectionError, RuntimeError, KeyError) as error:
            logging.error(error)

    def get_user_id_to_ban(self, username):
        result = None
        try:
            username = username.replace("/", "")
            response = self.session.get(f"https://vk.com/{username}")
            response_bs = BS(response.text, 'html.parser')

            for a in response_bs.find_all("a", attrs={
                "class": "BtnStack__btn button wide_button acceptFriendBtn Btn Btn_theme_regular"}):
                result = a['data-uid']
                break

            # result = result.replace("return Profile.showGiftBox(", "").replace(", event, 'profile_button');")

            if result is None:
                result = self.method('users.get', ({'user_ids': username})).json()
                return result['response'][0]['id']
        except Exception as e:
            logging.error(e)
        else:
            return result

    def get_user_id(self):
        """
           Get vk user id.
        """
        response = self.method('users.get').json()
        if 'response' in response:
            self.user_id = response['response'][0]['id']
            logging.info("user_id = %s", self.user_id)
        return self.user_id

    def get_token(self):
        """
           Get vk token.
           Return token if succ
        """
        client_id = 2274003
        client_secret = 'hHbZxrka2uZ6jB1inYsH'
        response = {}

        url = f'https://oauth.vk.com/token?grant_type=password&client_id={client_id}&client_secret={client_secret}&username={self.username}&password={self.password}&v=5.103&2fa_supported=1'
        try:
            response = requests.get(url).json()
            self.token = response['access_token']

        except KeyError as error:
            logging.info('Didn`t get: %s', error.args[0])
            if 'error' in response:
                logging.info("Причина: %s", response)
        except ConnectionError as error:
            logging.error("Connection error", error)
        else:
            self.user_id = self.get_user_id()
            return self.token

    def login_likest(self):
        """
           Login likes website.
        """
        response_likes_login = {}
        logging.info('Trying to login to likest')
        try:
            test_connection = requests.head("https://ulogin.ru/auth.php?name=vkontakte")
            logging.info(test_connection.status_code)
            if test_connection.status_code == 500:
                return False

            page = self.session.get('https://ulogin.ru/auth.php?name=vkontakte')
            soup = BS(page.content, 'lxml')
            token = soup.select('script')

            path = "token = \'(.+)\'"
            if token:
                token_login = re.search(path, str(token)).group(1)
                logging.info(f'Likest token: {token_login}')
            else:
                logging.error("Can`t find <script token=...>")

            if token_login:
                response_likes_login = self.session.post(
                    'https://likest.ru/user/login-ulogin/token',
                    headers=self.headers,
                    data={'token': token_login})

        except (NameError, KeyError, Exception) as error:
            logging.info('Failed login likest')
            logging.error(error)
            return False
        else:
            logging.info("Succ logged Likest")
            return True

    def get_likes_balance(self):
        """
           Get likes balance.
        """
        try:
            response = self.session.get(f'http://likest.ru/api/balance.get',
                                        headers=self.headers).json()
        except (TimeoutError, ConnectionError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Likest balance %s', response)
            return response

    def activate_coupon(self, coupon):
        """
           Activate coupon likest.
        """
        try:
            response = self.session.post('http://likest.ru/api/coupons.use',
                                         data={'coupons': str(coupon)},
                                         headers=self.headers).json()

        except (TimeoutError, ConnectionError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Result %s', response)
            return response

    def add_likest_task(self, likes_count, like_url, repost_like, reward='', ):
        """
           Add likest task like.

        """
        get_likes_url = 'https://likest.ru/system/ajax'
        try:
            if repost_like == 'l':
                get_likest_form = self.session.get('https://likest.ru/buy-likes',
                                                   headers=self.headers)
                form_id = 'hpoints_buy_likes_form'
                _triggering_element_value = 'Заказать'


            else:
                get_likest_form = self.session.get('https://likest.ru/reposts/add',
                                                   headers=self.headers)
                form_id = 'hpoints_reposts_add_form'
                _triggering_element_value = 'Получить репосты'

            soup = BS(get_likest_form.content, 'lxml')
            form_build_id = soup.select('input[name=form_build_id]')
            form_token = soup.select('input[name=form_token]')

            form_build_id = str(form_build_id).split('"')[5]
            form_token = str(form_token).split('"')[5]

            payload = {
                "title": like_url,
                "link": like_url,
                "reward": reward,
                "amount": likes_count,
                "sex": "0",
                "country": "0",
                "age_min": "0",
                "age_max": "255",
                "friends_min": "0",
                "lim_5": "0",
                "lim_30": "0",
                "lim_60": "0",
                "sleepy_factor": "0",
                "form_build_id": form_build_id,
                "form_token": form_token,
                "form_id": form_id,
                "_triggering_element_name": "op",
                "_triggering_element_value": _triggering_element_value
            }

            if repost_like == 'l':
                self.session.head('https://likest.ru/buy-likes')
            else:
                self.session.head('https://likest.ru/reposts/add')

            response = self.session.post(get_likes_url, data=payload,
                                         headers=self.headers)
            logging.info(response)

        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task added.')

    def get_likes_list(self):

        try:
            if self.is_group:
                req_url = "https://vk.com/wkview.php"
                data = {
                    "act": "show",
                    "al": 1,
                    "dmcah": "",
                    "loc": f"wall-{self.post_id}_{self.item_id}",
                    "location_owner_id": f"-{self.post_id}",
                    "ref": "",
                    "w": f"likes/wall-{self.post_id}_{self.item_id}"
                }
                users = []
                response = requests.post(req_url, data)

            else:
                req_url = "https://vk.com/wkview.php"
                data = {
                    "act": "show",
                    "al": 1,
                    "loc": f"wall{self.user_id}_{self.item_id}",
                    "location_owner_id": self.user_id,
                    "w": f"likes/wall{self.user_id}_{self.item_id}"
                }
                users = []
                response = requests.post(req_url, data)
            response = response.text.replace("\\", "")
            token_bs = BS(response, 'html.parser')

            for a in token_bs.find_all("a", attrs={"class": "fans_fan_ph"}):
                users.append(a["href"])
        except Exception as e:
            logging.error(e)
        else:
            return users

    def ban_users(self, user):
        try:

            if re.match('id([0-9])+', user) is None:
                user = self.get_user_id_to_ban(user)

            else:
                user = user.replace("/id", "")

            if self.is_group:
                data = {
                    'act': 'spam',
                    'al': '1',
                    'mid': user,
                    'object': 'wall-' + str(self.post_id) + '_' + str(self.item_id)
                }
            else:
                data = {
                    'act': 'spam',
                    'al': '1',
                    'mid': user,
                    'object': 'wall' + str(self.user_id) + '_' + str(self.item_id)
                }

            response = self.session.post('https://vk.com/like.php',
                                         data=data)

            res = re.findall('hash: \'(?:[a-zA-Z]|[0-9])+', str(response.text))[0]
            res = res.replace('hash: \'', '')
            user_hash = res.replace('"', '')

            if self.is_group:
                data = {
                    'act': 'do_spam',
                    'al': '1',
                    'hash': user_hash,
                    'mid': user,
                    'object': 'wall-' + str(self.post_id) + '_' + str(self.item_id)
                }
            else:
                data = {
                    'act': 'do_spam',
                    'al': '1',
                    'hash': user_hash,
                    'mid': user,
                    'object': 'wall' + str(self.user_id) + '_' + str(self.item_id)
                }

            self.session.post('https://vk.com/like.php',
                              data=data)
            self.banned_users.append(user)
        except Exception as e:
            raise e

    def ban_user_report(self):
        """
                   Listen and ban users/delete_likes which like repost.
        """
        users_list = []
        try:
            users_list = self.get_likes_list()
        except KeyError as error:
            logging.error(error)
        try:
            # if users_list:
            #     p = multiprocessing.Pool(processes=len(users_list))
            #     data = p.map_async(self.dothing, [i for i in users_list[:len(users_list)]])
            #     p.close()
            for user in users_list:
                self.ban_users(user)
        #         if re.match('id([0-9])+', user) is None:
        #             user = self.get_user_id_to_ban(user)
        # 
        #         else:
        #             user = user.replace("/id", "")
        #         data = {
        #             'act': 'spam',
        #             'al': '1',
        #             'mid': user,
        #             'object': 'wall' + str(self.user_id) + '_' + str(self.item_id)
        #         }
        # 
        #         response = self.session.post('https://vk.com/like.php',
        #                                      data=data)
        # 
        #         res = re.findall('hash: \'(?:[a-zA-Z]|[0-9])+', str(response.text))[0]
        #         res = res.replace('hash: \'', '')
        #         user_hash = res.replace('"', '')
        # 
        #         data = {
        #             'act': 'do_spam',
        #             'al': '1',
        #             'hash': user_hash,
        #             'mid': user,
        #             'object': 'wall' + str(self.user_id) + '_' + str(self.item_id)
        #         }
        # 
        #         self.session.post('https://vk.com/like.php',
        #                           data=data)
        #         self.banned_users.append(user)
        except Exception as e:
            logging.log(e)
        users_list = []
        time.sleep(1)

    def unban_users(self):
        response = self.session.post('https://vk.com/settings?act=blacklist')

        res = re.findall(f'Settings.delFromBl\((?:[0-9]+), \'(?:[a-zA-Z]|[0-9])+', str(response.text))

        for user_hash in res:
            user_hash = user_hash.replace(f'Settings.delFromBl(', '').replace(" \\", "").replace("'", "").replace(" ",
                                                                                                                  "").split(
                ",")
            user = user_hash[0]
            hash_user = user_hash[1]

            data = {
                'act': 'a_del_from_bl',
                'al': '1',
                'from': 'settings',
                'hash': hash_user,
                'id': user
            }
            print(data)
            self.session.post('https://vk.com/al_settings.php',
                              data=data)

    def get_data_from_link(self, link_to_search):
        """
           Get post id of url. Check if valid or not.
        """
        try:
            if 'wall-' in link_to_search:
                self.is_group = True

            base = (re.findall('wall-?(.+)_(\\d+)', link_to_search))
            if not base:
                raise IndexError
        except IndexError as error:
            logging.error("Invalid url! %s", error)
        else:
            self.post_id = base[0][0]
            self.item_id = base[0][1]
            return base[0]


def save_data_to_file(**kwargs):
    """
    Open data.txt and save.
    Return saved data
    """
    try:
        data = {}
        with open('data.txt', 'r+') as json_file:
            data = json.load(json_file)

        for key in kwargs:
            data[key] = kwargs[key]

        with open('data.txt', 'w+') as json_file:
            json.dump(data, json_file)

        return data
    except KeyError as error:
        if error.args[0] in ['link', 'login', 'password', 'token']:
            logging.info('Cannot find: %s', error.args[0])

    except IOError as error:
        logging.info(error)


def load_data_from_file():
    """
    To load data from file.
    Looks shit/
    """
    result = {}
    try:
        if not os.path.exists('data.txt'):
            with open('data.txt', 'w') as f:
                f.write('{}')

        with open('data.txt') as json_file:
            data = json.load(json_file)

        if 'login' in data:
            result['login'] = data['login']
        if 'password' in data:
            result['password'] = data['password']
        if 'token' in data:
            result['token'] = data['token']
        if 'url' in data:
            result['url'] = data['url']
        if 'user_id' in data:
            result['user_id'] = data['user_id']

    except KeyError as error:
        if error.args[0] in ['link', 'login', 'password', 'token']:
            logging.error('Cannot find: %s', error.args[0])
    except Exception as error:
        raise error
    else:
        return result
