import datetime, time, random
import requests, os, json
import json
import re

client_id = ['']
client_secret = ['']
urllist = ["http://xxxxx:xxx/"]


tgAPI = ''
tgpd = ''#群组名称
tgpdid = ''#号id
url = 'https://api.telegram.org/bot' + tgAPI + '/getupdates?offset=-1&chat_id=' + tgpd

requests.packages.urllib3.disable_warnings()
a = requests.session()


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
    id = json.loads(res1)["data"]["_id"]
    # print(res1)
    # 执行任务

    res2 = runcron(a, urllist[0], "open", [id])
    # print(res2)

    res3 = getstatus(a, urllist[0], "open", [id])

    while True:
        if json.loads(res3)["data"]["status"] == 0:
            msg = "还在查询中，请稍后"
            print(msg)
            time.sleep(2)
            res3 = getstatus(a, urllist[0], "open", [id])
        else:
            break

    time.sleep(1)
    res4 = getlogcron(a, urllist[0], "open", [id])

    # 查询结果
    result = json.loads(res4)["data"]

    # 删除任务
    res5 = deletecron(a, urllist[0], "open", [id])

    res_text = result[200:-60]
    return res_text


def tgpush_(res, tgAPI, tgpdid):
    push_url = 'https://api.telegram.org/bot' + tgAPI + '/sendMessage'
    data = {
        'chat_id': tgpdid,
        'text': res
    }
    requests.post(push_url, data=data)


curr_time = datetime.datetime.now()
login(a, urllist[0], client_id[0], client_secret[0])
ct = 1
print('已经启动')
with open('tgdata.txt', "r") as fp:
    tmps = fp.readlines()
count = len(tmps[1:])
tmpss = []
for o in tmps:
    tmpss.append(o.replace('\n', ''))
for i in tmpss[1:]:
    try:
        tgid = i.split(',')[0]
        res = check(a, i)
        tgpush_(res, tgAPI, tgid)
        time.sleep(random.random())
        print('推送到tgid：{}成功'.format(tgid))
    except:
        print('推送失败')
print('推送结束')
