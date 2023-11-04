import logging
import os
import pickle
import re
from vk_api import vk_api
import time
from datetime import datetime
from itertools import product
from multiprocessing.pool import ThreadPool

import requests
from bs4 import BeautifulSoup as BS
from requests import RequestException

from helpers.likest_helper import LikestWorker

with open('logs.log', 'w', encoding="utf-8") as f:
    f.writelines('')

logging.basicConfig(handlers=[logging.FileHandler('logs.log', 'w', 'utf-8')],
                    format=u'%(filename)s[LINE:%(lineno)-2s]# %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)


class VkHelper(LikestWorker):
    """User class."""

    def __init__(self, username, password):
        super(LikestWorker, self).__init__()
        self.time = None
        self.retries = 0
        self.once = True
        self.data = None
        self.count = 0
        self.url = None
        self.group_name = None
        self.group_members = None
        self.username = username
        self.password = password
        self.banned_users = []
        self.token = None
        self.list_2d = [[] for _ in range(0, 3)]
        self.session = requests.Session()
        self.session.cookies.set('remixmdevice', '3440/1440/1/!!-!!!!!!!!-/841', path='/', domain='.vk.com')
        self.item_id = None
        self.user_id = None
        self.is_group = False
        self.url = None
        self.group_id = None
        self.users_hash = None
        self.banned_counter = 0

    def get_user_image(self):
        response = self.method('users.get', {
            'user_ids': self.user_id,
            'fields': 'photo_100'
        }).json()
        if 'response' in response:
            image_url = response['response'][0]['photo_100']
            response = requests.get(f'{image_url}.png', stream=True)
            if response.status_code == 200:
                with open("icons/vk/user_icon.png", 'wb') as f:
                    f.write(response.content)

            os.system('attrib +h icons')

    def method(self, method, values=None):
        """
           Vk method.

           Example: self.method('wall.get', ({'owner_id': self.user_id}))
        """
        try:
            time.sleep(0.3)
            if values is None:
                values = {}
            values['v'] = '5.126'
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
            On successful login return Username
        """

        try:
            logging.info('User login')
            logging.info('Set cookies')
            if os.path.isfile("cookies"):
                with open('cookies', 'rb') as file:
                    self.session.cookies.update(pickle.load(file))

            logging.info('Check is user login')
            page = self.session.get('https://m.vk.com/feed')
            soup = BS(page.content, 'lxml')
            user_name = soup.select_one('a[class="op_owner"]')
            if not user_name:
                logging.info("Updating cookies. Trying to login.")
                vk_session = vk_api.VkApi(self.username, self.password)
                vk_session.auth()
                self.session = vk_session.http
                response = self.session.get('https://vk.com/settings')
                soup = BS(response.content, 'lxml')
                user_name = soup.select_one('a[data-task-click="Settings/show_followers_migration_form_popup"]')
                # a class="settings_right_control" data-is-account-data-not-changed="1" data-is-closed="" data-is-enough-followers="1" data-is-exist-needed-groups="1" data-is-ticket-recently-created="" data-is-verified="1
                if not user_name:
                    raise KeyError
                self.token = vk_session.token.get('access_token')
                self.user_id = vk_session.token.get('user_id')
                self.get_user_id()
            else:
                logging.info("Logged in by cookies!")
                logging.info(f'Successfully login as: {str(user_name["data-name"])}')
        except (TimeoutError, ConnectionError, RuntimeError, KeyError) as error:
            logging.error('Shit happened. Login fail. %s', error)
        else:
            with open('cookies', 'wb+') as file:
                pickle.dump(self.session.cookies, file)
            return user_name['data-name']

    def delete_repost(self):
        """
           Delete just last vk post.
        """
        try:
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
        except AttributeError as error:
            logging.info(error)
            return

        try:
            pass
            # response = self.method('wall.delete', data).json()
            # logging.info(response)
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
            logging.info(f"user_id = {self.user_id}")
        logging.info(response)
        return self.user_id

    def get_token(self):
        """
           Get vk token.
           Return token if successful
        """
        logging.info('Geting token')
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
            logging.info(response)
            self.token = response['access_token']
        except KeyError as error:
            logging.info('Didn\'t get: %s', error.args[0])
            if 'error' in response:
                logging.info("Reason: %s", response)
        except ConnectionError as error:
            logging.error("Connection error", error)
        else:
            self.user_id = self.get_user_id()
            return self.token

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

    def ban_user(self, user):
        try:
            user = str(user)
            # if re.match('id[0-9]+', user) is None:
            #     user = self.get_user_id_to_ban(user)
            # else:
            #     user = user.replace("id", "")
            self.banned_users.append(user)

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

            response = self.session.post('https://vk.com/like.php', data=data)

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

            self.session.post('https://vk.com/like.php', data=data)
            return True
        except Exception as e:
            raise e

    def get_group_id(self):
        try:
            logging.info('Getting group id')
            response = self.method('groups.getById', {
                'group_id': self.url.replace('https://vk.com/', '')
            }).json()
            if 'response' in response:
                self.group_id = response['response'][0]['id']
            logging.info(response)
        except (IndexError, KeyError, RequestException) as error:
            logging.error(error)

    def get_group_members(self):
        group_members = []
        logging.info('Getting group members')
        try:
            # get users
            response = self.method('groups.getMembers', {
                'group_id': self.group_id,
                'sort': 'time_desc',
                'count': 40
            }).json()

            if 'response' in response:
                group_members = response['response']['items']
            logging.info(response)
        except (IndexError, KeyError, RequestException) as error:
            logging.error(error)
        else:
            return group_members

    @staticmethod
    def get_user_id_hash_from_string_delete(url):
        try:
            user_id = re.findall(r'[mu]?id=[0-9]+', str(url))
            user_id = user_id[0].replace('mid=', '')
            user_id = user_id.replace('uid=', '')
            user_id = user_id.replace('id=', '')

            user_hash = re.findall('hash=[A-z0-o]+', str(url))
            user_hash = user_hash[0].replace('hash=', '')
        except Exception as error:
            logging.error(error)
            return None, None
        return user_hash, user_id

    def ban_user_group(self, user):
        temp_user = user
        try:
            self.session.post(f'https://m.vk.com/{temp_user}', data={'_ajax': 1})
            self.banned_users.append(user)
            # self.users_hash.append(user)
        except RequestException as error:
            logging.info(error)
        return True

    def unban_group_user(self, user):
        temp_user = user.replace('action=-1&', '')
        try:
            self.session.post(f'https://m.vk.com/{temp_user}', data={'_ajax': 1})
            self.banned_users.remove(user)
        except Exception as error:
            logging.error(error)
            return False
        else:
            return True

    def clear_group_users(self, is_all=False):
        banned = []
        if is_all:
            for item in self.list_2d:
                if item:
                    for user in item:
                        banned.append(user)
        else:
            for user in self.list_2d[0]:
                banned.append(user)

        if banned:
            with ThreadPool(processes=10) as pool:
                results = pool.starmap_async(self.unban_group_user, product(banned))
                results.wait()
                logging.info(f"Unbanned: {results.get()}")
                pool.close()
                pool.terminate()

        if self.banned_users and is_all:
            with ThreadPool(processes=5) as pool:
                results = pool.starmap_async(self.unban_group_user, product(self.banned_users))
                results.wait()
                logging.info(f"Unbanned: {results.get()}")
                pool.close()
                pool.terminate()

    def get_group_users_hash(self):
        hashes = []
        try:
            #            response = self.session.get(f'https://vk.com/{self.group_name}?act=users')
            # soup = BS(response.text, 'lxml')
            # users_hash = soup.select(f'a[class="group_u_action"]')
            # path = "\[this,\s\d+,\s\'(.+)\'"
            # for hash in users_hash:
            #     real_hash = re.search(path, str(hash)).group(1)
            #     hashes.append(real_hash)

            response = self.session.get(f'https://m.vk.com/{self.group_name}?act=users')
            soup = BS(response.text, 'lxml')
            users_hash = soup.select(f'div[class="si_links"]>a:nth-of-type(2)')
            for hash in users_hash:
                hashes.append(hash.get('href'))
        except Exception as error:
            logging.info(error)
        return hashes

    def unban_user_main_page(self, user):
        data = {
            'act': 'unban_user',
            'uid': user[2],
            'from': 'blacklist',
            'hash': user[1],
        }
        self.session.post(f'https://m.vk.com{user[0]}', data=data)
        return True

    def add_friends(self, user):
        response = self.session.post(f'https://m.vk.com/friends?act=accept&id={user[2]}&hash={user[1]}&from=requests',
                                     data={'_ajax': 1}).text
        if '"payload":[0' not in response:
            return True

    def keep_as_follower(self, user):
        response = self.session.post(f'https://m.vk.com/friends?act=decline&id={user[2]}&hash={user[1]}&from=requests',
                                     data={'_ajax': 1}).text
        if '"payload":[0' not in response:
            return True

    def clear_add_users_from_bl(self, combo_box_index):
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
                if not user_id:
                    continue
                users_to_unban.append((url, user_id, user_hash))

            if not users_to_unban:
                is_users_to_unban = False
                break

            if users_to_unban:
                with ThreadPool(processes=10) as pool:
                    results = pool.starmap_async(self.unban_user_main_page, product(users_to_unban))
                    results.wait()
                    logging.info(f'Unban: {results.get()}')

            users_to_add = []
            if combo_box_index == 1:
                self.method('friends.deleteAllRequests')
                return True

            if combo_box_index == 0:
                response = self.session.get('https://m.vk.com/friends?section=requests&all=1&sort=date')
                soup = BS(response.content, 'lxml')

                users_data = soup.select('a[class="BtnStack__btn Btn Btn_theme_small"]')

                for data in users_data:
                    url = data.get('href')
                    user_id, user_hash = self.get_user_id_hash_from_string_delete(url)
                    if not user_id:
                        continue
                    users_to_add.append((url, user_id, user_hash))

                if users_to_add:
                    with ThreadPool(processes=10) as pool:
                        results = pool.starmap_async(self.add_friends, product(users_to_add))
                        results.wait()
                        logging.info(f'Friends add: {results.get()}')

                response = self.method('friends.getRequests').json()
                users = response['response']['items']
                for user in users:
                    self.method('friends.add', {'user_id': user})
                    time.sleep(0.4)

                is_users_to_unban = False
                break

    def ban_user_friend_request(self, user):
        try:
            response = self.session.get(f'https://m.vk.com/id{user}')
            soup = BS(response.text, 'lxml')
            if soup.select_one('div[class="service_msg service_msg_error"]'):
                response = self.session.get(f'https://vk.com/id{user}', headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4041.0 Safari/537.36'})
                soup = BS(response.text, 'lxml')
                if soup.select_one('h5[class="profile_blocked page_block"]'):
                    return True

                user_hash = soup.select_one('a[class="page_actions_item PageActionItem--block"]')
                user_hash = user_hash.get('onclick')
                user_hash = user_hash.replace('Profile.toggleBlacklist(this, \'', '').replace('\', event)', '')
                data = {
                    'act': 'a_add_to_bl',
                    'al': 1,
                    'from': 'profile',
                    'hash': user_hash,
                    'id': user,
                }
                response = self.session.post(f'https://vk.com/al_settings.php', data=data)
                if '{"payload":[0' in str(response.text):
                    return True
                else:
                    return False
            if soup.select_one('div[class="service_msg service_msg_null"]'):
                return True
            url = soup.select('a[class="ContextMenu__listLink"]')
            url = url[2].get('href')

            response = self.session.post(f'https://m.vk.com{url}')
            soup = BS(response.text, 'lxml')
            if soup.select_one('div[class="service_msg service_msg_error"]'):
                return False
            else:
                return True
        except Exception as e:
            logging.error(e)
            return False

    def wait_for_balance_back(self, reward, count, combo_box_index):
        try:
            response = self.session.get('https://likest.ru/orders/friends')
            soup = BS(response.text, 'lxml')
            items = soup.select('div[class="form-item form-type-item"]')
            if 'Заявок на проверке' not in items[2].text:
                self.change_friends_task(reward=reward, count=0)
                self.clear_add_users_from_bl(combo_box_index)
                return True
            return False
        except Exception as e:
            logging.error(e)
            self.change_friends_task(reward=reward, count=0)

    def ban_user_friends(self, reward, count, combo_box_index=0, is_stop=False):
        try:
            time.sleep(0.7)
            response = ''
            if self.banned_counter >= 5 and self.once and not is_stop:
                self.change_friends_task(reward=reward, count=0)
                self.once = False

            if self.banned_counter >= 5 and not is_stop:
                if self.wait_for_balance_back(reward=reward, count=count, combo_box_index=combo_box_index):
                    time.sleep(5)
                    self.change_friends_task(reward=reward, count=count, is_change_to_normal=True)
                    self.once = True
                    self.banned_counter = 0

            current_hashes = self.method('friends.getRequests', {'count': 100, "need_viewed": 0}).json()
            current_hashes = current_hashes['response']['items']

            hashes = current_hashes.copy()
            if current_hashes:
                logging.info(f'users_to_ban: {current_hashes}')
                for user in current_hashes:
                    if user not in self.banned_users:
                        response = self.method('account.ban', {'owner_id': user}).json()
                        logging.info(response)
                        if 'response' in response:
                            if str(response['response']) == '1':
                                hashes.remove(user)
                                self.banned_users.append(user)
                                self.banned_counter += 1
                                time.sleep(0.4)
                        elif 'error' in response:
                            break
                res = True
                if hashes:
                    for user in hashes:
                        res = self.ban_user_friend_request(user)
                        logging.info(res)
                        time.sleep(0.5)
                        if res:
                            self.banned_users.append(user)
                            self.banned_counter += 1
                        elif res is False:
                            break
                if res is False and 'error' in response:
                    self.change_friends_task(reward=reward, count=0)
                    self.wait_for_balance_back(reward=reward, count=count, combo_box_index=combo_box_index)
                    raise Exception('Flood control')
        except Exception as e:
            self.change_friends_task(reward=reward, count=0)
            self.banned_counter = 6
            logging.error(e)

    def ban_users_group(self):
        current_time = datetime.now()
        difference = (self.time - current_time)
        logging.info(int(difference.total_seconds()))

        users_to_ban = []
        current_hashes = self.get_group_users_hash()

        if int(difference.total_seconds()) == -60 and self.once:
            self.once = False
            self.list_2d[0] = [_ for _ in self.list_2d[1]]
            self.list_2d[1] = [_ for _ in self.list_2d[2]]
            self.list_2d[-1].clear()

        for hash_url in current_hashes:
            if hash_url not in self.users_hash:
                users_to_ban.append(hash_url)
                self.users_hash.append(hash_url)

        if users_to_ban:
            for user in users_to_ban:
                self.list_2d[-1].append(user)

        if int(difference.total_seconds()) <= -68:
            self.once = True
            self.clear_group_users()
            # self.users_hash = self.get_group_users_hash()
            self.time = datetime.now()

        if users_to_ban:
            logging.info(f'users_to_ban: {users_to_ban}')

            with ThreadPool(processes=10) as pool:
                results = pool.starmap_async(self.ban_user_group, product(users_to_ban))
                results.wait()
                logging.info(f"Banned: {results.get()}")
                pool.close()
                pool.terminate()
        time.sleep(0.5)

    def ban_user_report(self, is_kill=False, task_type: str = None, reward: str = None, count: str = None):
        """
           Wait and ban users/delete_likes.
        """
        users = []
        req_likes = None
        current_time = datetime.now()
        difference = (self.time - current_time)
        logging.info(int(difference.total_seconds()))
        if int(difference.total_seconds()) <= -30 and self.once and not is_kill:
            self.once = False
            if task_type == 'like':
                self.change_likes_task()
            elif task_type == 'repost':
                self.change_repost_task()

        if int(difference.total_seconds()) <= -40 and not is_kill:
            if task_type == 'like':
                if self.check_is_task_changed('like'):
                    self.change_likes_task()
                    self.add_task_likes(count=self.count, url=self.url)
                    self.once = True
                    self.time = datetime.now()
            elif task_type == 'repost':
                if self.check_is_task_changed('repost'):
                    self.change_repost_task()
                    time.sleep(10)
                    self.add_task_reposts(count=count, url=self.url, reward=reward)
                    self.once = True
                    self.time = datetime.now()

        try:
            if self.is_group:
                req_likes = self.method('likes.getList', ({
                    'type': 'post',
                    'owner_id': f'-{self.post_id}',
                    'item_id': self.item_id
                })).json()
            else:
                req_likes = self.method('likes.getList', ({
                    'type': 'post',
                    'owner_id': self.user_id,
                    'item_id': self.item_id
                })).json()

            if 'response' in req_likes:
                logging.info(req_likes)
                if req_likes['response']['count'] != 0:
                    users = req_likes['response']['items']
            elif 'error' in req_likes:
                logging.info(req_likes)
                return req_likes
        except KeyError as error:
            logging.error(error)
            logging.error(req_likes)

        try:
            if users:
                with ThreadPool(processes=10) as pool:
                    results = pool.starmap_async(self.ban_user, product(users))
                    results.wait()
                    logging.info(results.get())
                    pool.close()
                    pool.terminate()
        except Exception as e:
            logging.error(e)
        time.sleep(0.7)

    def unban_user_group(self, url, progress_callback=None):
        user_hash, user_id = self.get_user_id_hash_from_string_delete(url)

        data = {
            'act': 'done_block',
            'mid': user_id,
            'tab': 'blacklist',
            'hash': user_hash,
            '_tstat': '',
            '_ref': self.group_name,
        }
        self.session.post(f'https://m.vk.com/{self.group_name}{url}', data=data)
        return True

    def clear_black_list_main_page(self, url=None, progress_callback=None):
        is_users_to_unban = True
        users_to_unban = []
        while is_users_to_unban:
            users_to_unban = []
            response = self.session.get(f'https://vk.com/settings?act=blacklist')
            soup = BS(response.content, 'lxml')
            users_data = soup.select('a[class="ii_btn"]')

            for data in users_data:
                url = data.get('href')
                user_hash, user_id = self.get_user_id_hash_from_string_delete(url)
                users_to_unban.append((url, user_id, user_hash))

            if not users_to_unban:
                is_users_to_unban = False
                break

            for user in users_to_unban:
                data = {
                    'act': 'unban_user',
                    'uid': user[1],
                    'from': 'blacklist',
                    'hash': user[2],
                }
                self.session.post(f'https://m.vk.com{user[0]}', data=data)

    def clear_black_list_public(self, url, progress_callback=None):
        is_users_to_unban = True
        users_to_unban = []
        self.group_name = url.replace('https://vk.com/', '')

        while is_users_to_unban:
            response = self.session.get(f'https://m.vk.com/{self.group_name}?act=blacklist')
            soup = BS(response.text, 'lxml')
            users_hash = soup.select(f'div[class="si_links"]>a:nth-of-type(2)')

            for hash in users_hash:
                users_to_unban.append(hash.get('href'))

            with ThreadPool(processes=5) as pool:
                results = pool.starmap_async(self.unban_user_group, product(users_to_unban))
                results.wait()
                logging.info(results.get())
                pool.close()
                pool.terminate()

            if not users_to_unban or len(users_to_unban) == 1:
                is_users_to_unban = False
                break
            time.sleep(0.5)

    def get_data_from_link(self, link_to_search, is_likes_reposts):
        """
           Get post id of url. Check if valid or not.
        """
        group = None
        wall = None
        try:
            if 'wall-' in link_to_search:
                self.is_group = True

            if is_likes_reposts:
                wall = (re.findall('wall-?(.+)_(\\d+)', link_to_search))
                if not wall:
                    raise IndexError
            else:
                group = (re.fullmatch(r'^https://vk.com/([A-z0-9]+)$', link_to_search))
                if not group:
                    raise IndexError
                else:
                    self.is_group = True
                    self.group_name = link_to_search.replace('https://vk.com/', '')
        except IndexError as error:
            logging.error("Invalid url %s", error)
        else:
            if group:
                self.url = group.string
                return self.url
            elif wall:
                self.url = link_to_search
                self.post_id = wall[0][0]
                self.group_id = wall[0][0]
                self.item_id = wall[0][1]

                return wall[0]
