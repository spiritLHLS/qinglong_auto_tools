# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools

'''
cron: 1
new Env('单容器 二叉树随机ck顺序');
'''

# 初次运行生成原始顺序模板文件 trigger_cookies.json，备份原始ck文件 allck.txt
# 可每次运行重新生成模板，在配置文件中配置 export ec_write_cks="true" 开启该功能
# 默认保持前6位ck顺序不变，有需要在配置文件中配置 export ec_head_cks="具体几个" 更改数量
# 可配置随机顺序时给ck备注标上原始顺序，如果备注已存在，则保留原始备注不更改
# 禁用的ck自动后置，非ck变量全部自动前置
# 默认任务定时自行修改


import os
import time
import json
import re
import random

print("不要在主容器运行！！！本脚本每运行一次少一个ck，请在分容器运行！！！")


try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)

requests.packages.urllib3.disable_warnings()

ql_auth_path = '/ql/config/auth.json'

try:
    head = int(os.environ["ec_head_cks"])
    print("已配置保留前{}位ck顺序做车头".format(head))
except:
    head = 6
    print("#默认只保留前6位ck做车头，有需求")
    print("#请在配置文件中配置\nexport ec_head_cks=\"具体几个\" \n#更改车头数量\n")

print("===================================")

print("已设置保留前{}位顺序不改变\n".format(head))


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


# 查询环境变量
def get_envs(name: str = None) -> list:
    params = {
        't': int(time.time() * 1000)
    }
    if name is not None:
        params['searchValue'] = name
    res = requests.get(ql_url + '/api/envs', headers=__get__headers(), params=params)
    j_data = res.json()
    if j_data['code'] == 200:
        return j_data['data']
    return []


def gettimestamp():
    return str(int(time.time() * 1000))


def gettoken(self):
    self.headers.update({"Authorization": "Bearer " + __get_token()})


def login(self):
    gettoken(self)


def getallenv(self, baseurl, typ):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


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


