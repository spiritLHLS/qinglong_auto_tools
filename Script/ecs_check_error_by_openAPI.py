# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('二叉树监控脚本运行');
'''
import random

ids=["xxxxxxxxxxx"]
secrets=["xxxxxxxxx"]
urllist=["http://xxxxxxxxxxx:xxxx/"]

errr_text = [
    "Response code",
    "Error: Cannot find module",
    "异常",
    "操作太频繁",
    "TypeError: Cannot read property",
    "活动已经结束",
    "活动太火爆",
    "点太快"
]

ec_log_disable = True


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


def getitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def getenvs(self, baseurl, typ):
    url = baseurl + typ + "/envs"
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def getlogcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/" + data[0] + "/log?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text

def synchronous_tasks_disable(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text

def getcrons(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item



if __name__ == '__main__':
    for num_u in range(0, len(urllist)):
        print("===================================")
        print("查询青龙 {}".format(num_u+1))

        print("--------------------------------")
        s = requests.session()
        login(s, urllist[num_u], ids[num_u], secrets[num_u])
        ztasks = getitem(s, urllist[num_u], "open")
        enable_list = []
        for i in ztasks:
            if i['isDisabled'] == 0:
                if i["command"][-2:] == "js" or i["command"][-2:] == "py":
                    enable_list.append(i)
        pf = []
        hb = []
        js = []
        yl = []
        wl = []
        zx = []
        for i in enable_list:
            # script_name = i["command"].replace("task ", "").split("/")[0]
            try:
                res = getlogcron(s, urllist[num_u], "open", [i["_id"]])
                status = 0

                for j in errr_text:
                    if j in res:
                        status = 1
                if status == 1:
                    # print("{}".format(i["name"]))
                    # print("已知报错原因:")

                    if "操作太频繁" in res or "点太快" in res:
                        pf.append(i)
                        # print("操作太频繁")

                    if "活动太火爆" in res:
                        hb.append(i)
                        # print("活动太火爆")

                    if "活动已经结束" in res:
                        js.append(i)
                        # print("活动已经结束")

                    if "Error: Cannot find module" in res:
                        yl.append(i)
                        # print("找不到模块，可能缺少依赖文件或依赖环境")

                    if "Response code" in res:
                        wl.append(i)
                        # print("网络原因的错误导致上报状态码")

                    if "TypeError: Cannot read property" in res:
                        zx.append(i)
                        # print("执行过程中有 报错 ，未知原因")

                    if "异常" in res:
                        zx.append(i)
                        # print("执行过程中有 异常 ，未知原因")

                    # print("--------------------------------")
                    time.sleep(random.uniform(0.2, 0.5))
                else:
                    pass
            except:
                print("{}查不到日志".format(i["name"]))


        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
        print("青龙地址\n{}\n启用的任务对应的日志中存在错误的任务名字为：".format(urllist[num_u]))
        print("操作太频繁:{}".format([j["name"] for j in pf]))
        print("活动太火爆:{}".format([j["name"] for j in hb]))
        print("活动已经结束:{}".format([j["name"] for j in js]))
        print("缺少依赖:{}".format([j["name"] for j in yl]))
        print("网络请求问题:{}".format([j["name"] for j in wl]))
        print("执行过程中有问题:{}".format([j["name"] for j in zx]))
        print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")

        if ec_log_disable == True:
            print("已配置自动禁用活动结束的任务")
            temp = []
            temp = temp + js
            temp = list(set(temp))
            disable_list_log = []
            for k in temp:
                disable_list_log.append(k["_id"])
                print("自动禁用 {}".format(k["name"]))
            synchronous_tasks_disable(s, urllist[num_u], "open", disable_list_log)
        print("===================================")















