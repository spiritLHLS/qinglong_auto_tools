# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树监控脚本运行');
'''
import random
import requests
import time
import json
import os

# 该脚本将启用的任务对应的日志进行检索
# 若脚本日志异常，分类成6大异常，并输出异常的任务名字
# 自动禁用只会自动禁用含 结束的活动 的关键词的任务日志对应的任务
# 有别的类别的自动禁用需求，自行更改本脚本223行

erro_text = [
    "Response code",
    "Error: Cannot find module",
    "操作太频繁",
    "TypeError: Cannot read property",
    "活动已经结束",
    "活动结束",
    "活动太火爆",
    "点太快",
    "异常"
]

whitelist = [
    "东东农场",
    "东东萌宠",
    "京东种豆得豆",
    "京喜工厂",
    "东东工厂",
    "京东赚赚",
    "京喜农场",
    "口袋书店",
    "签到领现金",
    "闪购盲盒",
    "京喜财富岛",
    "东东健康社区",
    "摇钱树",
    "种豆得豆",
    "店铺签到",
    "5G超级盲盒",
    "摇京豆",
    "超级直播间红包雨",
    "寻找内容鉴赏官",
    "东东电竞经理",
    "早起福利",
    "秒秒币"
]

ql_auth_path = '/ql/config/auth.json'

print("该脚本将启用的任务对应的日志进行检索，若脚本日志异常，分类成6大异常，并输出异常的任务名字，自动禁用只会自动禁用含 结束的活动 的任务，有别的类别的自动禁用需求，自行更改本脚本223行，详细更改方法看脚本注释\n")

try:
    if os.environ["ec_log_detail"] == "true":
        ec_log_detail = True
        print("已配置开启详情模式，输出每个任务的报错原因\n")
    else:
        ec_log_detail = False
        pass
except:
    ec_log_detail = False
    print("默认不开启详情模式")
    print("请在配置文件中配置 export ec_log_detail=\"true\" 开启详情模式")
    print("开启详情模式后将输出每个任务的报错原因，不再输出报错原因的任务合集\n")

try:
    if os.environ["ec_log_disable"] == "true":
        ec_log_disable = True
        print("已配置自动禁用含 结束的活动 的任务\n")
    else:
        pass
except:
    ec_log_disable = False
    print("默认不禁用任务")
    print("请在配置文件中配置 export ec_log_disable=\"true\" 开启脚本自动禁用任务\n")

try:
    if os.environ["ec_log_whitelist"] == "true":
        ec_log_whitelist = True
        print("已配置开启白名单，自动禁用除白名单外的异常任务\n")
    else:
        pass
except:
    ec_log_whitelist = False
    print("默认不启用白名单不禁用任务")
    print("请在配置文件中配置 export ec_log_whitelist=\"true\" 开启脚本白名单\n")
    print("白名单开启后将不禁用白名单内的任务")

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def __get_token() -> str or None:
    with open(ql_auth_path, 'r', encoding='utf-8') as f:
        j_data = json.load(f)
    return j_data.get('token')


def gettoken(self):
    res = __get_token()
    self.headers.update({"Authorization": "Bearer " + res})


def login(self):
    gettoken(self)


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


def synchronous_tasks_enable(self, baseurl, typ, data):
    url = baseurl + typ + "/crons/enable?t=%s" % gettimestamp()
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
    print("===================================")
    print("查询任务日志中")

    print("--------------------------------")
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        ztasks = getitem(s, ql_url, "api")
    except:
        ql_url = 'http://localhost:5600/'
        ztasks = getitem(s, ql_url, "api")
    enable_list = []
    for i in ztasks:
        if i['isDisabled'] == 0:
            if i["command"][-2:] == "js" or i["command"][-2:] == "py":
                enable_list.append(i)
    pf = []  # 频繁
    hb = []  # 火爆
    js = []  # 结束
    yl = []  # 依赖
    wl = []  # 网络
    zx = []  # 执行
    zx2 = []  # 异常不影响
    for i in enable_list:
        # script_name = i["command"].replace("task ", "").split("/")[0]
        try:
            try:
                res = getlogcron(s, ql_url, "api", [i["_id"]])
            except:
                res = getlogcron(s, ql_url, "api", [i["id"]])
            status = 0

            for j in erro_text:
                if j in res:
                    status = 1
            if status == 1:
                if ec_log_detail == True:
                    print("{}".format(i["name"]))
                    print("已知报错原因:")

                if "操作太频繁" in res or "点太快" in res:
                    pf.append(i)
                    if ec_log_detail == True:
                        print("操作太频繁")

                if "活动太火爆" in res:
                    hb.append(i)
                    if ec_log_detail == True:
                        print("活动太火爆")

                if "活动已经结束" in res or "活动结束" in res:
                    js.append(i)
                    if ec_log_detail == True:
                        print("活动已经结束")

                if "Error: Cannot find module" in res:
                    yl.append(i)
                    if ec_log_detail == True:
                        print("找不到模块，可能缺少依赖文件或依赖环境")

                if "Response code" in res:
                    wl.append(i)
                    if ec_log_detail == True:
                        print("网络原因的错误导致上报状态码")

                if "TypeError: Cannot read property" in res:
                    zx.append(i)
                    if ec_log_detail == True:
                        print("执行过程中有 报错 ，未知原因")

                if "异常" in res:
                    if ec_log_whitelist != True:
                        zx.append(i)
                    zx2.append(i)
                    if ec_log_detail == True:
                        print("执行过程中有 异常 ，未知原因")

                if ec_log_detail == True:
                    print("--------------------------------")
                time.sleep(random.uniform(0.2, 0.5))
            else:
                pass
        except:
            print("{}查不到日志".format(i["name"]))

    if ec_log_detail == True:
        print("================================================\n")
    else:
        print("启用的任务对应的日志中存在错误的任务名字为：")
        print("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓")
        print("操作太频繁:")
        for k in [j["name"] for j in pf]:
            print(k)

        print()
        print("活动太火爆:")
        for k in [j["name"] for j in hb]:
            print(k)

        print()
        print("活动已经结束:")
        for k in [j["name"] for j in js]:
            print(k)

        print()
        print("缺少依赖:")
        for k in [j["name"] for j in yl]:
            print(k)

        print()
        print("网络请求问题:")
        for k in [j["name"] for j in wl]:
            print(k)

        print()
        print("执行过程中有问题:")
        for k in [j["name"] for j in zx]:
            print(k)
        print("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑")

    if ec_log_disable == True:
        print("已配置自动禁用任务")
        temp = []
        # 六大类别
        # pf  点击频繁
        # hb  活动火爆
        # js  活动结束
        # yl  缺少依赖
        # wl  网络问题
        # zx  执行异常
        temp = temp + js  # 有需求自己改这行自行添加需要禁用的任务类别往后 +hb+zx 这样子写
        tp = []
        for j in temp:
            if j not in tp:
                tp.append(j)
        disable_list_log = []
        for k in tp:
            try:
                disable_list_log.append(k["_id"])
            except:
                disable_list_log.append(k["id"])
            print("自动禁用任务： {}".format(k["name"]))
        synchronous_tasks_disable(s, ql_url, "api", disable_list_log)
    else:
        print("未配置自动禁用任务")
        print("请在配置文件中配置 export ec_log_disable=\"true\" 开启脚本自动禁用任务\n")

    if ec_log_whitelist == True:
        print("已配置自动禁用白名单外的任务")
        temp = []
        temp = temp + pf + hb + js + yl + wl + zx

        temp2 = []
        for n in temp:
            if n not in temp2 and n not in zx2:
                temp2.append(n)
        temp = temp2

        # 禁用异常
        tp = []
        for j in temp:
            if j not in tp:
                tp.append(j)
        disable_list_log = []
        for k in tp:
            try:
                disable_list_log.append(k["_id"])
            except:
                disable_list_log.append(k["id"])
            pt = 0
            for m in whitelist:
                if k["name"] in m or m in k["name"]:
                    pt = 1
                    break
                else:
                    pt = 0
            if pt == 0:
                print("自动禁用任务： {}".format(k["name"]))
        synchronous_tasks_disable(s, ql_url, "api", disable_list_log)

        # 启用白名单
        tp = []
        for j in temp:
            if j not in tp:
                for k in whitelist:
                    if j["name"] in k or k in j["name"]:
                        tp.append(j)
                        break
        enable_list_log = []
        for k in tp:
            try:
                enable_list_log.append(k["_id"])
            except:
                enable_list_log.append(k["id"])
            print("白名单任务不禁用但有报错： {}".format(k["name"]))
        for k in zx2:
            try:
                enable_list_log.append(k["_id"])
            except:
                enable_list_log.append(k["id"])
        synchronous_tasks_enable(s, ql_url, "api", enable_list_log)
    else:
        print("未配置白名单")
        print("请在配置文件中配置 export ec_log_whitelist=\"true\" 开启脚本白名单\n")
        print("白名单开启后将不禁用白名单内的任务，但会禁用其他异常任务，执行有异常但可以执行的也不会禁用")

    print("===================================")




















