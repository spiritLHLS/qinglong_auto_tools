# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('多容器 二叉树分发ck');
'''

# 在脚本管理里修改这个文件的配置，然后保存，然后禁用 二叉树分发ck 这个任务，有需要再点运行
# 记得修改定时，定时在你的转换ck脚本运行完后分发即可

# 主青龙，wskey容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
# 本分发脚本不含转ck功能，只分发，默认分发的环境变量名为JD_COOKIE，其他变量名自己按照下面注释改
# 分发不含wskey的ck的分容器，事先需要在分容器里创建应用，给所有权限，然后重启容器，应用设置才会生效
# 按照格式有几个写几个，没有的空的删除
# 备份ck的容器，里面传入所有转换后的ck，，事先需要在备份容器里创建应用，给所有权限，然后重启容器，应用设置才会生效
# ps:跑一些需要所有ck脚本的备份容器，你懂的
'''
# ec_config.txt中填写如下设置

# 二叉树分发ck
### 主青龙
cks_push_alql_cilent_id1="xxxxxxxx"
cks_push_alql_cilent_secret1="xxxxxxxxxx"
cks_push_alql_url1="http://xxxxxxxx:xxxx/"
### 副青龙
cks_push_alql_N_c=""
cks_push_alql_client_ids=["",""]
cks_push_alql_client_secrets=["",""]
cks_push_alql_urllist=["http://xxxxxxxxx:xxxx/",""]
### 备份容器
cks_push_alql_cilent_id_che=["xxxxxxxx"]
cks_push_alql_cilent_secret_che=["xxxxxxxxxx"]
cks_push_alql_che=["http://xxxxxxxx:xxxx/"]

