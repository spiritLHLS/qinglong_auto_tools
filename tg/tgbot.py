# tgbot.py

#作者仓库:https://github.com/spiritLHL/qinglong_auto_tools 
#觉得不错麻烦点个star谢谢 

import requests,os,json
import time,random
import json
import re


client_id=['']
client_secret=['']
urllist = ["http://ip:5700/"]
tgAPI='tg机器人的token'
tgpd = 'tg群组名字'
tgpdid = 'tg群组id'
url = 'https://api.telegram.org/bot'+tgAPI+'/getupdates?offset=-1&chat_id='+tgpd


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

def select_(chat):
    cht = chat.split(',')
    if not os.path.exists('tgdata.txt'):
        with open("tgdata.txt","w") as f:
            f.write("tgid,pin,zhuanghu")
    with open("tgdata.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    tg_list=[]
    p_list=[]
    z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        p_list.append(qwe[1])
        z_list.append(qwe[2])
    if cht[1] in p_list:
        index = p_list.index(cht[1])
        return '该京东账号的pin已经被绑定了，请更换绑定账号'
    else:
        with open("tgdata.txt","a") as fe:
            fe.write("\n{},{},{}".format(cht[0],cht[1],cht[2]))
        return '{},{},{}'.format(cht[0],cht[1],cht[2])

def getdetail(self,baseurl,files,filename):
    url = baseurl + "open/logs/"+files+'/'+filename+'/'
    r = a.get(url)
    return r.text

def pre_check(tgid):
    with open("tgdata.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    tg_list=[]
    p_list=[]
    z_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        p_list.append(qwe[1])
        z_list.append(qwe[2])
    if str(tgid) in tg_list:
        b = []
        for index, nums in enumerate(tg_list):
            if nums == str(tgid):
                b.append(index)
        c = []
        for j in b:
            c.append('{},{},{}'.format(tg_list[j],p_list[j],z_list[j]))
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
    return res_text

def tg_check(cht):
    with open("tgdata.txt","r") as fi:
        tmps = fi.readlines()
    tmpss = []
    for o in tmps:
        tmpss.append(o.replace('\n',''))
    tg_list=[]
    pin_list=[]
    zh_list=[]
    for i in tmpss:
        qwe = i.split(',')
        tg_list.append(qwe[0])
        pin_list.append(qwe[1])
        zh_list.append(qwe[2])
    if cht in tg_list:
        index = tg_list.index(cht)
        return '{},{},{}'.format(tg_list[index],pin_list[index],zh_list[index])
    else:
        return 'error'

def tgpush_(res,tgAPI,tgpdid):
    push_url = 'https://api.telegram.org/bot'+tgAPI+'/sendMessage'
    data = {
        'chat_id':tgpdid,
        'text':res
    }
    requests.post(push_url,data=data)

count = -1
while True:
    try:
        ori = requests.get(url)
        user = json.loads(ori.text)['result'][-1]['message']['from']['id']
        msg = json.loads(ori.text)['result'][-1]['message']['text']
        if msg == 'start':
            if count != 1:
                sm = '请按照提示操作\n增加tg绑定   请以‘英文输入法’输入：\ntg账号id,京东的pin值,京东账户昵称\n格式例子：\n111111111,jd_xxxxxxx,yyyyyy\ntg用户的id去tg搜@userinfobot私聊‘/start’获取\n查询   请输入‘check’\n查询结果显示api错误不用管，只是查不到过期京豆而已\n每轮使用命令需要输入‘start’开始，每轮查询只有6秒命令输入时间，过期就下一轮了'
                tgpush_(sm,tgAPI,tgpdid)
                time.sleep(5)
                for i in range(6):
                    cot = 5 - i
                    tgpush_('命令等待执行倒计时{}秒'.format(cot),tgAPI,tgpdid)
                count = 1
            else:
                time.sleep(random.random()+random.randint(0,3))
                count = 1
        elif (len(msg.split(',')) == 3) and (str(count) == '1'):
            tgpush_('tg绑定的账号增加中',tgAPI,tgpdid)
            response = select_(msg)
            if len(response.split(',')) == 3:
                tgpush_('账号增加完毕，请输入‘start’重新开始命令模式',tgAPI,tgpdid)
            else:
                tgpush_(response,tgAPI,tgpdid)
            count = 0
        elif (msg == 'check') and (str(count) == '1'):
            tgpush_('查询中',tgAPI,tgpdid)
            tg_data = tg_check(str(user))
            if tg_data == 'error':
                print('tg push error')
            else:
                tg_id = tg_data
            response = pre_check(str(user))
            if response == 'error':
                tgpush_('查询失败',tgAPI,tgpdid)
            else:
                for i in response:
                    rest = check(a,i)
                    tgpush_(rest,tgAPI,tgpdid)
            tgpush_('查询完毕，下一位请输入‘start’开始下一轮命令',tgAPI,tgpdid)
            count = 0
        else:
            time.sleep(3)
            count = 0
    except:
        time.sleep(random.random()+random.randint(0,2))
        count = -1
        continue
