'''
Author: wangyunfei
Date: 2023-07-16 09:42:49
LastEditors: wangyunfei
LastEditTime: 2023-07-30 01:24:42
Description: file content
FilePath: /platfrom/commo/getCode.py
'''

import requests
import os
import json
import time
import random


class GetCode:

    def __init__(self, user, passwd) -> None:

        self.url = 'http://api.fgma.top'
        self.user = user
        self.passwd = passwd
        data = self._get_token()
        self.token = data['data']['authtoken']
        self.comid = 19409758
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Authorization': self.token,
            'Cookie': 'sidebarStatus=1',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Length': '98',
            'Origin': 'http://yjyfdc.com',
            'Referer': 'http://yjyfdc.com/',
            'Signid': 'AEA9152CA1D1A3AF679893238227ED87'
        }
        time.sleep(1)

    def _get_token(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        params = {
            'account':	self.user,
            'password':	self.passwd,
            'loginsource':	"API"
        }
        url = f'{self.url}/api/login'
        r = requests.get(url, headers=headers, params=params)
        return r.json()

    def get_itemid(self):
        url = f'{self.url}/api/project/searchItem'
        data = {
            "itemtype": 0,
            "itemname": "学习强国"
        }
        r = requests.post(url, headers=self.headers, json=data)
        data = r.json()
        if '学习强国' == data['data']['itemlist'][0]['item_project_website']:
            pass

        itemid = data['data']['itemlist'][0]['item_id']

    def get_phone(self, phone='', statusType=False):

        url = f'{self.url}/api/phone/loadReceivePhone'
        if not statusType:
            likephoneList = ['192']
            likephone = random.sample(likephoneList, 1)[0]
            likephone = ''
        else:
            likephone = ''
        print(likephone)
        data = {
            # 项目名称
            "itemid": 934,
            # 项目类型 0为收码，1为发码 默写0就行
            "itemtype": 0,
            # 手机号类型0随机，1实体号，2虚拟号
            "phonetype": 1,
            "igblock": 0,
            "likephone": '',
            'form': '网页端',
            'phone': phone
        }
        r = requests.post(url, headers=self.headers, json=data)
        data = r.json()
        print(data)
        self.comid = data['data']['comid']
        phone = data['data']['itemlist']['phone']
        return phone

    def get_code(self):
        url = f'{self.url}/api/phone/getPutSmsResult'
        data = {
            "comid": self.comid
        }
        print(data)
        com_code = ''
        count = 0
        while True:
            if count >= 20:
                break
            try:
                r = requests.post(url, headers=self.headers, json=data)
                data1 = r.json()
                com_code = data1['data']['comdata']['com_code']
                print(data1['data']['comdata'])
            except:
                print(data1)
                continue
            if com_code != '':
                break
            else:
                count += 1
                time.sleep(2)
            print('='*100)
        print(com_code)
        return com_code


if __name__ == '__main__':
    g = GetCode()
    # g.get_phone()
    # time.sleep(10)
    g.get_code()


# 18580621361
