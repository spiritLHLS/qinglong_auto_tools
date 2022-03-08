# qqbot.py
# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢

client_id = ["", ""]
client_secret = ["", ""]
urllist = ["http://xxxxxx:xxxx/", "http://xxx:xxxx/"]
zQQ = ""

from aiocqhttp import CQHttp, Event, Message, MessageSegment
from apscheduler.schedulers.background import BackgroundScheduler
import requests, os
import time, random
import json
import re
import datetime

bot = CQHttp(api_root='http://127.0.0.1:5700')  # go-cahttp部署的端口

requests.packages.urllib3.disable_warnings()
a = requests.session()
scheduler = BackgroundScheduler()
scheduler.start()
status_c = 0


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


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


def gettaskitem(self, baseurl, typ):
    url = baseurl + typ + "/crons?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def ckup(wskey):
    pt_key = re.findall(r"wskey=(.*?);", wskey)[0]
    pt_key = "pt_key=" + pt_key + ";"
    k = re.finditer("wskey=", wskey)
    for j in k:
        t = j.span()[1]
    pt_pin = 'pt_' + wskey[0:t - 7] + ';'
    ck = pt_pin + pt_key + wskey.split(';')[1] + ';'
    return ck


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


def push_QQ(userid, res_text, typ):
    data = {
        'user_id': userid,
        'message': res_text
    }
    requests.post('http://xxxxx:xxxx/' + typ, data)


