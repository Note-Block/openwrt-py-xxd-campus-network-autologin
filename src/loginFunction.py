# -*- coding: utf-8 -*-
import requests
import socket
import random
import os
import time

LOGIN_URL = 'http://192.168.2.50/api/account/login'

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('192.168.2.50', 80))
        ip = s.getsockname()[0]
    except:
        ip = "10.220.10.30" # 备用
    finally:
        s.close()
    return ip

def change_wlan0_mac():
    # mac 更换
    print("[MAC Changer] 更换mac")
    
    # 随机生成 MAC 5e:xx:xx...）
    suffix = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    new_mac = f"5e:{':'.join(suffix)}"
    print(f"[MAC Changer] wlan0 MAC 变更为: {new_mac}")
    
    try:
        os.system(f'echo "\033[1;93mlF():Change MAC to \033[1;32m{new_mac}\033[0m" > /dev/tty1')
    except:
        pass
    
    # 执行
    os.system("ifconfig wlan0 down")
    os.system(f"ifconfig wlan0 hw ether {new_mac}")
    os.system("ifconfig wlan0 up")
    
    print("[MAC Changer] MAC 更改已下发...")
    
    try:
        os.system(f'echo "\033[1;93mlF():Change is Done\033[0m" > /dev/tty1')
    except:
        pass
    
    time.sleep(5) 

# 外部调用
def loginFunction(username, full_id):
    #手机号 密码
    
    password = str(full_id)[-6:]
    local_ip = get_host_ip()
    
    portal_url = f"http://192.168.2.50/tpl/default/login_account.html?ip={local_ip}&nasId=2"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;q=0.6,ja;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://192.168.2.50',
        'Pragma': 'no-cache',
        'Referer': portal_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0',
        'X-CSRF-Token': 'ee4BJ20ZF3Xud-B_wGXwg0wYelU=',
        'X-Requested-With': 'XMLHttpRequest'
    }
    cookies = {
        'yudear': 'MTc3OTU0NjEwOXxEWDhFQVFMX2dBQUJFQUVRQUFBeV80QUFBUVp6ZEhKcGJtY01DZ0FJWTNOeVpsTmhiSFFHYzNSeWFXNW5EQklBRUcxRVlrWjBXa1pxZEVwUFJWWkZSbVU9fC03BQPNKVLfWDz9CwYV6sN0BYDj8b9cdDPgPPWOhKHC'
    }
    payload = {
        'username': username,
        'password': password,
        'nasId': '2',
        'userIpv4': local_ip,
        'isp': 'local',
        'timeLimit': ''
    }

    # 登录
    try:
        print(f"[lF Debug] 尝试登录 [账号: {username}]...")
    
        login_res = requests.post(
            LOGIN_URL, 
            headers=headers, 
            data=payload, 
            cookies=cookies, 
            timeout=5
        )
        
        print(f"[lF Debug] 网关返回状态码: {login_res.status_code}")
        print(f"[lF Debug] 网关返回原文: {login_res.text}")
        try:
            os.system(f'echo "\033[1;93mlF():ReturnCode:\033[1;36m{login_res.status_code}\t\033[1;93mReturnText:\033[1;36m{login_res.text}" > /dev/tty1')
        except:
            pass
            
        # 判定
        if login_res.status_code == 200:
            if "已登录成功" in login_res.text:
                os.system(f'echo "\033[1;93mlF():ReturnCode:\033[1;32mLoginSuccess\033[0m" > /dev/tty1')
                return 1
            elif "error" in login_res.text:
                return 0
            elif "mac" in login_res.text:
                return -2
        return -1

    except Exception as e:
        print(f"[lF Debug] 网络请求异常: {e}")
        
        try:
            os.system(f'echo "\033[1;93mlF():Exception:\033[1;31m{str(e)}\033[0m" > /dev/tty1')
        except:
            pass
        
        return -1