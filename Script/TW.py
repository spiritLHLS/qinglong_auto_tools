# -*- coding: utf-8 -*
# 修改自https://github.com/Zy143L/wskey
# 本地使用版本
# input.txt放入以&间隔的wsck
# 运行后output.txt出来以&间隔的ck
# 个人使用，勿喷，勿询问用法或者其他问题
# By spiritlhl
# version 10114

import socket
import base64
import http.client
import json
import os
import sys
import logging
import time
import urllib.parse

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
try:
    import requests
except Exception as e:
    logger.info(str(e) + "\n缺少requests模块, 请执行命令：pip3 install requests\n")
    sys.exit(1)
os.environ['no_proxy'] = '*'
requests.packages.urllib3.disable_warnings()

ver = 10114



# 返回值 list[wskey]
def get_wskey():
    with open("input.txt", "r") as fp:
        wskey_list = fp.read().split("\n")
    if len(wskey_list) > 0:
        return wskey_list
    else:
        logger.info("JD_WSCK变量未启用")
        sys.exit(1)


# 返回值 list[jd_cookie]
def get_ck():
    with open("ttcks.txt", "r") as fp:
        cks = fp.read().split("\n")
    if len(cks) >= 1:
        return cks
    else:
        logger.info("JD_COOKIE变量未启用")
        sys.exit(1)


# 返回值 bool
def check_ck(ck):
    if "QL_WSCK" in os.environ:
        logger.info("不检查账号有效性\n--------------------\n")
        return False
    else:
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
        headers = {
            'Cookie': ck,
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'user-agent': ua
        }
        try:
            res = requests.get(url=url, headers=headers, verify=False, timeout=10)
        except:
            # logger.info("JD接口错误, 切换第二接口")
            url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion'
            headers = {
                'Cookie': ck,
                'user-agent': ua,
                'Referer': 'https://home.m.jd.com/myJd/home.action'
            }
            res = requests.get(url=url, headers=headers, verify=False, timeout=30)
            if res.status_code == 200:
                code = int(json.loads(res.text)['retcode'])
                pin = ck.split(";")[1]
                if code == 0:
                    logger.info(str(pin) + ";状态正常\n")
                    return True
                else:
                    logger.info(str(pin) + ";状态失效\n")
                    return False
            else:
                logger.info("JD接口错误码: " + str(res.status_code))
                return False
        else:
            if res.status_code == 200:
                code = int(json.loads(res.text)['retcode'])
                pin = ck.split(";")[1]
                if code == 0:
                    logger.info(str(pin) + ";状态正常\n")
                    return True
                else:
                    logger.info(str(pin) + ";状态失效\n")
                    return False
            else:
                logger.info("JD接口错误码: " + str(res.status_code))
                return False


# 返回值 bool jd_ck
def getToken(wskey):
    headers = {
        'cookie': wskey,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'charset': 'UTF-8',
        'accept-encoding': 'br,gzip,deflate',
        'user-agent': ua
    }
    params = {
        'functionId': 'genToken',
        'clientVersion': '10.2.2',
        'client': 'android',
        'uuid': uuid,
        'st': st,
        'sign': sign,
        'sv': sv
    }
    url = 'https://api.m.jd.com/client.action'
    data = 'body=%7B%22action%22%3A%22to%22%2C%22to%22%3A%22https%253A%252F%252Fplogin.m.jd.com%252Fcgi-bin%252Fm%252Fthirdapp_auth_page%253Ftoken%253DAAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg%2526client_type%253Dandroid%2526appid%253D879%2526appup_type%253D1%22%7D&'
    try:
        res = requests.post(url=url, params=params, headers=headers, data=data, verify=False, timeout=10)
        res_json = json.loads(res.text)
        tokenKey = res_json['tokenKey']
    except:
        logger.info("WSKEY转换接口出错, 请稍后尝试, 脚本退出")
        sys.exit(1)
    else:
        return appjmp(wskey, tokenKey)