def pre_check(userid):
    with open("data.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    p_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
    if str(userid) in Q_list:
        b = []
        for index, nums in enumerate(Q_list):
            if nums == str(userid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{}'.format(Q_list[j], p_list[j]))
        return c
    else:
        return 'error'


def check(a, msg, push_type):
    userid = msg[0]
    pin = msg[1:]
    # name = msg.split(',')[2]
    
    msg1 = "还在查询中,请耐心等待,16秒刷新一次状态,运行中不再返回查询状态"
    push_QQ(userid, msg1, push_type)

    ucount = 0
    url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_id[ucount] + '&client_secret=' + client_secret[
        ucount]
    gettoken(a, url_token)
    ztasks = gettaskitem(a, urllist[ucount], "open")
    enable_list = []
    for i in ztasks:
        if i['isDisabled'] == 0:
            enable_list.append(i)
    enable_tlid = []
    enable_tname = []
    enable_tcommand = []
    for j in enable_list:
        enable_tlid.append(j['_id'])
        enable_tname.append(j['name'])
        enable_tcommand.append(j['command'])
    count = 0
    for i in enable_tname:
        if i == "查询":
            id = enable_tlid[count]
        count += 1
    try:
        res3 = getstatus(a, urllist[ucount], "open", [id])
        if json.loads(res3)["data"]["status"] == 0 or json.loads(res3)["data"]["status"] == 1:
            push_QQ(userid, "上一位用户还在查询，本次查询将强制停止上一位用户查询的进程", push_type)
        # 删除任务
            deletecron(a, urllist[0], "open", [id])
            time.sleep(2)
    except:
        pass
    
    
    weiz = []
    for k in pin:
        cks = getitem(a, urllist[0], "JD_COOKIE", "open")
        res = getitem(a, urllist[0], k, "open")
        weizhi = cks.index(res[0]) + 1
        weiz.append(weizhi)

    wzz = ""
    for kk in weiz:
        wzz = wzz + " " + str(kk)
    data = {
        "command": "task ccwav_QLScript_jd_bean_change.js conc JD_COOKIE" + str(wzz),
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
        try:
            if json.loads(res3)["data"]["status"] == 0:
                time.sleep(16)
                res3 = getstatus(a, urllist[0], "open", [id])
            else:
                break
        except:
            break

    time.sleep(1)
    try:
        res4 = getlogcron(a, urllist[0], "open", [id])

        # 查询结果
        result = json.loads(res4)["data"]

        # 删除任务
        deletecron(a, urllist[0], "open", [id])

        # 发送消息
        res_text = str(result)[10:-55]
        res_text = res_text.replace("京东", "狗东")
        res_text = res_text.replace("红包", "red包")
        res_text = res_text.replace("京豆", "Jin豆")
        res_text = res_text.replace("收入", "入")

        push_QQ(userid, res_text, push_type)
    except:
        push_QQ(userid, "{}查询被后来者中断".format(userid), push_type)




def select_(chat):
    cht = chat.split(',')
    if not os.path.exists('data.txt'):
        with open("data.txt", "w") as f:
            f.write("QQ,pin,zhuanghu")
    with open("data.txt", "r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n', ''))
    Q_list = []
    p_list = []
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
    if cht[1] in p_list:
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("data.txt", "a") as fe:
            fe.write("\n{},{}".format(cht[0], cht[1]))
        return '{},{}'.format(cht[0], cht[1])


# 服务器1
def command_s(name):
    ucount = 0
    url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_id[ucount] + '&client_secret=' + client_secret[
        ucount]
    gettoken(a, url_token)
    ztasks = gettaskitem(a, urllist[ucount], "open")
    disable_list = []
    for i in ztasks:
        if i['isDisabled'] != 0:
            disable_list.append(i)
    disable_tlid = []
    disable_tname = []
    disable_tcommand = []
    for j in disable_list:
        disable_tlid.append(j['_id'])
        disable_tname.append(j['name'])
        disable_tcommand.append(j['command'])
    count = 0
    for i in disable_tname:
        if i == name:
            id = disable_tlid[count]
        count += 1
    res2 = runcron(a, urllist[ucount], "open", [id])
    res3 = getstatus(a, urllist[ucount], "open", [id])
    push_QQ(zQQ, "已添加到任务列表运行中，完成后返回日志", 'send_private_msg')
    while True:
        if json.loads(res3)["data"]["status"] == 0:
            time.sleep(8)
            res3 = getstatus(a, urllist[ucount], "open", [id])
        else:
            break
    time.sleep(1)
    res4 = getlogcron(a, urllist[ucount], "open", [id])
    ms = json.loads(res4)["data"][-100:-40] + "\n来自上海服务器"
    push_QQ(zQQ, ms, 'send_private_msg')


# 服务器2
def command_x(name):
    ucount = 1
    x = requests.session()
    url_token = urllist[ucount] + 'open/auth/token?client_id=' + client_id[ucount] + '&client_secret=' + client_secret[
        ucount]
    gettoken(x, url_token)
    ztasks = gettaskitem(x, urllist[ucount], "open")
    disable_list = []
    for i in ztasks:
        if i['isDisabled'] != 0:
            disable_list.append(i)
    disable_tlid = []
    disable_tname = []
    disable_tcommand = []
    for j in disable_list:
        disable_tlid.append(j['_id'])
        disable_tname.append(j['name'])
        disable_tcommand.append(j['command'])
    count = 0
    for i in disable_tname:
        if i == name:
            id = disable_tlid[count]
        count += 1
    res2 = runcron(x, urllist[ucount], "open", [id])
    res3 = getstatus(x, urllist[ucount], "open", [id])
    push_QQ(zQQ, "已添加到任务列表运行中，完成后返回日志", 'send_private_msg')
    while True:
        if json.loads(res3)["data"]["status"] == 0:
            time.sleep(8)
            res3 = getstatus(x, urllist[ucount], "open", [id])
        else:
            break
    time.sleep(1)
    res4 = getlogcron(x, urllist[ucount], "open", [id])
    ms = json.loads(res4)["data"][-100:-40] + "\n来自香港服务器"
    push_QQ(zQQ, ms, 'send_private_msg')


@bot.on_message
async def handle_msg(event):
    ms = Message(event.message)
    msg = str(ms)
    global status_c
    if msg == 'start':
        sm = '请按照提示操作\n增加QQ绑定   请以‘英文输入法’输入：\nQQ账号,京东的pin值\n格式例子：\n111111111,jd_xxxxxxx\n查询   请输入‘check’\n查询结果显示api错误不用管，只是查不到过期京豆而已\n如果有用户正在查询，会占用查询导致你check没有回应，这是正常现象，见谅'
        await bot.send(event, sm)
    elif len(msg.split(',')) == 2:
        await bot.send(event, 'QQ绑定的账号增加中')
        response = select_(msg)
        if len(response.split(',')) == 2:
            await bot.send(event, '账号增加完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, response)
        # 1
    elif msg == 'common1' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用开卡[普通]",), next_run_time=datetime.datetime.now())
    elif msg == 'game1' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用京东游戏",), next_run_time=datetime.datetime.now())
    elif msg == 'collect1' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用集卡",), next_run_time=datetime.datetime.now())
    elif msg == '16001' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用开卡[1600]",), next_run_time=datetime.datetime.now())
    elif msg == 'video1' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用京东视频狂得京豆",), next_run_time=datetime.datetime.now())
    elif msg == 'share1' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_s, args=("通用分享",), next_run_time=datetime.datetime.now())
        # 2
    elif msg == 'common2' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用开卡[普通]",), next_run_time=datetime.datetime.now())
    elif msg == 'game2' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用京东游戏",), next_run_time=datetime.datetime.now())
    elif msg == 'collect2' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用集卡",), next_run_time=datetime.datetime.now())
    elif msg == '16002' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用开卡[1600]",), next_run_time=datetime.datetime.now())
    elif msg == 'video2' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用京东视频狂得京豆",), next_run_time=datetime.datetime.now())
    elif msg == 'share2' and str(event['sender']['user_id']) == zQQ:
        scheduler.add_job(func=command_x, args=("通用分享",), next_run_time=datetime.datetime.now())
        # 1
    elif msg == 'check':
        userid = event['sender']['user_id']
        response = pre_check(userid)
        if response == 'error':
            await bot.send(event, '查询失败')
        else:
            idss = []
            idss.append(response[0].split(",")[0])
            for i in response:
                idss.append(i.split(",")[1])
            scheduler.add_job(func=check, args=(a, idss), next_run_time=datetime.datetime.now())
            await bot.send(event, '正在后台查询中,请勿重复输入命令')
    elif (msg[0] == 'p'):
        print('ck  ')
        ck = ckup(msg)
        push_QQ(zQQ, ck, 'send_private_msg')
        print(ck)
    else:
        await bot.send(event, '命令输入错误，请输入‘start’仔细查看命令指南')
    await bot.send(event, '上述命令执行完毕，休息中')


bot.run(host='127.0.0.1', port=5701)  # go-cahttp监听的端口

