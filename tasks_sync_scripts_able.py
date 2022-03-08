# -*- coding:utf-8 -*-
# 作者仓库:https://jihulab.com/spiritlhl/qinglong_auto_tools.git
# 觉得不错麻烦点个star谢谢
# 频道：https://t.me/qinglong_auto_tools
# 根据主青龙的启用任务和对应脚本同步到副青龙中去，不存在于副青龙中的任务和对应脚本会自动新增，如果启用的任务对应的脚本内容有更新，也会同步更新

# 只同步更新主青龙中已经启用的任务和对应脚本

'''
cron: 1
new Env('任务 二叉树同步脚本文件');
'''

# 在脚本管理里修改这个文件的配置，然后保存，然后禁用 二叉树同步脚本文件 这个任务，有需要再点运行
# 主青龙，任务获取更新的容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
# 副青龙，被同步的任务容器，事先需要在容器里创建应用，给所有权限，然后重启容器，应用设置才会生效，
# 按照格式有几个写几个，没有的空的删除
'''
# ec_config.txt中填写如下设置

# 二叉树同步脚本文件
### 主青龙
tasks_sync_scripts_able_cilent_id1="xxxxxxxx"
tasks_sync_scripts_able_cilent_secret1="xxxxxxxxxx"
tasks_sync_scripts_able_url1="http://xxxxxxxx:xxxx/"

### 副青龙
tasks_sync_scripts_able_client_ids=["",""]
tasks_sync_scripts_able_client_secrets=["",""]
tasks_sync_scripts_able_urllist=["http://xxxxxxxxx:xxxx/",""]

'''
# client_id1=""
# client_secret1=""
# url1 = ""
# client_ids=['','','','']
# client_secrets=['','','','']
# urllist = ["http://xxxx:xxxx/","","",'']

import re
import time
import json

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
                temp = re.findall(r"tasks_sync_scripts_able_cilent_id1=\"(.*?)\"", i)[0]
                client_id1 = temp
                if client_id1 == "":
                    print("tasks_sync_scripts_able_cilent_id1 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_cilent_id1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"tasks_sync_scripts_able_cilent_secret1=\"(.*?)\"", i)[0]
                client_secret1 = temp
                if client_secret1 == "":
                    print("tasks_sync_scripts_able_cilent_secret1 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_cilent_secret1 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = re.findall(r"tasks_sync_scripts_able_url1=\"(.*?)\"", i)[0]
                url1 = temp
                if url1 == "":
                    print("tasks_sync_scripts_able_url1 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_url1 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

try:
    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"tasks_sync_scripts_able_client_ids=\[(.*?)\]", i)[0] + "]"
                try:
                    client_ids = json.loads(temp)
                except:
                    print("tasks_sync_scripts_able_client_ids 填写有误")
                if client_ids == []:
                    print("tasks_sync_scripts_able_client_ids 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_client_ids 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"tasks_sync_scripts_able_client_secrets=\[(.*?)\]", i)[0] + "]"
                try:
                    client_secrets = json.loads(temp)
                except:
                    print("tasks_sync_scripts_able_client_secrets 填写有误")
                if client_secrets == []:
                    print("tasks_sync_scripts_able_client_secrets 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_client_secrets 未创建")
        exit(3)

    try:
        for i in t:
            try:
                temp = "[" + re.findall(r"tasks_sync_scripts_able_urllist=\[(.*?)\]", i)[0] + "]"
                try:
                    urllist = json.loads(temp)
                except:
                    print("tasks_sync_scripts_able_urllist 填写有误")
                if urllist == []:
                    print("tasks_sync_scripts_able_urllist 未填写")
            except:
                pass
    except:
        print("tasks_sync_scripts_able_urllist 未创建")
        exit(3)
except:
    print("找不到配置文件或配置文件有错误, 请填写ec_config.txt")

requests.packages.urllib3.disable_warnings()


def gettimestamp():
    return str(int(time.time() * 1500))


def gettoken(self, url_token):
    r = requests.get(url_token).text
    res = json.loads(r)["data"]["token"]
    self.headers.update({"Authorization": "Bearer " + res})


def login(self, baseurl, client_id_temp, client_secret_temp):
    url_token = baseurl + 'open/auth/token?client_id=' + client_id_temp + '&client_secret=' + client_secret_temp
    gettoken(self, url_token)


def getitem(self, baseurl, typ):
    url = baseurl + typ + "/scripts/files?t={}".format(gettimestamp())
    r = self.get(url)
    item = json.loads(r.text)["data"]
    return item


