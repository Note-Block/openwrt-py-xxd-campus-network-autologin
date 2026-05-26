import subprocess
import requests

def NetworkCheckFunction():
    """
    -1: 无 WiFi 连接 
     0: 有连接，但 Ping 不通
     1: 能 Ping 通，但被重定向
     2: 网络正常
    """
    # 检测 wlan0 连接
    try:
        # iw dev wlan0 link
        res = subprocess.run(['iw', 'dev', 'wlan0', 'link'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # 匹配 "Connected" 
        if "Connected" not in res.stdout:
            print("[Debug NCF] 未匹配 Connected")
            return -1
            
    except Exception as e:
        # 无iw 使用netstat
        try:
            with open('/sys/class/net/wlan0/operstate', 'r') as f:
                state = f.read().strip()
                # 非up则无连接
                if 'up' not in state:
                    return -1
        except:
            return -1

    # 3ping百度
    ping_res = subprocess.run(['ping', '-c', '3', 'www.baidu.com'], capture_output=True)
    if ping_res.returncode != 0:
        return 0

    # 检查内容
    try:
        response = requests.get("http://www.baidu.com", timeout=5, allow_redirects=True)
        response.encoding = 'utf-8'
        
        # 检查
        if "百度一下" in response.text:
            return 2
        else:
            return 1
    except Exception:
        # 请求失败视作拦截
        return 1