# 返回值 bool jd_ck
def appjmp(wskey, tokenKey):
    headers = {
        'User-Agent': ua,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    }
    params = {
        'tokenKey': tokenKey,
        'to': 'https://plogin.m.jd.com/cgi-bin/m/thirdapp_auth_page?token=AAEAIEijIw6wxF2s3bNKF0bmGsI8xfw6hkQT6Ui2QVP7z1Xg',
        'client_type': 'android',
        'appid': 879,
        'appup_type': 1,
    }
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp'
    try:
        res = requests.get(url=url, headers=headers, params=params, verify=False, allow_redirects=False, timeout=20)
        res_set = res.cookies.get_dict()
        pt_key = 'pt_key=' + res_set['pt_key']
        pt_pin = 'pt_pin=' + res_set['pt_pin']
        jd_ck = str(pt_key) + ';' + str(pt_pin) + ';'
        wskey = wskey.split(";")[0]
        if 'fake' in pt_key:
            logger.info(str(wskey) + ";WsKey状态失效\n")
            return False, jd_ck
        else:
            logger.info(str(wskey) + ";WsKey状态正常\n")
            return True, jd_ck
    except:
        logger.info("JD接口转换失败, 默认WsKey失效\n")
        wskey = "pt_" + str(wskey.split(";")[0])
        print(wskey)
        return False, wskey


