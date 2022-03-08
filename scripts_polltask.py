# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools
# 半成品
'''
cron: 1
new Env('单容器 二叉树自动启用任务');
'''

import os
import time
import json
import re
import random

try:
    if os.environ["ec_expect_list"] != "":
        expect_list = ["二叉树", "任务 ", "更新", "ql raw", "ql repo", "拉取", "通用", "ql ", "opencard", "tptp", "help", "助力"]
        expect_list += os.environ["ec_expect_list"].split("@")
        print("已配置不检索列表，不检索的禁用任务表为：\n{}\n".format(expect_list))
    else:
        expect_list = ["二叉树", "任务 ", "更新", "ql raw", "ql repo", "拉取", "通用", "ql ", "opencard", "tptp", "help", "助力"]
        pass
except:
    print("默认不检索")
    print("有需要请在配置文件中配置\nexport ec_expect_list=\"任务名字1@任务名字2\" \n用@分隔不需要检索的已禁用的任务的关键字\n")
    exit(3)

try:
    if os.environ["ec_poll_start_time"] != "":
        start_time = int(os.environ["ec_poll_start_time"])
        print("已配置初始化时间为：\n{}\n".format(start_time))
    else:
        start_time = 6
        pass
except:
    print("使用默认初始时间6秒，尝试运行时长少于6秒已经结束的任务不检索，每个禁用执行配置时长后自动停止，然后检索日志")
    print("有需要请在配置文件中配置\nexport ec_poll_start_time=\"初始秒数\" \n自定义时长\n")
    start_time = 6

try:
    if os.environ["ec_poll_end_time"] != "":
        end_time = int(os.environ["ec_poll_end_time"])
        print("已配置每个任务检索时间：\n{}\n".format(end_time))
    else:
        end_time = 60
        pass
except:
    print("使用默认每个任务检索时间60秒，尝试运行时长多于60秒已经结束的任务自动停止，然后检索日志")
    print("有需要请在配置文件中配置\nexport ec_poll_end_time=\"检索时长秒数\" \n自定义时长\n")
    end_time = 60

print("\n=================说明===================")
print("分为7类异常，如果异常存在于运行日志中，则不启用\n"
      "如果异常不存在于其中，则启用")
print("7类异常内含的关键字请查看脚本注释并自行修改")
print("下方配置异常用模式数值对应表示")
print("异常             模式\n"
      "点击频繁:         1\n"
      "活动火爆:         2\n"
      "活动结束:         3\n"
      "缺少依赖:         4\n"
      "网络问题:         5\n"
      "执行中异常有影响:  6\n"
      "执行有异常无影响:  7")
print("========================================\n")

try:
    if os.environ["ec_select_erro"] == "":
        select_erro = "1,2,3,4,5,6,7"
        print("使用默认模式： {}".format(select_erro))
    else:
        select_erro = os.environ["ec_select_erro"]
        print("使用自定义模式： {}".format(select_erro))
except:
    print("未配置检索模式")
    print("如需要检索，请在配置文件中配置\nexport ec_select_erro=\"1,2,3,等等\" \n用“,”分隔模式，留空则默认使用所有模式\n")
    exit(3)

# 选择启用逻辑
# 六大类别
# pf  点击频繁 1
# hb  活动火爆 2
# js  活动结束 3
# yl  缺少依赖 4
# wl  网络问题 5
# zx  执行异常 6
pf = ["操作太频繁", "频繁"]  # 频繁
hb = ["活动太火爆", "火爆"]  # 火爆
js = ["活动已经结束", "活动结束", "等待下一次活动开启"]  # 结束
yl = ["Error: Cannot find module"]  # 依赖
wl = ["Response code"]  # 网络
zx = ["TypeError: Cannot read property"]  # 执行
zx2 = ["点太快", "异常"]  # 异常不影响
err_list = [pf, hb, js, yl, wl, zx, zx2]
erro_text = []
for i in select_erro.split(","):
    erro_text += err_list[int(i) - 1]

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


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self):
    self.headers.update({"Authorization": "Bearer " + __get_token()})


def login(self):
    gettoken(self)


def gettaskitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getstatus(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/" + data[0] + "?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
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


def getlogcron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/" + data[0] + "/log?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.get(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.text
    else:
        return r.text


def enablecron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/enable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return r.text


if __name__ == '__main__':
    ccoott = []
    print("================开始======================\n")
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        tasks = gettaskitem(s, ql_url, "api")
    except:
        ql_url = 'http://localhost:5600/'
        tasks = gettaskitem(s, ql_url, "api")

    # 取已禁用任务
    disable_list = []
    for i in tasks:
        if i["isDisabled"] == 1:
            status = 0
            for j in expect_list:
                if j in i["name"] or j in i["command"]:
                    status = 1
                    break
            if status == 0:
                disable_list.append(i)

    # 启用逻辑
    print("启用逻辑： {}".format(erro_text))

    for i in disable_list:
        print("-------------------------------------------\n")
        print("检索禁用的任务： {}".format(i["name"]))
        try:
            id = i["_id"]
        except:
            id = i["id"]

        # 状态码       status
        # 运行            0
        # 结束运行空闲中  1

        # 第一次运行判断任务是否在运行
        runcron(s, ql_url, "api", [id])
        res1 = getstatus(s, ql_url, "api", [id])
        status = json.loads(res1)["data"]["status"]

        # 运行时长短于限定时间不检索，队列中结束运行不检索
        if status == 1:
            print("运行时间短于{}秒，不自动启用\n".format(start_time))
            continue
        elif status == 0:
            time.sleep(start_time)
            res1 = getstatus(s, ql_url, "api", [id])
            status2 = json.loads(res1)["data"]["status"]
            if status2 == 1:
                print("运行时间短于{}秒，不自动启用\n".format(start_time))
                continue
        else:
            print("运行时间短于{}秒，不自动启用\n".format(start_time))
            continue

        # 判断运行是否结束
        ct = 0
        while status != 1:
            res1 = getstatus(s, ql_url, "api", [id])
            status = json.loads(res1)["data"]["status"]
            # 查看实时日志
            if status != 1:
                res2 = getlogcron(s, ql_url, "api", [id])
                result = json.loads(res2)["data"]
                err_status = 0
                for j in erro_text:
                    if j in result:
                        err_status = 1
                        break
                if err_status == 1:
                    stopcron(s, ql_url, "api", [id])
            time.sleep(1)
            ct += 1
            if ct >= end_time:
                stopcron(s, ql_url, "api", [id])
                break

        # 无报错自动启用
        if status == 1 and err_status == 0:
            enablecron(s, ql_url, "api", [id])
            ccoott.append(i["name"])
            print("无报错，已自动启用\n")
        else:
            print("有报错，不自动启用\n")

    print("================结束======================\n")

    print("自动启用任务{}个，名字如下".format(len(ccoott)))
    for m in ccoott:
        print(m)








