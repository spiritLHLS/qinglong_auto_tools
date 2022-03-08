# tgts.py

#作者仓库:https://github.com/spiritLHL/qinglong_auto_tools 
#觉得不错麻烦点个star谢谢 

import time,random
import requests,os,json
import json
import re


client_id=['']
client_secret=['']
urllist = ["http://ip:5700/"]
tgAPI='tg机器人的token'
tgpd = 'tg群组名字'
tgpdid = 'tg群组id'
url = 'https://api.telegram.org/bot'+tgAPI+'/getupdates?offset=-1&chat_id='+tgpd

'''
使用方式：
tgbot.py和tgts.py文件放在青龙script文件夹下，配置好两文件后在青龙里添加任务
task tgts.py
定时给已经在tg机器人里绑定的号推送资产变动日志，自己定时
tgbot.py需要一直运行，建议在linux的screen会话窗口里启动，让程序一直运行

如果有报错，一定是没给777权限，tgbot生成的tgdata.txt文件也得给777权限
'''


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

def check(a,msg):
    global x
    x = 0
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


def tgpush_(res,tgAPI,tgpdid):
    push_url = 'https://api.telegram.org/bot'+tgAPI+'/sendMessage'
    data = {
        'chat_id':tgpdid,
        'text':res
    }
    requests.post(push_url,data=data)


curr_time = datetime.datetime.now()
ct = 1
print('已经启动')
with open('tgdata.txt',"r") as fp:
    tmps = fp.readlines()
count = len(tmps[1:])
tmpss = []
for o in tmps:
    tmpss.append(o.replace('\n',''))
for i in tmpss[1:]:
    try:
        tgid = i.split(',')[0]
        res = check(a,i)
        tgpush_(res,tgAPI,tgid)
        time.sleep(random.random())
        print('推送到tgid：{}成功'.format(tgid))
    except:
        print('推送失败')
print('推送结束')
