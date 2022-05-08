import json
import os
import pickle
import re
import time
from datetime import datetime
from itertools import product
from multiprocessing.pool import Pool
import vk_api
import requests
from bs4 import BeautifulSoup as BS
import datetime


class VkWorker:
    """User class."""

    def __init__(self, username, password):
        self.time = None
        self.username = username
        self.password = password
        self.banned_users = []
        self.session = requests.Session()
        self.token = None

    def method(self, method, values=None):
        """
           Vk method.

           Example: self.method('wall.get', ({'owner_id': self.user_id}))
        """
        try:
            if values is None:
                values = {}
            values['v'] = '5.126'
            if self.token:
                values['access_token'] = self.token

        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            print(error)
        else:
            return self.session.post(
                'https://api.vk.com/method/' + method,
                values
            )

    def get_token(self):
        """
           Get vk token.
           Return token if successful
        """
        client_id = 2274003
        client_secret = 'hHbZxrka2uZ6jB1inYsH'
        response = {}

        url = f'https://oauth.vk.com/token?grant_type=password&' \
              f'client_id={client_id}&' \
              f'client_secret={client_secret}&' \
              f'username={self.username}&' \
              f'password={self.password}&v=5.126&2fa_supported=1 '
        try:
            response = requests.get(url).json()
            self.token = response['access_token']

        except KeyError as error:
            print('Didn\'t get: %s', error.args[0])
            if 'error' in response:
                print("Reason: %s", response)
        except ConnectionError as error:
            print("Connection error", error)
        else:
            return self.token

    def login(self):
        """
            Login and save cookies.
            Login vk by username:password or cookies.
            On successful login return Username
        """

        try:
            if os.path.isfile("cookies"):
                with open('cookies', 'rb') as file:
                    self.session.cookies.update(pickle.load(file))

            page = self.session.get('https://m.vk.com/login')
            soup = BS(page.content, 'lxml')
            user_name = soup.select('a[class=op_owner]')
            if not user_name:
                print("Updating cookies! Trying to login.")
                url = soup.find('form')['action']
                response = self.session.post(url,
                                             data={'email': self.username,
                                                   'pass': self.password},
                                             )
                soup = BS(response.content, 'lxml')
                user_name = soup.select('a[class=op_owner]')
                if not user_name:
                    raise KeyError
                self.get_token()
            else:
                print("Logged by cookies!")
                print('Successfully login as: %s', user_name[0]["data-name"])
        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            print('Shit happend. Login fail. %s', error)
        else:
            return user_name[0]["data-name"]

    def unban_users(self, user):
        data = {
            'act': 'unban_user',
            'uid': user[2],
            'from': 'blacklist',
            'hash': user[1],
        }
        self.session.post(f'https://m.vk.com{user[0]}', data=data)
        return True

    def ban_user(self, user):
        try:
            # self.vk.account.ban(owner_iduser)
            # response = self.method('account.ban', {'owner_id': user}).json()
            response = self.session.get(f'https://m.vk.com/id{user}')
            soup = BS(response.text, 'lxml')
            url = soup.select('a[class="ContextMenu__listLink"]')
            url = url[2].get('href')
            self.session.post(f'https://m.vk.com/{url}', data={'_ajax': 1})

        except Exception as e:
            return False
        else:
            return True

    @staticmethod
    def get_user_id_hash_from_string_delete(url):
        user_id = re.findall(r'[mu]?id=[0-9]+', str(url))
        user_id = user_id[0].replace('mid=', '')
        user_id = user_id.replace('uid=', '')
        user_id = user_id.replace('id=', '')

        user_hash = re.findall('hash=[A-z0-o]+', str(url))
        user_hash = user_hash[0].replace('hash=', '')
        return user_hash, user_id

    def clear_add_users_from_bl(self):
        is_users_to_unban = True
        users_to_unban = []
        while is_users_to_unban:
            users_to_unban = []
            response = self.session.get(f'https://vk.com/settings?act=blacklist')
            soup = BS(response.content, 'lxml')
            users_data = soup.select('a[class="ii_btn"]')

            for data in users_data:
                url = data.get('href')
                user_id, user_hash = self.get_user_id_hash_from_string_delete(url)
                users_to_unban.append((url, user_id, user_hash))

            if users_to_unban:
                with Pool(processes=len(users_to_unban)) as pool:
                    results = pool.starmap_async(self.unban_users, product(users_to_unban))
                    results.wait()
                    print(results.get())

            users_to_add = []
            response = self.session.get('https://m.vk.com/friends?section=requests&all=1&sort=date')
            soup = BS(response.content, 'lxml')
            users_data = soup.select('a[class="BtnStack__btn Btn Btn_theme_small"]')
            for data in users_data:
                url = data.get('href')
                user_id, user_hash = self.get_user_id_hash_from_string_delete(url)
                users_to_add.append((url, user_id, user_hash))

            if users_to_add:
                with Pool(processes=len(users_to_add)) as pool:
                    results = pool.starmap_async(self.add_friends, product(users_to_add))
                    results.wait()
                    print(results.get())

            if not (users_to_unban and users_to_add):
                response = self.method('friends.getRequests').json()
                users = response['response']['items']
                response = self.method('friends.areFriends', {'user_ids': users}).json()

                is_users_to_unban = False
                break

    def add_friends(self, user):
        response = self.session.post(f'https://m.vk.com/friends?act=accept&id={user[2]}&hash={user[1]}&from=requests',
                          data={'_ajax': 1}).text
        if '"payload":[0' not in response:
            return True

    def main(self):

        self.time = datetime.now()
        print(':'.join(datetime.datetime.now().strftime("%H:%M:%S").split(':')))
        while True:
            current_time = datetime.now()
            difference = (self.time - current_time)
            if int(difference.total_seconds()) <= -300:
                self.clear_black_list_main_page()
                self.time = datetime.now()

            response = self.method('friends.getRequests').json()
            users = response['response']['items']

            if users:
                with Pool(processes=len(users)) as pool:
                    results = pool.starmap_async(self.ban_user, product(users))
                    results.wait()
                    print(results.get())
            time.sleep(0.33)


def load_token():
    result = {}
    try:
        if not os.path.exists('token.txt'):
            with open('token.txt', 'w') as f:
                f.write('{}')

        with open('token.txt') as json_file:
            data = json.load(json_file)

        if 'token' in data:
            result['token'] = data['token']

    except KeyError as error:
        if error.args[0] in ['link', 'login', 'password', 'token']:
            print('Cannot find: %s', error.args[0])
    except Exception as error:
        raise error
    else:
        return result


def save_token(**kwargs):
    """
    Open data.txt and save.
    Return saved data
    """
    try:
        data = {}
        with open('token.txt', 'r+') as json_file:
            data = json.load(json_file)

        for key in kwargs:
            data[key] = kwargs[key]

        with open('token.txt', 'w+') as json_file:
            json.dump(data, json_file)

        return data
    except KeyError as error:
        if error.args[0] in ['link', 'login', 'password', 'token']:
            print('Cannot find: %s', error.args[0])

    except IOError as error:
        print(error)


if __name__ == '__main__':
    user = VkWorker('+79278818462', 'kDsuNWLp4YX7exi4g19q')
    user.login()
    user.main()