def getscript(self, baseurl, typ, filename, path):
    url = baseurl + typ + "/scripts/" + filename + "?t=%s" % gettimestamp()
    r = self.get(url)
    response = json.loads(r.text)["code"]
    if response == 500:
        url = baseurl + typ + "/scripts/" + filename + "?path=" + path
        r = self.get(url)
    script = json.loads(r.text)["data"]
    return script


def pushscript(self, baseurl, typ, data, path):
    url = baseurl + typ + "/scripts?t=%s" % gettimestamp()
    self.headers.update({"Content-Type": "application/json;charset=UTF-8", 'Connection': 'close'})
    r = self.put(url, data=json.dumps(data))
    response = json.loads(r.text)["code"]
    if response == 500:
        data["path"] = path
        r = self.put(url, data=json.dumps(data))
    return r.text


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


if __name__ == '__main__':
    # 主容器
    s = requests.session()
    login(s, url1, client_id1, client_secret1)

    # 获取主青龙任务
    print("=========== 主青龙 信息获取中 =============")
    print()
    ztasks = getcrons(s, url1, "open")
    zenable_list = []
    zdisable_list = []
    for i in ztasks:
        if i['isDisabled'] == 0:
            zenable_list.append(i)
        else:
            continue
    # enable_tlid = []
    zenable_tname = []
    zenable_tcommand = []
    zenable_tschedule = []
    for j in zenable_list:
        # enable_tlid.append(j['_id'])
        zenable_tname.append(j['name'])
        zenable_tcommand.append(j['command'])
        zenable_tschedule.append(j['schedule'])
    print("主青龙任务数量：{}，启用任务{}".format(len(ztasks), len(zenable_tname)))
    print()

    # 获取主青龙的脚本名
    ## 根目录
    zscripts = getitem(s, url1, "open")
    zscripts_list = []
    for i in zscripts:
        zscripts_list.append(i["key"])

    # script根目录默认存在的文件夹，放入其中的文件夹不再检索
    or_list = ['node_modules', '__pycache__', 'utils', '.pnpm-store', 'function', 'tools', 'backUp', '.git', '.idea']
    zpath_list = []
    zpath_scripts_list = []
    for i in zscripts:
        try:
            i["children"]
            if i["title"] not in or_list:
                zpath_list.append(i["title"])
                zpath_scripts_list.append(i["children"])
        except:
            pass

    print("主青龙根目录脚本文件数量：{}，".format(len(zscripts_list)))
    print("主青龙任务拉取的仓库对应目录文件夹数量：{}，".format(len(zpath_list)))
    print()
    print()

    # 创建对应文件夹字典
    dict_z = {}
    for i in zpath_list:
        dict_z[i] = []

    # 主青龙启用的任务对应的脚本
    zscripts_enable = []
    for i in zenable_tcommand:
        if i[-2:] == "js" or i[-2:] == "py":
            ti = i.replace("task ", "").split("/")
            if len(ti) == 1:
                zscripts_enable.append(ti[0])
            elif len(ti) == 2:
                dict_z[ti[0]].append(ti[1])

    t = 0
    for k in urllist:
        # 分容器
        print("=========== 副青龙{} 信息获取中 =============".format(t + 1))
        print()
        a = requests.session()
        login(a, urllist[t], client_ids[t], client_secrets[t])

        tasks = getcrons(a, urllist[t], "open")

        # 增加新任务
        enable_list = []
        disable_list = []
        for i in tasks:
            if i['isDisabled'] == 0:
                enable_list.append(i)
            else:
                continue
        # enable_tlid = []
        enable_tname = []
        enable_tcommand = []
        enable_tschedule = []
        for j in enable_list:
            # enable_tlid.append(j['_id'])
            enable_tname.append(j['name'])
            enable_tcommand.append(j['command'])
            enable_tschedule.append(j['schedule'])
        print("副青龙任务数量：{}".format(len(tasks)))
        print()

        print("同步任务中")
        print()

        count = 0
        ct = 0

        for i in zenable_tname:
            if zenable_tname[count] not in enable_tname and zenable_tcommand[count] not in enable_tcommand:
                data_cron = {
                    "command": zenable_tcommand[count],
                    "schedule": zenable_tschedule[count],
                    "name": zenable_tname[count]
                }
                addcron(a, urllist[t], "open", data_cron)
            else:
                ct += 1
            count += 1
        xc = count - ct
        print("新增启用任务数量：{}".format(xc))
        print()

        # 获取副青龙根目录脚本名
        scripts = getitem(a, urllist[t], "open")
        scripts_list = []
        for i in scripts:
            scripts_list.append(i["key"])

        # 获取副青龙仓库目录脚本名字典
        dict_cs_name = {}
        for i in zpath_list:
            dict_cs_name[i] = []
            for j in scripts:
                if j["key"] == i:
                    for k in j["children"]:
                        dict_cs_name[i].append(k["value"])

        # 筛选需要添加或更改的脚本名
        ## 根目录
        add_list = []
        change_list = []
        for j in zscripts_enable:
            if j not in scripts_list:
                add_list.append(j)
            else:
                change_list.append(j)

        ## 仓库目录
        dict_add_f = {}
        dict_change_f = {}
        for j in dict_z:
            dict_add_f[j] = []
            dict_change_f[j] = []
            for k in dict_z[j]:  # 在主青龙
                if k not in dict_cs_name[j]:  # 不在副青龙的文件
                    dict_add_f[j].append(k)
                else:
                    dict_change_f[j].append(k)

        print(dict_add_f)
        print(dict_change_f)

        print("同步脚本文件中")
        print()

        # 查询新增脚本内容
        ## 根目录
        data_script_list = []
        for i in add_list:
            content = getscript(s, url1, "open", i, "")
            data_script = {
                "filename": i,
                "content": content,
            }
            data_script_list.append(data_script)

        ## 仓库文件夹
        data_script_add_dict = {}
        for i in dict_add_f:
            data_script_add_dict[i] = []
            for j in dict_add_f[i]:  # j是文件名，i 是文件夹名
                content = getscript(s, url1, "open", j, i)
                data_script = {
                    "filename": j,
                    "content": content,
                    "path": i
                }
                data_script_add_dict[i].append(data_script)

        # 写入新增内容
        ## 根目录更新
        for i in data_script_list:
            pushscript(a, urllist[t], "open", i, "")

        ## 仓库文件夹更新
        cotu = 0
        for i in data_script_add_dict:
            for j in data_script_add_dict[i]:
                rc = pushscript(a, urllist[t], "open", j, j["path"])
                print(rc)
                cotu += 1
        print("新增启用任务对应脚本文件数量：{}".format(xc))
        print("新增启用任务对应仓库文件脚本数量：{}".format(cotu))
        print()

        print("同步脚本文件中")
        print()

        # 查询需要更改的脚本内容
        ## 根目录
        change_script_list = []
        for i in change_list:
            content = getscript(s, url1, "open", i, "")
            data_script = {
                "filename": i,
                "content": content,
            }
            change_script_list.append(data_script)

        origin_script_list = []
        for i in change_list:
            content = getscript(a, urllist[t], "open", i, "")
            data_script = {
                "filename": i,
                "content": content,
            }
            origin_script_list.append(data_script)

        ## 仓库文件字典
        change_script_dict = {}
        for i in dict_change_f:
            change_script_dict[i] = []
            for j in dict_change_f[i]:  # j是文件名，i 是文件夹名
                content = getscript(s, url1, "open", j, i)
                data_script = {
                    "filename": j,
                    "content": content,
                    "path": i
                }
                change_script_dict[i].append(data_script)

        origin_script_dict = {}
        for i in dict_change_f:
            origin_script_dict[i] = []
            for j in dict_change_f[i]:  # j是文件名，i 是文件夹名
                content = getscript(a, urllist[t], "open", j, i)
                data_script = {
                    "filename": j,
                    "content": content,
                    "path": i
                }
                origin_script_dict[i].append(data_script)

        # 比较后更新
        ## 根目录
        count = 0
        ct = 0
        while True:
            if count <= (len(change_script_list) - 1):
                if change_script_list[count] != origin_script_list[count]:
                    pushscript(a, urllist[t], "open", change_script_list[count], "")
                    print("更新脚本文件  {}".format(change_script_list[count]["filename"]))
                else:
                    ct += 1
                count += 1
            else:
                break
        ## 仓库文件
        for i, k in zip(change_script_dict, origin_script_dict):
            for j, l in zip(change_script_dict[i], origin_script_dict[k]):
                if j != l:
                    pushscript(a, urllist[t], "open", j, j["path"])
                    print("更新脚本文件  {}".format(j["filename"]))

        print()

        print("同步脚本文件完毕")
        t += 1

        print('========= 副青龙{} 同步信息完毕 ============='.format(t))
        print()








