import json
import logging
import re
import time
from random import choice

import requests
from bs4 import BeautifulSoup as BS


class LikestWorker:
    def __init__(self):
        self.group_name = None
        self.url = None
        self.session = requests.Session()

        self.friends_task_url = None
        self.data = None

    def login_likest(self, access_token) -> bool:
        """Login likest

        Returns:
            True or False: Login result
        """
        token_login = None
        logging.info('Trying to login to likest')
        try:
            page = self.session.get('https://ulogin.ru/auth.php?name=vkontakte')
            time.sleep(0.5)
            soup = BS(page.content, 'lxml')
            token = soup.select('script')
            hash_return_auth = None
            hash_return_auth = re.search('"return_auth":"(.+)"},"domains', str(token)).group(1)
            params = {
                "redirect_uri": "https://ulogin.ru/auth.php?name=vkontakte",
                "app_id": 3280318,
                "scope": 4194306,
                "is_seamless_auth": 1,
                "access_token": access_token,
                "hash": hash_return_auth,

            }
            response = self.session.post("https://api.vk.com/method/auth.getOauthCode?v=5.207&client_id=3280318",
                                         params=params).json()
            time.sleep(0.5)
            response_code = response['response']

            page = self.session.get(f'https://ulogin.ru/auth.php?name=vkontakte&code={response_code}')
            time.sleep(0.5)
            soup = BS(page.content, 'lxml')
            token = soup.select('script')
            path = "token = \'(.+)\'"
            if token:
                token_login = re.search(path, str(token)).group(1)
                logging.info(f'Likest token: {token_login}')
            else:
                logging.error("Can`t find <script token=...>")

            if token_login:
                response = self.session.post(
                    'https://likest.ru/user/login-ulogin/token',
                    data={'token': token_login})
                soup = BS(response.content, 'lxml')
                user_balance = soup.select_one('span[id="user-balance"]')
                if not user_balance:
                    return False
        except (NameError, KeyError, Exception) as error:
            logging.info('Failed login likest')
            logging.error(error)
            return False
        else:
            logging.info("Successfully logged in Likest")
            return True

    def get_likes_balance(self) -> str:
        """Get likes balance

        Returns:
            current_balance (str): Current likest balance
        """
        current_balance = None
        try:
            response = self.session.get(f'http://likest.ru/api/balance.get').json()
            if 'balance' in response:
                current_balance = response['balance']
        except (TimeoutError, ConnectionError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Likest balance %s', response)
            return current_balance

    def activate_coupon(self, coupon: str) -> json:
        """Activate coupon likest

        Returns:
            json: json response
        """
        try:
            response = self.session.post(
                'http://likest.ru/api/coupons.use',
                data={'coupons': str(coupon)}
            ).json()
        except (TimeoutError, ConnectionError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Result %s', response)
            return response

    def add_task_likes(self, url, count):
        try:
            get_likest_form = self.session.get('https://likest.ru/buy-likes')
            soup = BS(get_likest_form.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_token = soup.select_one('input[name=form_token]')

            form_build_id = form_build_id.get('value')
            form_token = form_token.get('value')

            payload = {
                "title": url,
                "link": url,
                "amount": count,
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
                "form_id": 'hpoints_buy_likes_form',
                "_triggering_element_name": "op",
                "_triggering_element_value": 'Заказать'
            }

            self.session.head('https://likest.ru/buy-likes')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task added likes')

    def get_friends_task_url(self):
        response = self.session.get('https://likest.ru/orders/friends')
        soup = BS(response.content, 'lxml')
        self.friends_task_url = soup.select_one('a[class="order-action"]').get('href')

    def change_friends_task(self, reward, count, is_change_to_normal=False):
        try:
            friends_min = 999
            mail = 1
            lim_60 = 1
            get_likest_form = self.session.get(f'https://likest.ru/{self.friends_task_url}')
            soup = BS(get_likest_form.content, 'lxml')

            form_build_id = soup.select_one('input[name=form_build_id]')
            form_token = soup.select_one('input[name=form_token]')

            form_build_id = form_build_id.get('value')
            form_token = form_token.get('value')

            payload = {
                "amount": count,
                "reward": reward,
                "sex": "0",
                "country": "0",
                "age_min": "0",
                "age_max": "255",
                "friends_min": friends_min,
                "mail": mail,
                "lim_5": "0",
                "lim_30": "0",
                "lim_60": lim_60,
                "sleepy_factor": "0",
                "form_build_id": form_build_id,
                "form_token": form_token,
                "form_id": 'hpoints_friends_edit_form',
                "_triggering_element_name": "op",
                "_triggering_element_value": 'Сохранить'
            }
            if is_change_to_normal:
                friends_min = 0
                mail = 0
                lim_60 = 0
                payload = {
                    "amount": count,
                    "reward": reward,
                    "sex": "0",
                    "country": "0",
                    "age_min": "0",
                    "age_max": "255",
                    "friends_min": friends_min,
                    "lim_5": "0",
                    "lim_30": "0",
                    "lim_60": lim_60,
                    "sleepy_factor": "0",
                    "form_build_id": form_build_id,
                    "form_token": form_token,
                    "form_id": 'hpoints_friends_edit_form',
                    "_triggering_element_name": "op",
                    "_triggering_element_value": 'Сохранить'
                }

            self.session.head('https://likest.ru/friends/add')
            self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError, Exception) as error:
            logging.error(error)
        else:
            logging.info('Task changed friends')

    def add_task_friends(self, count, reward):
        try:
            get_likest_form = self.session.get('https://likest.ru/friends/add')
            soup = BS(get_likest_form.content, 'lxml')

            form_build_id = soup.select_one('input[name=form_build_id]')
            form_token = soup.select_one('input[name=form_token]')

            form_build_id = form_build_id.get('value')
            form_token = form_token.get('value')

            payload = {
                "reward": reward,
                "amount": count,
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
                "form_id": 'hpoints_friends_add_form',
                "_triggering_element_name": "op",
                "_triggering_element_value": 'Заказать'
            }

            self.session.head('https://likest.ru/friends/add')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task added friend')

    def add_task_reposts(self, url, count, reward):
        try:
            get_likest_form = self.session.get('https://likest.ru/reposts/add')
            soup = BS(get_likest_form.content, 'lxml')

            form_build_id = soup.select_one('input[name=form_build_id]')
            form_token = soup.select_one('input[name=form_token]')

            form_build_id = form_build_id.get('value')
            form_token = form_token.get('value')

            payload = {
                "title": url,
                "link": url,
                "reward": reward,
                "amount": count,
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
                "form_id": 'hpoints_reposts_add_form',
                "_triggering_element_name": "op",
                "_triggering_element_value": 'Получить репосты'
            }

            self.session.head('https://likest.ru/reposts/add')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
            logging.info(response.text)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task added reposts')

    def add_task_group_followers(self, url, count, reward):
        try:
            get_likest_form = self.session.get('https://likest.ru/groups/add')
            soup = BS(get_likest_form.content, 'lxml')

            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            payload = {
                "link": url,
                "reward": reward,
                "amount": count,
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
                "form_id": 'hpoints_groups_add_form',
                "_triggering_element_name": "op",
                "_triggering_element_value": 'С правилами согласен, заказать'
            }

            self.session.head('https://likest.ru/groups/add')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task added group followers')

    def get_tokens(self, like_repost):
        # Get tokens to change state to activa tasks
        if 'repost' in like_repost:
            response = self.session.get('https://likest.ru/orders/reposts')
        elif 'like' in like_repost:
            response = self.session.get('https://likest.ru/orders/likes')
        soup = BS(response.content, 'lxml')
        form_build_id = soup.select_one('input[name=form_build_id]')
        self.form_build_id = form_build_id.get('value')
        form_token = soup.select_one('input[name=form_token]')
        self.form_token = form_token.get('value')
        self.data = {
            'state': 2,
            'last_changed': 0,
            'op': 'Применить',
            'form_build_id': self.form_build_id,
            'form_token': self.form_token,
            'form_id': 'hpoints_orders_filter_form'
        }

    def check_is_task_changed(self, like_repost):
        if not self.data:
            self.get_tokens(like_repost)

        group_name = self.url.replace('https://vk.com/wall', '')
        group_name = group_name.replace('https://m.vk.com/wall', '')

        if 'repost' in like_repost:
            response = self.session.post('https://likest.ru/orders/reposts', data=self.data)
        elif 'like' in like_repost:
            response = self.session.post('https://likest.ru/orders/likes', data=self.data)

        soup = BS(response.content, 'lxml')
        all_orders = soup.select('div[class="order-view"]')
        for order in all_orders:
            temp = order.select_one('a[class="vklink"]')
            if group_name in temp.get('href'):
                items = soup.select('div[class="form-item form-type-item"]')
                if 'Заблокировано' not in items[2].text:
                    return True
                else:
                    return False
        return False

    def change_repost_task(self):
        countries = [176, 141, 136, 131, 116, 96]
        try:
            last_order = None
            group_name = self.url.replace('https://vk.com/wall', '')
            group_name = group_name.replace('https://m.vk.com/wall', '')

            # Get tokens to change state to active tasks
            response = self.session.get('https://likest.ru/orders/reposts')
            soup = BS(response.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            data = {
                'state': 2,
                'last_changed': 0,
                'op': 'Применить',
                'form_build_id': form_build_id,
                'form_token': form_token,
                'form_id': 'hpoints_orders_filter_form'
            }

            # get all active orders
            response = self.session.post('https://likest.ru/orders/reposts', data=data)
            soup = BS(response.content, 'lxml')
            all_orders = soup.select('div[class="order-view"]')
            for order in all_orders:
                temp = order.select_one('a[class="vklink"]')
                if group_name in temp.get('href'):
                    last_order = order.select_one('a[class="order-action"]').get('href')
                    break

            response = self.session.get(f'https://likest.ru/{last_order}')
            soup = BS(response.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            payload = {
                'amount': '0',
                'reward': '4',
                'sex': '0',
                'country': str(choice(countries)),
                'city': '0',
                'age_min': '0',
                'age_max': '255',
                'friends_min': '0',
                'lim_5': '0',
                'lim_30': '0',
                'lim_60': '1',
                'sleepy_factor': '0',
                'form_build_id': form_build_id,
                'form_token': form_token,
                'form_id': 'hpoints_reposts_edit_form',
                '_triggering_element_name': 'op',
                '_triggering_element_value': 'Сохранить',
            }

            self.session.head(f'https://likest.ru/{last_order}')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task changed')

    def change_likes_task(self):
        countries = [176, 141, 136, 131, 116, 96, 173]
        try:
            group_name = self.url.replace('https://vk.com/wall', '')
            group_name = group_name.replace('https://m.vk.com/wall', '')
            last_order = None

            # Get tokens to change state to activa tasks
            response = self.session.get('https://likest.ru/orders/likes')
            soup = BS(response.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            data = {
                'state': 2,
                'last_changed': 0,
                'op': 'Применить',
                'form_build_id': form_build_id,
                'form_token': form_token,
                'form_id': 'hpoints_orders_filter_form'
            }

            # get all active orders
            response = self.session.post('https://likest.ru/orders/likes', data=data)
            soup = BS(response.content, 'lxml')
            all_orders = soup.select('div[class="order-view"]')

            for order in all_orders:
                temp = order.select_one('a[class="vklink"]')
                if group_name in str(temp.get('href')):
                    last_order = order.select_one('a[class="order-action"]').get('href')
                    break

            response = self.session.get(f'https://likest.ru/{last_order}')
            soup = BS(response.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            payload = {
                'amount': '0',
                'reward': '2',
                'sex': '0',
                'country': str(choice(countries)),
                'city': '0',
                'age_min': '0',
                'age_max': '255',
                'friends_min': '0',
                'lim_5': '0',
                'lim_30': '0',
                'lim_60': '1',
                'sleepy_factor': '0',
                'form_build_id': form_build_id,
                'form_token': form_token,
                'form_id': 'hpoints_likes_edit_form',
                '_triggering_element_name': 'op',
                '_triggering_element_value': 'Сохранить',
            }

            self.session.head(f'https://likest.ru/{last_order}')
            self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task changed')

    def get_tokens_groups(self):
        # Get tokens to change state to active tasks
        response = self.session.get('https://likest.ru/orders/groups')
        soup = BS(response.content, 'lxml')
        form_build_id = soup.select_one('input[name=form_build_id]')
        form_build_id = form_build_id.get('value')
        form_token = soup.select_one('input[name=form_token]')
        form_token = form_token.get('value')

        self.data = {
            'state': 2,
            'last_changed': 0,
            'op': 'Применить',
            'form_build_id': form_build_id,
            'form_token': form_token,
            'form_id': 'hpoints_orders_filter_form'
        }

    def is_group_task_changed(self):
        if not self.data:
            self.get_tokens_groups()

        group_name = self.group_name.replace('public', '')
        group_name = group_name.replace('club', '')

        response = self.session.post('https://likest.ru/orders/groups', data=self.data)

        soup = BS(response.content, 'lxml')
        all_orders = soup.select('div[class="order-view"]')
        for order in all_orders:
            temp = order.select_one('a[class="vklink"]')
            if group_name in temp.get('href'):
                items = soup.select('div[class="form-item form-type-item"]')
                if 'Заблокировано' not in items[2].text:
                    return True
                else:
                    return False
        return False

    def change_group_followers_task(self):
        countries = [176, 141, 136, 131, 116, 96]
        try:
            last_order = None
            group_name = self.group_name.replace('public', '')
            group_name = group_name.replace('club', '')

            if not self.data:
                self.get_tokens_groups()

            # get all active orders
            response = self.session.post('https://likest.ru/orders/groups', data=self.data)
            soup = BS(response.content, 'lxml')
            all_orders = soup.select('div[class="order-view"]')

            for order in all_orders:
                temp = order.select_one('a[class="vklink"]')
                if group_name in temp.get('href'):
                    last_order = order.select_one('a[class="order-action"]').get('href')
                    break

            response = self.session.get(f'https://likest.ru/{last_order}')
            soup = BS(response.content, 'lxml')
            form_build_id = soup.select_one('input[name=form_build_id]')
            form_build_id = form_build_id.get('value')
            form_token = soup.select_one('input[name=form_token]')
            form_token = form_token.get('value')

            payload = {
                'amount': '0',
                'reward': '2',
                'sex': '0',
                'country': str(choice(countries)),
                'city': '0',
                'age_min': '0',
                'age_max': '255',
                'friends_min': '0',
                'lim_5': '0',
                'lim_30': '0',
                'lim_60': '1',
                'sleepy_factor': '0',
                'form_build_id': form_build_id,
                'form_token': form_token,
                'form_id': 'hpoints_groups_edit_form',
                '_triggering_element_name': 'op',
                '_triggering_element_value': 'Сохранить',
            }

            self.session.head(f'https://likest.ru/{last_order}')
            response = self.session.post('https://likest.ru/system/ajax', data=payload)
        except (ConnectionError, TimeoutError, ValueError, RuntimeError) as error:
            logging.error(error)
        else:
            logging.info('Task changed')

    def add_likest_task(self, task_type: str, count: str, reward=None, url=None):
        """
           Add likest task like.
        """
        if task_type == 'like':
            self.add_task_likes(url, count)
        elif task_type == 'repost':
            self.add_task_reposts(url, count, reward)
        elif task_type == 'followers':
            self.add_task_group_followers(url, count, reward)
        elif task_type == 'friends':
            self.add_task_friends(count, reward)
