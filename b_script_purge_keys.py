# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('二叉树屏蔽关键词');
'''

# 屏蔽词
keys = []

# 屏蔽词也可在fake_keys.txt中按一行一行填写
try:
    with open("fake_keys.txt", "r") as fp:
        t = fp.readlines()
    for j in t:
        keys.append(j)
except:
    print("fake_keys.txt 未创建，有需要请按照注释进行操作")

import re

for i in t:
    keys.append(i)

keys = list(set(keys))

# 屏蔽词替换成real_key的值
real_key = "www.baidu.com"

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：pip3 install requests")
import time
import json
import os


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


def getitem(self, baseurl, typ):
    url = baseurl + typ + "/scripts/files?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getscript(self, baseurl, typ, filename):
    url = baseurl + typ + "/scripts/" + filename + "?t=%s" % gettimestamp()
    r = self.get(url)
    script = json.loads(r.text)["data"]
    return script


def pushscript(self, baseurl, typ, data):
    url = baseurl + typ + "/scripts?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    # response = json.loads(r.text)["data"]
    return r


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
        return True
    else:
        return r.text

def traversalDir_FirstDir(path):
    list = []
    if (os.path.exists(path)):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path, file)
            if (os.path.isdir(m)):
                h = os.path.split(m)
                list.append(h[1])
        return list


def read_ex(or_list):
    # 加载远程依赖剔除依赖文件的检索
    try:
        res1 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents").json()
        time.sleep(5)
        res2 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/utils").json()
        time.sleep(4)
        res3 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/function").json()
        try:
            res1["documentation_url"]
            return
        except:
            try:
                res2["documentation_url"]
                return
            except:
                try:
                    res3["documentation_url"]
                    return
                except:
                    pass


    except:
        print("网络波动，稍后尝试")
        time.sleep(5)
        try:
            res1 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents").json()
            time.sleep(5)
            res2 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/utils").json()
            time.sleep(4)
            res3 = requests.get("https://api.github.com/repos/spiritLHL/dependence_scripts/contents/function").json()
            try:
                res1["documentation_url"]
                return
            except:
                try:
                    res2["documentation_url"]
                    return
                except:
                    try:
                        res3["documentation_url"]
                        return
                    except:
                        pass
        except:
            print("网络问题无法获取仓库文件列表，停止加载远程文件剔除依赖文件，直接本地检索")

    for i in res1:
        or_list.append(i["name"])
    for i in res2:
        or_list.append(i["name"])
    for i in res3:
        or_list.append(i["name"])
    or_list = list(set(or_list))
    return or_list

def check_root():
    zscripts_list = []
    for i in zscripts:
        zscripts_list.append(i["key"])
    try:
        zscripts_list.remove("fake_keys.txt")
    except:
        print("fake_keys.txt未创建，请按照注释创建")
    print("主青龙脚本文件数量：{}".format(len(zscripts_list)))
    print()
    print()

    print("查询结束，正在修改中")
    print()

    # 查询需要更改的脚本内容
    change_script_list = []
    change_content = []
    # 查询根目录
    for i in zscripts_list:
        content = getscript(s, ql_url, "api", i)
        data_script = {
            "filename": i,
            "content": content,
            "path": ""
        }
        change_content.append(content)
        change_script_list.append(data_script)

    origin_script_list = change_script_list.copy()
    origin_content = change_content.copy()

    # 替换关键词
    tp = []
    for i in origin_content:
        tpp = i.split("\n")
        tp_list = []
        for j in keys:
            for k in tpp:
                if j in k:
                    c = k.replace(j, "", 5) + "\n"
                    tp_list.append(c)
        temp = tp_list[0]
        for l in tp_list[1:]:
            temp += l
        tp.append(temp)

    # 构造请求内容，进行正式修改
    count = 0
    change_k = []
    for k in tp:
        if change_script_list[count]["content"] != k:
            data_script = {
                "filename": change_script_list[count]["filename"],
                "content": k,
                "path": ""
            }
            change_k.append(data_script)
        else:
            change_k.append(change_script_list[count])
        count += 1

    # 修改
    count = 0
    ct = 0
    while True:
        if count <= (len(change_script_list) - 1):
            if change_k[count] != origin_script_list[count]:
                pushscript(s, ql_url, "api", change_k[count])
                print("屏蔽关键字的脚本文件 {}".format(change_k[count]["filename"]))
            else:
                ct += 1
            count += 1
        else:
            break
    print()

def check_dir():
    return


if __name__ == '__main__':
    # 主容器
    s = requests.session()
    login(s)

    # 获取主青龙任务
    print("=========== 主青龙 信息获取中 =============")
    print()

    # 获取主青龙的脚本名
    try:
        ql_url = 'http://localhost:5700/'
        zscripts = getitem(s, ql_url, "api")
    except:
        ql_url = 'http://localhost:5600/'
        zscripts = getitem(s, ql_url, "api")

    # 查询根目录
    check_root()

    # 查询分文件夹
    check_dir()

    print("屏蔽脚本文件关键词完毕")