'''
# client_id1=""
# client_secret1=""
# url1 = "http://ip:端口/"
# client_ids=['','','']
# client_secrets=['','','']
# urllist = ["http://xxxx:xxxx/","",""]
# client_id_che=''
# client_secret_che=''
# che = "http://xxxxx:xxx/"

# 分容器默认配置，如果在配置ec_config.txt中填写有该配置，则会覆盖下面默认40
N_c = 40

import os
import time
import json
import re

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

try:
    with open("ec_config.txt", "r", encoding="utf-8") as fp:
        t = fp.readlines()
    try:
        for i in t:
            try:
                temp = re.findall(r"cks_push_alql_cilent_id1=\"(.*?)\"", i)[0]
                client_id1 = temp
                if client_id1 == "":
                    print("cks_push_alql_cilent_id1 未填写")
            except:
                pass
    except:
        print("cks_push_alql_cilent_id1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"cks_push_alql_cilent_secret1=\"(.*?)\"", i)[0]
                client_secret1 = temp
                if client_secret1 == "":
                    print("cks_push_alql_cilent_secret1 未填写")
            except:
                pass
    except:
        print("cks_push_alql_cilent_secret1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"cks_push_alql_url1=\"(.*?)\"", i)[0]
                url1 = temp
                if url1 == "":
                    print("cks_push_alql_url1 未填写")
            except:
                pass
    except:
        print("cks_push_alql_url1 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

try:
    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_client_ids=\[(.*?)\]", i)[0] + "]"
                try:
                    client_ids = json.loads(temp)
                except:
                    print("cks_push_alql_client_ids 填写有误")
                if client_ids == []:
                    print("cks_push_alql_client_ids 未填写")
            except:
                pass
    except:
        print("cks_push_alql_client_ids 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_client_secrets=\[(.*?)\]", i)[0] + "]"
                try:
                    client_secrets = json.loads(temp)
                except:
                    print("cks_push_alql_client_secrets 填写有误")
                if client_secrets == []:
                    print("cks_push_alql_client_secrets 未填写")
            except:
                pass
    except:
        print("cks_push_alql_client_secrets 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_urllist=\[(.*?)\]", i)[0] + "]"
                try:
                    urllist = json.loads(temp)
                except:
                    print("cks_push_alql_urllist 填写有误")
                if urllist == []:
                    print("cks_push_alql_urllist 未填写")
            except:
                pass
    except:
        print("cks_push_alql_urllist 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

try:
    try:
        for i in t:
            try:
                temp = re.findall(r"cks_push_alql_N_c=\"(.*?)\"", i)[0]
                try:
                    N_c = int(temp)
                except:
                    print("cks_push_alql_N_c 填写有误")
                if temp == "40":
                    print("cks_push_alql_N_c 未在ec_config.txt配置中更改，使用默认配置分发40")
            except:
                pass
    except:
        print("cks_push_alql_N_c 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

try:
    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_cilent_id_che=\[(.*?)\]", i)[0] + "]"
                client_id_che = json.loads(temp)
                if client_id_che == "":
                    print("cks_push_alql_cilent_id_che 未填写")
            except:
                pass
    except:
        print("cks_push_alql_cilent_id_che 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_cilent_secret_che=\[(.*?)\]", i)[0] + "]"
                client_secret_che = json.loads(temp)
                if client_secret_che == "":
                    print("cks_push_alql_cilent_secret_che 未填写")
            except:
                pass
    except:
        print("cks_push_alql_cilent_secret_che 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"cks_push_alql_che=\[(.*?)\]", i)[0] + "]"
                che = json.loads(temp)
                if che == "":
                    print("cks_push_alql_che 未填写")
            except:
                pass
    except:
        print("cks_push_alql_che 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, client_id_temp, client_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + client_id_temp + '&client_secret=' + client_secret_temp
    gettoken(self, url_token)


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


def update(self, baseurl, typ, text, qlid):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = {
        "name": "JD_COOKIE",
        "value": text,
        "_id": qlid
    }
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def insert(self, baseurl, typ, text):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    data_json = {
        "value": text,
        "name": "JD_COOKIE"
    }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    s = requests.session()
    login(s, url1, client_id1, client_secret1)
    wskeys = getitem(s, url1, "JD_COOKIE", "open")  # JD_COOKIE为默认转发的主青龙的环境变量名
    ck_list = []
    c_list = []
    for i in wskeys:
        tp = i['value']
        ptpin = re.findall(r"pt_pin=(.*?);", tp)[0]  # 默认获取的变量里的pt_pin=xxx;里的xxx
        ptpin = "pt_pin=" + ptpin + ';'
        ptkey = re.findall(r"pt_key=(.*?);", tp)[0]  # 默认获取的变量里的pt_key=xxxx;里的xxxx
        ptkey = "pt_key=" + ptkey + ';'
        c = ptkey + ptpin
        c_list.append(c)
        ck = ptkey + ptpin + '\n'
        ck_list.append(ck)
    if os.path.exists("./allck.txt"):
        os.remove("allck.txt")
    with open("./allck.txt", "w") as f:
        f.writelines(ck_list)
    count = 0
    temp = []
    ucount = 0
    for j in c_list:
        count += 1
        temp.append(j)
        if (count % N_c) == 0:  # 分配40个
            a = requests.session()
            url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_ids[ucount] + '&client_secret=' + \
                        client_secrets[ucount]
            gettoken(a, url_token)
            co = 0
            for k in temp:
                co += 1
                ptpin = re.findall(r"pt_pin=(.*?);", k)[0]
                ptpin = "pt_pin=" + ptpin
                item = getckitem(a, urllist[ucount], ptpin, "open")
                if item != []:
                    try:
                        qlid = item["_id"]
                    except:
                        qlid = item["id"]
                    if update(a, urllist[ucount], "open", k, qlid):
                        print("第%s个JD_COOKIE更新成功,pin为%s" % (co, ptpin[7:]))
                    else:
                        print("第%s个JD_COOKIE更新失败,pin为%s" % (co, ptpin[7:]))
                else:
                    if insert(a, urllist[ucount], "open", k):
                        print("第%s个JD_COOKIE添加成功" % co)
                    else:
                        print("第%s个JD_COOKIE添加失败" % co)
            temp = []
            ucount += 1
            print("第%s个容器更新成功" % ucount)
    a = requests.session()
    url_token = urllist[-1] + 'open/auth/token?client_id=' + client_ids[-1] + '&client_secret=' + client_secrets[-1]
    gettoken(a, url_token)
    co = 0

    if temp != []:  # 剩余放到最后一个容器里
        for k in temp:
            co += 1
            ptpin = re.findall(r"pt_pin=(.*?);", k)[0]
            ptpin = "pt_pin=" + ptpin
            item = getckitem(a, urllist[-1], ptpin, "open")
            if item != []:
                try:
                    qlid = item["_id"]
                except:
                    qlid = item["id"]
                if update(a, urllist[-1], "open", k, qlid):
                    print("第%s个JD_COOKIE更新成功,pin为%s" % (co, ptpin[7:]))
                else:
                    print("第%s个JD_COOKIE更新失败,pin为%s" % (co, ptpin[7:]))
            else:
                if insert(a, urllist[-1], "open", k):
                    print("第%s个JD_COOKIE添加成功" % co)
                else:
                    print("第%s个JD_COOKIE添加失败" % co)
        print("最后一个容器更新成功")
        print('分发CK完毕')
        print()
    else:
        print('分发CK完毕')
        print()

    for i in range(0, len(che)):
        b = requests.session()
        url_token = che[i] + 'open/auth/token?client_id=' + client_id_che[i] + '&client_secret=' + client_secret_che[i]
        gettoken(b, url_token)
        co = 0
        for chek in c_list:  # 备份ck
            co += 1
            ptpin = re.findall(r"pt_pin=(.*?);", chek)[0]
            ptpin = "pt_pin=" + ptpin
            item = getckitem(b, che[i], ptpin, "open")
            if item != []:
                try:
                    qlid = item["_id"]
                except:
                    qlid = item["id"]
                if update(b, che[i], "open", chek, qlid):
                    print("第%s个JD_COOKIE更新成功,pin为%s" % (co, ptpin[7:]))
                else:
                    print("第%s个JD_COOKIE更新失败,pin为%s" % (co, ptpin[7:]))
            else:
                if insert(b, che[i], "open", chek):
                    print("第%s个JD_COOKIE添加成功" % co)
                else:
                    print("第%s个JD_COOKIE添加失败" % co)
        print('备份容器{} 更新完毕\n'.format(i + 1))

    print("分发结束")