# 返回值 svv, stt, suid, jign
def get_sign():
    url = str(base64.b64decode(url_t).decode()) + 'wskey'
    for i in range(3):
        try:
            headers = {
                "User-Agent": ua
            }
            res = requests.get(url=url, headers=headers, verify=False, timeout=20)
        except requests.exceptions.ConnectTimeout:
            logger.info("\n获取Sign超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except requests.exceptions.ReadTimeout:
            logger.info("\n获取Sign超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except Exception as err:
            logger.info(str(err) + "\n未知错误, 重试脚本!")
            continue
        else:
            try:
                sign_list = json.loads(res.text)
            except:
                logger.info("Sign Json错误")
                sys.exit(1)
            else:
                svv = sign_list['sv']
                stt = sign_list['st']
                suid = sign_list['uuid']
                jign = sign_list['sign']
                return svv, stt, suid, jign


# 返回值 None
def boom():
    ex = int(cloud_arg['code'])
    if ex != 200:
        logger.info("Check Failure")
        logger.info("--------------------\n")
        sys.exit(0)
    else:
        logger.info("Verification passed")
        logger.info("--------------------\n")


def update():
    up_ver = int(cloud_arg['update'])
    if ver >= up_ver:
        logger.info("当前脚本版本: " + str(ver))
        logger.info("--------------------\n")
    else:
        logger.info("当前脚本版本: " + str(ver) + "新版本: " + str(up_ver))
        logger.info("存在新版本, 请更新脚本后执行")
        logger.info("--------------------\n")
        text = '当前脚本版本: {0}新版本: {1}, 请更新脚本~!'.format(ver, up_ver)
        print(text)
        # sys.exit(0)


def ql_check(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect(('127.0.0.1', port))
    except:
        sock.close()
        return False
    else:
        sock.close()
        return True


# 返回值 bool, key, eid
def serch_ck(pin):
    if all('\u4e00' <= char <= '\u9fff' for char in pin):
        pin1 = urllib.parse.quote(pin)
        pin2 = pin1.replace('%', '%5C%25')
        logger.info(str(pin) + "-->" + str(pin1))
    else:
        pin2 = pin.replace('%', '%5C%25')
    with open("ttcks.txt", "r") as fp:
        cks = fp.read().split('\n')
    for i in cks:
        if pin in i:
            value = i
    logger.info(str(pin) + "检索成功\n")
    try:
        key = value
        eid = 1
        return True, key, eid
    except:
        return False, 1




def cloud_info():
    url = str(base64.b64decode(url_t).decode()) + 'check_api'
    for i in range(3):
        try:
            headers = {
                "authorization": "Bearer Shizuku"
            }
            res = requests.get(url=url, verify=False, headers=headers, timeout=20).text
        except requests.exceptions.ConnectTimeout:
            logger.info("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except requests.exceptions.ReadTimeout:
            logger.info("\n获取云端参数超时, 正在重试!" + str(i))
            time.sleep(1)
            continue
        except Exception as err:
            logger.info(str(err) + "\n未知错误云端, 退出脚本!")
            sys.exit(1)
        else:
            try:
                c_info = json.loads(res)
            except:
                logger.info("云端参数解析失败")
                sys.exit(1)
            else:
                return c_info


def check_cloud():
    url_list = ['aHR0cDovLzQzLjEzNS45MC4yMy8=', 'aHR0cHM6Ly9zaGl6dWt1Lm1sLw==', 'aHR0cHM6Ly9jZi5zaGl6dWt1Lm1sLw==']
    for i in url_list:
        url = str(base64.b64decode(i).decode())
        try:
            res = requests.get(url=url, verify=False, timeout=10)
        except:
            continue
        else:
            info = ['Default', 'HTTPS', 'CloudFlare']
            logger.info(str(info[url_list.index(i)]) + " Server Check OK\n--------------------\n")
            return i
    logger.info("\n云端地址全部失效, 请检查网络!")
    try:
        print('WSKEY转换', '云端地址失效. 请检查网络.')
    except:
        logger.info("通知发送失败")
    sys.exit(1)



if __name__ == '__main__':
    tp = ""
    with open("output.txt", "w") as fp:
        fp.write(tp)
    logger.info("\n--------------------\n")
    url_t = check_cloud()
    cloud_arg = cloud_info()
    update()
    boom()
    ua = cloud_arg['User-Agent']
    sv, st, uuid, sign = get_sign()
    wslist = get_wskey()
    for ws in wslist:
        wspin = ws.split(";")[0]
        if "pin" in wspin:
            wspin = "pt_" + wspin + ";"  # 封闭变量
            return_serch = serch_ck(wspin)  # 变量 pt_pin 搜索获取 key eid
            if return_serch[0]:  # bool: True 搜索到账号
                jck = str(return_serch[1])  # 拿到 JD_COOKIE
                if not check_ck(jck):  # bool: False 判定 JD_COOKIE 有效性
                    return_ws = getToken(ws)  # 使用 WSKEY 请求获取 JD_COOKIE bool jd_ck
                    if return_ws[0]:  # bool: True
                        nt_key = str(return_ws[1])
                        with open("output.txt", "a") as fp:
                            fp.write(nt_key + "\n")
                        # logger.info("wskey转pt_key成功", nt_key)
                        logger.info("wskey转换成功")
                        eid = return_serch[2]  # 从 return_serch 拿到 eid
                        # ql_update(eid, nt_key)  # 函数 ql_update 参数 eid JD_COOKIE
                    else:
                        # logger.info(str(wspin) + "wskey失效\n")
                        eid = return_serch[2]
                        logger.info(str(wspin) + "账号禁用")
                        # ql_disable(eid)
                        # dd = serch_ck(ws)[2]
                        # ql_disable(dd)
                        text = "账号: {0} WsKey失效, 已禁用Cookie".format(wspin)
                        try:
                            print('WsKey转换脚本', text)
                        except:
                            logger.info("通知发送失败")
                else:
                    logger.info(str(wspin) + "账号有效")
                    eid = return_serch[2]
                    # ql_enable(eid)
                    logger.info("--------------------\n")
            else:
                logger.info("\n新wskey\n")
                return_ws = getToken(ws)  # 使用 WSKEY 请求获取 JD_COOKIE bool jd_ck
                if return_ws[0]:
                    nt_key = str(return_ws[1])
                    logger.info("wskey转换成功\n")
                    # ql_insert(nt_key)
                    with open("output.txt", "a") as fp:
                        fp.write(nt_key+"\n")
        else:
            logger.info("WSKEY格式错误\n--------------------\n")
    logger.info("执行完成\n--------------------")
    with open("output.txt", "r") as fp:
        cks = fp.read().split("\n")
    tp = ""
    for kk in cks:
        tp = tp + kk +"&"
    with open("output.txt", "w") as fp:
        fp.write(tp)
    sys.exit(0)
