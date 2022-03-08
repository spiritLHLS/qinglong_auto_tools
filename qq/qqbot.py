# qqbot.py
# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
#觉得不错麻烦点个star谢谢

client_id=['']
client_secret=['']
urllist = ["http://青龙ip+端口/"]
tgAPI='tg机器人的api，形式：xxxx:xxxxxxxxxx'

from aiocqhttp import CQHttp, Event,Message, MessageSegment
import requests,os
import time,random
import json
import re

bot = CQHttp(api_root='http://127.0.0.1:5700')#go-cahttp部署的端口

requests.packages.urllib3.disable_warnings()
a = requests.session()

def gettimestamp():
    return str(int(time.time() * 1000))

def gettoken(self,url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer "+res})
    
def getckitem(self, baseurl, key, typ):
    url = baseurl + typ + "/envs?searchValue=JD_COOKIE&t=%s" % gettimestamp()
    r = self.get(url)
    for i in json.loads(r.text)["data"]:
        if key in i["value"]:
            return i
    return []

def getitem(self, baseurl, key , typ):
    url = baseurl + typ + "/envs?searchValue=%s&t=%s" % (key, gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item

def getlogs(self, baseurl, typ):
    url = baseurl + typ + "/logs"
    r = self.get(url)
    res = json.loads(r.text)["dirs"]
    return res

def getfiles(dirs, name):
    for i in dirs:
        if i['name'] == name:
            return i['files']
    return []

def getdetail(self,baseurl,files,filename):
    url = baseurl + "open/logs/"+files+'/'+filename+'/'
    r = a.get(url)
    return r.text

def push_QQ(userid,res_text,typ):
    data = {
    'user_id': userid,
    'message': res_text
    }
    requests.post('http://go-cqhttp机器人部署的ip:发信息的端口/'+typ,data)

def pre_check(userid):
    with open("data.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    Q_list=[]
    p_list=[]
    z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
        z_list.append(qwe[2])
    if str(userid) in Q_list:
        b = []
        for index, nums in enumerate(Q_list):
            if nums == str(userid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{},{}'.format(Q_list[j],p_list[j],z_list[j]))
        return c
    else:
        return 'error'

def check(a,msg):
    pin = msg.split(',')[1]
    name = msg.split(',')[2]
    ucount = 0
    url_token = urllist[ucount]+'open/auth/token?client_id='+client_id[ucount]+'&client_secret='+client_secret[ucount]
    gettoken(a, url_token)
    JDkeys = getitem(a, urllist[ucount], "JD_COOKIE" , "open")
    pin_list = []
    for i in JDkeys:
        tp = i['value']
        ptpin = re.findall(r"pt_pin=(.*?);", tp)[0]
        pin_list.append(ptpin)
    r = getlogs(a,urllist[ucount],'open')
    res = getfiles(r,'ccwav_QLScript_jd_bean_change')
    detail = getdetail(a,urllist[ucount],'ccwav_QLScript_jd_bean_change',res[0])
    pagetext = json.loads(detail)["data"]
    log1 = re.finditer('\u5065\u5eb7', pagetext)
    log1_list=[]
    for k in log1:
        log1_list.append(int(k.start()))
    log2 = re.finditer(name , pagetext)
    for j in log2:
        x = j.span()[1]-60
    y=log1_list[pin_list.index(pin)]
    result = pagetext[x:y+23]
    res_text = pagetext[10:30]+'查询的资产，定时每日12点更新当天资产\n'+result
    userid = msg.split(',')[0]
    push_type='send_private_msg'
    #push_QQ(userid,res_text,push_type)
    return res_text

def select_(chat):
    cht = chat.split(',')
    if not os.path.exists('data.txt'):
        with open("data.txt","w") as f:
            f.write("QQ,pin,zhuanghu")
    with open("data.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    Q_list=[]
    p_list=[]
    z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        p_list.append(qwe[1])
        z_list.append(qwe[2])
    if cht[1] in p_list:
        index = p_list.index(cht[1])
        #return '{},{},{}'.format(Q_list[index],p_list[index],z_list[index])
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("data.txt","a") as fe:
            fe.write("\n{},{},{}".format(cht[0],cht[1],cht[2]))
        return '{},{},{}'.format(cht[0],cht[1],cht[2])

def tg_select(chat):
    cht = chat.split(',')
    if not os.path.exists('tg.txt'):
        with open("tg.txt","w") as f:
            f.write("QQ,tg")
    with open("tg.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    Q_list=[]
    tg_list=[]
    for i in tmpss:
        tp = i.split(',')
        Q_list.append(tp[0])
        tg_list.append(tp[1])
    if cht[0] in Q_list:
        return '该QQ账号的tg已经被绑定了，请更换QQ账号'
    else:
        with open("tg.txt","a") as fe:
            fe.write("\n{},{}".format(cht[0],cht[1]))
        return "{},{}".format(cht[0],cht[1])

def tg_check_(cht):
    with open("tg.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    Q_list=[]
    tg_list=[]
    for i in tmpss:
        qwe = i.split(',')
        Q_list.append(qwe[0])
        tg_list.append(qwe[1])
    if cht in Q_list:
        index = Q_list.index(cht)
        return tg_list[index]
    else:
        return 'error'

def tgpush_(tg_id,res,tgAPI):
    #国内机子
    push_url = 'https://cloudfare代理的api端口/bot'+tgAPI+'/sendMessage'
    #国外机子这里的api是直接使用api.telegram.org即可
    data = {
        'chat_id':tg_id,
        'text':res
    }
    requests.post(push_url,data=data)

@bot.on_message
async def handle_msg(event):
    ms = Message(event.message)
    msg = str(ms)
    if msg == 'start':
        sm = '请按照提示操作\n增加QQ绑定   请以‘英文输入法’输入：\nQQ账号,京东的pin值,京东账户昵称\n格式例子：\n111111111,jd_xxxxxxx,yyyyyy\nqq增加tg绑定   请以‘英文输入法’输入：\nQQ账号,tg的用户id\ntg用户的id去tg搜@userinfobot私聊‘/start’获取\n查询   请输入‘check’\nQQ若有绑定tg，查询时qq和tg一起发消息给你\n查询结果显示api错误不用管，只是查不到过期京豆而已'
        await bot.send(event, sm)
    elif len(msg.split(',')) == 3:
        await bot.send(event, 'QQ绑定的账号增加中')
        response = select_(msg)
        if len(response.split(',')) == 3:
            await bot.send(event,'账号增加完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, response)
    elif len(msg.split(',')) == 2:
        await bot.send(event, 'QQ绑定的TG账号增加中')
        restg = tg_select(msg)
        if len(restg.split(',')) == 2:
            await bot.send(event,'TG绑定完毕，查询资产请输入‘check’')
        else:
            await bot.send(event, restg)
    elif msg == 'check':
        await bot.send(event, '查询中')
        userid = event['sender']['user_id']
        tg_data = tg_check_(str(userid))
        if tg_data == 'error':
            print('tg push error')
        else:
            tg_id = tg_data
        response = pre_check(userid)
        if response == 'error':
            await bot.send(event, '查询失败')
        else:
            for i in response:
                rest = check(a,i)
                tgpush_(tg_id,rest,tgAPI)
                await bot.send(event, str(rest))
    else:
        await bot.send(event, '命令输入错误，请输入‘start’仔细查看命令指南')
    await bot.send(event, '上述命令执行完毕，休息中')


bot.run(host='127.0.0.1', port=5701)#go-cahttp监听的端口
