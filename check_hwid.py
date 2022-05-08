import logging
import subprocess

import requests
from requests import RequestException


def get_hwid() -> str:
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen('C:\\Windows\\System32\\Wbem\\wmic csproduct get UUID', startupinfo=startupinfo,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        return str(process.stdout.read()).split('\\r\\n')[1].strip('\\r').strip()
    except Exception as e:
        print(e)
        return ''


def get_hdsn():
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen('C:\\Windows\\System32\\Wbem\\wmic DISKDRIVE get SerialNumber',
                                   startupinfo=startupinfo, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        return ''.join(str(process.stdout.read()).replace('\'', '').replace('\\r\\r\\n', '').split(' ')[1:])
    except Exception as e:
        print(e)
        return ''


def check_hwid() -> bool:
    return True
    try:
        logging.disable(logging.DEBUG)
        #response = requests.get("https://pastebin.com/raw/GFQrRHcS")
        # for testers
        response = requests.get("https://pastebin.com/raw/eTPDZHgJ")
        user_hwid = get_hwid()
        hd_sn = get_hdsn()
        user_hwid = user_hwid + '-' + hd_sn
        logging.info(user_hwid)
        logging.disable(logging.NOTSET)
    except (RequestException, ConnectionError) as error:
        logging.error(error)
    else:
        return user_hwid in response.text