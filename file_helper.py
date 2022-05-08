import json
import logging
import os


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
    Load data from file
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
