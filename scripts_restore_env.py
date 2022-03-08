# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树还原环境变量');
'''


import os
import time
import json
import re
import random

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ql_auth_path = '/ql/config/auth.json'


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def __get__headers() -> dict:
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer ' + __get_token()
    }
    return headers


# 查询环境变量
def get_envs(name: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    if name is not None:
        params['searchValue'] = name
    res = requests.get(ql_url + '/api/envs', headers=__get__headers(), params=params)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self):
    self.headers.update({"Authorization": "Bearer " + __get_token()})


def login(self):
    gettoken(self)


def getallenv(self, baseurl, typ):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()  # JD_COOKIE为默认的环境变量名，该变量里的值默认含pt_pin和pt_key，其他类似默认按照下面注释改
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []


def insert(self, baseurl, typ, name, value, remarks):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    if remarks == None:
        data_json = {
            "value": value,
            "name": name
        }
    else:
        data_json = {
            "value": value,
            "name": name,
            'remarks': remarks
        }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.json()['data']
    else:
        return False


def delete(self, baseurl, typ, value):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = value
    r = self.delete(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def disable(self, baseurl, typ, ids):
    url = baseurl + typ + "/envs/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(ids))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    print("还原顺序 备份.json trigger_cookies.json \n 如果前者存在就还原前者，前者不存在还原后者，请保留其中一个文件还原")
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    allenv = getallenv(s, ql_url, "api")
    for i in allenv:
        try:
            delete(s, ql_url, 'api', [i['_id']])
        except:
            delete(s, ql_url, 'api', [i['id']])
    if os.path.exists('备份.json') == True:
        tt = '备份.json'
        print("还原 {}".format(tt))
    elif os.path.exists('trigger_cookies.json') == True:
        tt = 'trigger_cookies.json'
        print("还原 {}".format(tt))
    else:
        print("找不到 备份.json 或 trigger_cookies.json 跳出还原")
        exit(3)
    with open(tt,'r',encoding='utf-8') as fp:
        allenv = json.loads(fp.read())
    for i in allenv:
        try:
            i['remarks']
            c = insert(s, ql_url, "api", i['name'], i['value'], i['remarks'])
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
        except:
            c = insert(s, ql_url, "api", i['name'], i['value'], None)
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
    print("还原完毕")
    print("============================================")
    print("脚本执行完毕")