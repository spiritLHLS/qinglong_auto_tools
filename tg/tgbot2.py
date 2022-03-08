# tgbot.py
import requests, os, json
import time, random
import json
import re

client_id = ['']
client_secret = ['']
urllist = ["http://xxxx:xxxx/"]
tgAPI = ''
tgpd = ''#群组名称
tgpdid = ''#群组id
url = 'https://api.telegram.org/bot' + tgAPI + '/getupdates?offset=-1&chat_id=' + tgpd

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, cilent_id_temp, cilent_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + cilent_id_temp + '&client_secret=' + cilent_secret_temp
    gettoken(self, url_token)


def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []


def getitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
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


def deletecron(self, baseurl, typ, data):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.delete(url, data=json.dumps(data))
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


def select_(chat):
    cht = chat.split(',')
    if not os.path.exists('tgdata.txt'):
        with open("tgdata.txt", "w") as f:
            f.write("tgid,pin,zhuanghu")
    with open("tgdata.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    tg_list = []
    p_list = []
    # z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        p_list.append(qwe[1])
        # z_list.append(qwe[2])
    if cht[1] in p_list:
        index = p_list.index(cht[1])
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("tgdata.txt", "a") as fe:
            fe.write("\n{},{}".format(cht[0], cht[1]))
        return '{},{}'.format(cht[0], cht[1])


def pre_check(tgid):
    with open("tgdata.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    tg_list = []
    p_list = []
    # z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        p_list.append(qwe[1])
        # z_list.append(qwe[2])
    if str(tgid) in tg_list:
        b = []
        for index, nums in enumerate(tg_list):
            if nums == str(tgid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{}'.format(tg_list[j], p_list[j]))
        return c
    else:

        return 'error'


def check(a, msg):
    global x
    x = 0
    pin = msg.split(',')[1]
    # name = msg.split(',')[2]
    cks = getitem(a, urllist[0], "JD_COOKIE", "open")
    res = getitem(a, urllist[0], pin, "open")
    weizhi = cks.index(res[0]) + 1
    data = {
        "command": "task ccwav_QLScript_jd_bean_change.js conc JD_COOKIE {}".format(str(weizhi)),
        "schedule": "1",
        "name": "查询"
    }
    # 创建任务
    res1 = addcron(a, urllist[0], "open", data)
    print(res1)
    id = json.loads(res1)["data"]["_id"]
    # print(res1)
    # 执行任务

    res2 = runcron(a, urllist[0], "open", [id])
    # print(res2)

    res3 = getstatus(a, urllist[0], "open", [id])
    print(res3)

    while True:
        if json.loads(res3)["data"]["status"] == 0:
            ms = "还在查询中,请稍后查看,等待8秒后检测查询结果"
            tgpush_(ms, tgAPI, tgpdid)
            time.sleep(8)
            res3 = getstatus(a, urllist[0], "open", [id])
        else:
            break

    time.sleep(1)
    res4 = getlogcron(a, urllist[0], "open", [id])

    # 查询结果
    result = json.loads(res4)["data"]
    print(result)

    # 删除任务
    res5 = deletecron(a, urllist[0], "open", [id])

    res_text = result[200:-60]
    return res_text


def tg_check(cht):
    with open("tgdata.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    tg_list = []
    pin_list = []
    # zh_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        pin_list.append(qwe[1])
        # zh_list.append(qwe[2])
    if cht in tg_list:
        index = tg_list.index(cht)
        return '{},{}'.format(tg_list[index], pin_list[index])
    else:
        return 'error'


def tgpush_(res, tgAPI, tgpdid):
    push_url = 'https://api.telegram.org/bot' + tgAPI + '/sendMessage'
    data = {
        'chat_id': tgpdid,
        'text': res
    }
    requests.post(push_url, data=data)


count = -1
while True:
    try:
        ori = requests.get(url)
        user = json.loads(ori.text)['result'][-1]['message']['from']['id']
        msg = json.loads(ori.text)['result'][-1]['message']['text']
        if msg == 'start':
            a = requests.session()
            login(a, urllist[0], client_id[0], client_secret[0])
            if count != 1:
                sm = '请按照提示操作\n增加tg绑定   请以‘英文输入法’输入：\ntg账号id,京东的pin值\n格式例子：\n111111111,jd_xxxxxxx\ntg用户的id去tg搜@userinfobot私聊‘/start’获取\n查询   请输入‘check’\n查询结果显示api错误不用管，只是查不到过期京豆而已\n每轮使用命令需要输入‘start’开始，每轮查询只有6秒命令输入时间，过期就下一轮了'
                tgpush_(sm, tgAPI, tgpdid)
                time.sleep(5)
                for i in range(6):
                    cot = 5 - i
                    tgpush_('命令等待执行倒计时{}秒'.format(cot), tgAPI, tgpdid)
                count = 1
            else:
                time.sleep(random.random() + random.randint(0, 3))
                count = 1
        elif (len(msg.split(',')) == 2) and (str(count) == '1'):
            tgpush_('tg绑定的账号增加中', tgAPI, tgpdid)
            response = select_(msg)
            if len(response.split(',')) == 2:
                tgpush_('账号增加完毕，请输入‘start’重新开始命令模式', tgAPI, tgpdid)
            else:
                tgpush_(response, tgAPI, tgpdid)
            count = 0
        elif (msg == 'check') and (str(count) == '1'):
            tgpush_('查询中', tgAPI, tgpdid)
            tg_data = tg_check(str(user))
            if tg_data == 'error':
                print('tg push error')
            else:
                tg_id = tg_data
            response = pre_check(str(user))
            if response == 'error':
                tgpush_('查询失败', tgAPI, tgpdid)
            else:
                for i in response:
                    rest = check(a, i)
                    tgpush_(rest, tgAPI, tgpdid)
                    time.sleep(0.3)
            tgpush_('查询完毕，下一位请输入‘start’开始下一轮命令', tgAPI, tgpdid)
            count = 0
        else:
            time.sleep(3)
            count = 0
    except:
        time.sleep(random.random() + random.randint(0, 2))
        count = -1
        continue
