#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('二叉树轮换车头运行脚本');
'''


client_id1 = ""
client_secret1 = ""
url1 = "http://xxxxxxxx:xxxx/"
scname = "脚本名字"
start = 1           # 开始号
name = "任务名字"
sleep_time1 = 60    # 任务执行时长
sleep_time2 = 30    # 完成后间隔
team_nums = 30      # 一队几人


import requests
import time
import json

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, client_id_temp, client_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + client_id_temp + '&client_secret=' + client_secret_temp
    gettoken(self, url_token)


def getitem(self, baseurl, typ, path):
    url = baseurl + typ + "/scripts/files?path={}".format(path)
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getenvs(self, baseurl, typ):
    url = baseurl + typ + "/envs"
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getscript(self, baseurl, typ, filename):
    url = baseurl + typ + "/scripts/" + filename + "?t=%s" % gettimestamp()
    r = self.get(url)
    response = json.loads(r.text)["code"]
    if response == 500:
        url = baseurl + typ + "/scripts/" + filename + "?path="
        r = self.get(url)
    script = json.loads(r.text)["data"]
    return script


def pushscript(self, baseurl, typ, data, path):
    url = baseurl + typ + "/scripts?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    response = json.loads(r.text)["code"]
    if response == 500:
        data["path"] = path
        r = self.put(url, data=json.dumps(data))
    return r.text


def getcrons(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def addcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.post(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def runcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/run?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def stopcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/stop?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def deletecron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.delete(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


if __name__ == '__main__':
    # 主容器
    s = requests.session()
    login(s, url1, client_id1, client_secret1)
    tasks = getcrons(s, url1, "open")
    envs = getenvs(s, url1, "open")
    count = 0
    for i in envs:
        if i["name"] == "JD_COOKIE" and i["status"] == 0:
            count += 1
    print("共计有效账号 {}\n".format(count))
    status = 0
    for i in tasks:
        if scname in i["command"]:
            stopcron(s, url1, "open", [i["_id"]])
            time.sleep(1)
            deletecron(s, url1, "open", [i["_id"]])
            time.sleep(1)
            for j in range(start, count):
                for k in range(j, j + team_nums + 1):
                    if j + 11 < count - 1 and k == j + 20:
                        wzz = " " + str(j) + "-" + str(k)
                    elif k == j + 20:
                        wzz = " " + str(j) + "-" + str(k - 30)
                data = {
                    "command": "task {} desi JD_COOKIE ".format(scname) + str(wzz),
                    "schedule": "1",
                    "name": name
                }
                res1 = addcron(s, url1, "open", data)
                time.sleep(1)
                id = json.loads(res1)["data"]["_id"]
                runcron(s, url1, "open", [id])
                print("运行账号 {}".format(j))
                time.sleep(sleep_time1)
                stopcron(s, url1, "open", [id])
                time.sleep(1)
                deletecron(s, url1, "open", [id])
                time.sleep(1)
                time.sleep(sleep_time2)
                if j == count - 1:
                    status = 1
                    break
    if status == 0:
        for j in range(start, count + 1):
            for k in range(j, j + team_nums + 1):
                if j + 11 < count - 1 and k == j + 20:
                    wzz = " " + str(j) + "-" + str(k)
                elif k == j + 20:
                    wzz = " " + str(j) + "-" + str(k - 30)
            data = {
                "command": "task {} desi JD_COOKIE ".format(scname) + str(wzz),
                "schedule": "1",
                "name": name
            }
            res1 = addcron(s, url1, "open", data)
            time.sleep(1)
            id = json.loads(res1)["data"]["_id"]
            runcron(s, url1, "open", [id])
            print("运行账号 {}".format(j))
            time.sleep(sleep_time1)
            stopcron(s, url1, "open", [id])
            time.sleep(1)
            deletecron(s, url1, "open", [id])
            time.sleep(1)
            time.sleep(sleep_time2)
            if j == count - 1:
                status = 1
                break










