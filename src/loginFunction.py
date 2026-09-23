import requests
import socket
import random
import os
import time

CHECK_URL = 'http://192.168.2.50/api/account/check'
LOGIN_URL = 'http://192.168.2.50/api/account/login'
PORTAL_BASE = 'http://192.168.2.50/tpl/default/login_account.html'

CSRF_API_URLS = [
    'http://192.168.2.50/csrf-token',
    'http://192.168.2.50/api/csrf-token'
]

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('192.168.2.50', 80))
        ip = s.getsockname()[0]
    except:
        ip = "10.220.10.30" 
    finally:
        s.close()
    return ip

def wait_for_network(target_host='192.168.2.50', timeout=30):
    print("[Network Guard] 等待获取 IP ...")
    start_time = time.time()
    time.sleep(2)
    
    while time.time() - start_time < timeout:
        current_ip = get_host_ip()
        if current_ip == "10.220.10.30":
            time.sleep(1)
            continue
            
        try:
            s = socket.create_connection((target_host, 80), timeout=1.5)
            s.close()
            print(f"[Network Guard] 当前分配到的 IP: {current_ip}")
            return True
        except:
            time.sleep(1.5)
            
    print("[Network Guard] 网络获取超时！")
    return False

def safe_tty_echo(msg, color_code="\033[0m"):
    try:
        clean_msg = str(msg).replace('"', '').replace("'", "").replace("(", "[").replace(")", "]")
        os.system(f'echo "{color_code}{clean_msg}\033[0m" > /dev/tty1')
    except:
        pass

def change_wlan0_mac():
    print("[MAC Changer] 更换mac")
    suffix = [f"{random.randint(0, 255):02x}" for _ in range(5)]
    new_mac = f"5e:{':'.join(suffix)}"
    print(f"[MAC Changer] wlan0 MAC 变更为: {new_mac}")
    
    safe_tty_echo(f"lF():\tChange MAC to {new_mac}", "\033[1;93m")
    
    os.system("ifconfig wlan0 down")
    os.system(f"ifconfig wlan0 hw ether {new_mac}")
    os.system("ifconfig wlan0 up")
    
    print("[MAC Changer] MAC 更改已下发")
    network_ready = wait_for_network('192.168.2.50', timeout=30)
    
    if network_ready:
        safe_tty_echo("lF():\tChange is Done. Network Ready.", "\033[1;92m")
    else:
        safe_tty_echo("lF():\tChange Done but Network Timeout.", "\033[1;31m")

def fetch_csrf_token(session, portal_url):
    try:
        session.get(portal_url, timeout=3)
    except:
        pass

    for api_url in CSRF_API_URLS:
        try:
            print(f"[CSRF Fetcher] 尝试请求 Token API: {api_url}")
            res = session.get(api_url, timeout=3)
            if res.status_code == 200:
                data = res.json()
                token = data.get('csrf_token') or data.get('token') or data.get('_csrf')
                if token:
                    print(f"[CSRF Fetcher] 最新 CSRF Token: {token}")
                    return token
        except Exception as e:
            print(f"[CSRF Fetcher Warning] 请求 {api_url} 异常: {e}")
            
    print("[CSRF Fetcher Warning] 无法拉取 Token,使用静态 Token")
    return "wl1J9C9w6VoOAje6Hu_Nhr9h6ws="

def loginFunction(username, full_id):
    password = str(full_id)[-6:]
    
    if get_host_ip() == "10.220.10.30":
        if not wait_for_network('192.168.2.50', timeout=5):
            print("[lF Error] 拒绝发送无效报文。")
            return -1
        
    local_ip = get_host_ip()
    portal_url = f"{PORTAL_BASE}?ip={local_ip}&nasId=2"
    
    session = requests.Session()
    
    # 获取动态 Token
    csrf_token = fetch_csrf_token(session, portal_url)
    
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': '192.168.2.50',
        'Origin': 'http://192.168.2.50',
        'Pragma': 'no-cache',
        'Referer': portal_url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0',
        'X-CSRF-Token': csrf_token,
        'X-Requested-With': 'XMLHttpRequest'
    }

    payload = {
        'username': username,
        'password': password,
        'nasId': '2',
        'userIpv4': local_ip,
        'isp': 'local',
        'timeLimit': ''
    }

    try:
        print(f"[lF Debug] 发送 check [IP: {local_ip}]...")
        check_res = session.post(CHECK_URL, headers=headers, data=payload, timeout=5)
        print(f"[lF Debug] check 回应: {check_res.status_code}")
    except Exception as e:
        print(f"[lF Warning] check 请求异常: {e}")

    try:
        print(f"[lF Debug] 尝试登录 [账号: {username}]...")
        login_res = session.post(LOGIN_URL, headers=headers, data=payload, timeout=5)
        
        print(f"[lF Debug] 网关返回: {login_res.status_code}")
        print(f"[lF Debug] 网关返回原文: {login_res.text}")
        
        safe_tty_echo(f"lF():\tReturnCode:{login_res.status_code}\tReturnText:{login_res.text}", "\033[1;93m")
            
        if login_res.status_code == 200:
            if "已登录成功" in login_res.text or '"code":0' in login_res.text or "认证成功" in login_res.text:
                safe_tty_echo("lF():\tReturnCode:LoginSuccess  - 1", "\033[1;32m")
                return 1
            elif "账号或密码错误" in login_res.text:
                safe_tty_echo("lF():\tReturnCode:AccOrPasswdError  - 0", "\033[1;31m")
                return 0
            elif "账号不存在" in login_res.text:
                safe_tty_echo("lF():\tReturnCode:NotHaveAcc  - 0", "\033[1;31m")
                return 0
            elif "mac" in login_res.text or "解绑" in login_res.text or "CSRF" in login_res.text or "mismatch" in login_res.text:
                safe_tty_echo("lF():\tReturnCode:MacLock_or_CSRF  - -2", "\033[1;31m")
                return -2
        else:
            safe_tty_echo(f"lF():\tReturnCode:{login_res.status_code}  - -1", "\033[1;31m")
            time.sleep(2)
        return -1

    except Exception as e:
        print(f"[lF Debug] 网络请求异常: {e}")
        safe_tty_echo(f"lF():\tException:{str(e)}  - -1", "\033[1;31m")
        return -1