def update(self, baseurl, typ, value, qlid, remarks):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = {
        "name": "JD_COOKIE",
        "value": value,
        "_id": qlid,
        "remarks": remarks
    }
    r = self.put(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        data = {
            "name": "JD_COOKIE",
            "value": value,
            "id": qlid,
            "remarks": remarks
        }
        r = self.put(url, data=json.dumps(data))
        if json.loads(r.text)["code"] == 200:
            return True
        return False


def insert(self, baseurl, typ, name, value, remarks):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = []
    if remarks == None:
        data_json = {
            "value": value,
            "name": name
        }
    else:
        data_json = {
            "value": value,
            "name": name,
            'remarks': remarks
        }
    data.append(data_json)
    r = self.post(url, json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return r.json()['data']
    else:
        return False


def delete(self, baseurl, typ, value):
    url = baseurl + typ + "/envs?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    data = value
    r = self.delete(url, data=json.dumps(data))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


def disable(self, baseurl, typ, ids):
    url = baseurl + typ + "/envs/disable?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(ids))
    if json.loads(r.text)["code"] == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    s = requests.session()
    login(s)
    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    # # 备份ck
    # if os.path.exists("./allck.txt") == False:
    #     temp = []
    #     for i in cookies:
    #         temp.append(i["value"] + "\n")
    #     with open("./allck.txt", "w") as ffp:
    #         ffp.writelines(temp)
    #     print("初次运行，自动备份ck到allck.txt文件里，有需要恢复初始状态自取\n")
    # else:
    #     print("脚本管理根目录下allck.txt文件已存在，有需要恢复初始状态自取\n")
    #     pass

    # 备份
    tt = "trigger_cookies.json"
    allenv = getallenv(s, ql_url, "api")
    try:
        os.environ['ec_backup_ck']
        ec_backup_ck = os.environ['ec_backup_ck']
    except:
        ec_backup_ck = 'true'
    if ec_backup_ck == 'true' and os.path.exists('./' + tt) != True:
        with open(tt, "w", encoding="utf-8") as fp:
            json.dump(allenv, fp)
        print("已备份原有环境变量至{},有需要还原请使用二叉树还原环境变量脚本还原".format(tt))
        print("如果不需要备份，请设置export ec_backup_ck=\"false\"")
    else:
        print("上次备份文件{}还存在或已配置无需备份，本次运行不进行备份".format(tt))

    ####################################################################################

    try:
        ql_url = 'http://localhost:5700/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")
    except:
        ql_url = 'http://localhost:5600/'
        cookies = getitem(s, ql_url, "JD_COOKIE", "api")

    allenv = getallenv(s, ql_url, "api")
    jdcount = 0
    result_list = []
    he_list = []
    head_list = []
    random_list = []
    disable_list = []
    for i in allenv:
        if "JD_COOKIE" == i["name"]:
            jdcount += 1
        else:
            he_list.append(i)
            continue
        if jdcount <= head:
            head_list.append(i)
            continue
        if i["status"] != 0:
            disable_list.append(i)
            continue
    head_len = len(head_list) + len(he_list)
    # 随机化启用的cookie顺序，保留指定位置不变
    res = random.sample(range(head, len(cookies)), len(cookies) - head)
    print("固定的ck顺序")
    print("pin\t\t\t\t上次\t       本次")
    for i in range(0, head):
        c = re.findall(r"pt_pin=(.*?);", cookies[i]["value"])[0][-16:].ljust(16)
        print("{}\t\t{}\t\t{}".format(c, i + 1, i + 1))
    print("本次随机ck的顺序")
    print("pin\t\t\t\t上次\t       本次")
    temp = []
    ct = 1
    for i in res:
        random_list.append(cookies[i - 1])
        c = re.findall(r"pt_pin=(.*?);", cookies[i - 1]["value"])[0][-16:].ljust(16)
        print("{}\t\t{}\t\t{}".format(c, i, ct + head))
        ct += 1

    result_list.extend(head_list)

    # 与后置黑号脚本匹配
    tp1 = []
    tp2 = []
    try:
        ec_blackkey = os.environ["ec_blackkey"]
        for i in random_list:
            try:
                if i['remarks'] == ec_blackkey:
                    tp2.append(i)
                else:
                    tp1.append(i)
            except:
                tp1.append(i)
        random_list = tp1 + tp2
    except:
        pass
    tp1 = []
    tp2 = []
    try:
        for i in random_list:
            try:
                if i['remarks'] == '黑号':
                    tp2.append(i)
                else:
                    tp1.append(i)
            except:
                tp1.append(i)
        random_list = tp1 + tp2
    except:
        pass

    # 去重
    tp1 = []
    value_tp = []
    for i in random_list:
        if i['value'] not in value_tp:
            tp1.append(i)
            value_tp.append(i['value'])
    random_list = tp1
    he_count = len(he_list)
    result_list.extend(random_list)
    result_list.extend(disable_list)

    # 去重
    tp1 = []
    value_tp = []
    for i in result_list:
        if i['value'] not in value_tp:
            tp1.append(i)
            value_tp.append(i['value'])
    result_list = tp1

    he_list.extend(result_list)
    result_list = he_list

    for i in allenv:
        try:
            c = delete(s, ql_url, "api", [i['_id']])
        except:
            c = delete(s, ql_url, "api", [i['id']])
    time.sleep(2)
    print(len(result_list))
    for i in result_list:
        try:
            i['remarks']
            c = insert(s, ql_url, "api", i['name'], i['value'], i['remarks'])
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
        except:
            c = insert(s, ql_url, "api", i['name'], i['value'], None)
            if i["status"] != 0:
                try:
                    disable(s, ql_url, 'api', [c[0]['_id']])
                except:
                    disable(s, ql_url, 'api', [c[0]['id']])
    print("已前置非ck变量共{}个，车头ck共{}个，随机顺序ck共{}个，后置禁用ck共{}个".format(he_count, len(head_list), len(random_list),
                                                               len(disable_list)))
    print("============================================")
    print("脚本执行完毕")