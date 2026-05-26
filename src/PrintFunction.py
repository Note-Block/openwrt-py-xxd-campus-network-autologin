import time
import subprocess
import re
import sys

COLOR_GOLD = "\033[1;33m"       # 金黄
COLOR_SKY_BLUE = "\033[1;36m"   # 天蓝
COLOR_LIGHT_GREEN = "\033[1;32m" # 亮绿
COLOR_LIGHT_RED = "\033[1;31m"   # 亮红
COLOR_LIGHT_YELLOW = "\033[1;93m"# 亮黄
COLOR_WHITE = "\033[0m"        # 白色/重置
COLOR_BOLD = "\033[1m"         # 粗体

# 打印
def _custom_print(text):
    # 终端
    sys.stdout.write(text)
    sys.stdout.flush()
    
    # tty1
    try:
        with open('/dev/tty1', 'w', encoding='utf-8') as tty:
            tty.write(text)
            tty.flush()
    except:
        # 防止崩溃
        pass

# 数据获取
def _get_time_str():
    return time.strftime("%Y:%m:%d-%H:%M:%S")

def _get_time_short_str():
    return time.strftime("%M")

def _get_wifi_ssid():
    # 获取SSID
    try:
        res = subprocess.check_output("iwinfo wlan0 info", shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        match = re.search(r'ESSID:\s*"([^"]+)"', res)
        if match:
            return match.group(1)
    except:
        pass
    return "Unknown-SSID"

def _get_wlan_ip():
    # 获取wlan0的 IPv4
    try:
        res = subprocess.check_output("ifconfig wlan0", shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        match = re.search(r'inet addr:([\d\.]+)', res)
        if match:
            return match.group(1)
    except:
        pass
    return "0.0.0.0"

def _get_wlan_mac():
    # 获取wlan0 MAC地址
    try:
        with open('/sys/class/net/wlan0/address', 'r') as f:
            return f.read().strip()
    except:
        pass
    return "00:00:00:00:00:00"

def _get_wlan_gateway():
    # 获取网关
    try:
        res = subprocess.check_output("route -n", shell=True).decode('utf-8')
        for line in res.split('\n'):
            if line.startswith('0.0.0.0'):
                parts = line.split()
                if len(parts) > 2:
                    return parts[1]
    except:
        pass
    return "0.0.0.0"

def _get_wlan_dns():
    # 获取DNS接口
    try:
        with open('/tmp/resolv.conf.d/resolv.conf.auto', 'r') as f:
            for line in f:
                if line.strip().startswith('nameserver'):
                    return line.split()[1]
    except:
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if line.strip().startswith('nameserver'):
                        return line.split()[1]
        except:
            pass
    return "114.114.114.114"

def _get_baidu_ping():
    # ping
    try:
        # 发ping超时 2 秒
        res = subprocess.check_output("ping -c 2 -W 2 baidu.com", shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        # 抓取 avg
        match = re.search(r'min/avg/max[^=]*=\s*[\d\.]+/([\d\.]+)', res)
        if match:
            ping_val = float(match.group(1))
            
            # 颜色匹配
            if ping_val < 30.0:
                color_prefix = COLOR_LIGHT_GREEN
            elif 30.0 <= ping_val < 60.0:
                color_prefix = COLOR_SKY_BLUE
            elif 60.0 <= ping_val < 100.0:
                color_prefix = COLOR_LIGHT_YELLOW
            else:
                color_prefix = COLOR_LIGHT_RED
                
            return f"{color_prefix}{ping_val:.3f}{COLOR_WHITE}"
    except:
        pass
    return f"{COLOR_LIGHT_RED}Failed{COLOR_WHITE}"


# 打印函数族
def _print_status_1():
    current_struct_time = time.localtime()
    m = current_struct_time.tm_min

    # 60 分钟节点
    if m % 60 == 0:
        head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_GREEN} - NetWork is Ok \t\t[{COLOR_LIGHT_GREEN}{COLOR_BOLD}OK{COLOR_WHITE}]\n"
        body = (
            f"\tWIFI SSID:\t{COLOR_SKY_BLUE}{_get_wifi_ssid()}{COLOR_WHITE}\n"
            f"\tWLAN IP:\t{COLOR_SKY_BLUE}{_get_wlan_ip()}{COLOR_WHITE}\n"
            f"\tWLAN MAC:\t{COLOR_SKY_BLUE}{_get_wlan_mac()}{COLOR_WHITE}\n"
            f"\tWLAN Gateway:\t{COLOR_SKY_BLUE}{_get_wlan_gateway()}{COLOR_WHITE}\n"
            f"\tWLAN DNS:\t{COLOR_SKY_BLUE}{_get_wlan_dns()}{COLOR_WHITE}\n"
            f"\tPing Baidu:\t{_get_baidu_ping()} ms\n"
        )
        _custom_print(head + body)
    else:
        # 20 40带 \n 否则为空
        prefix = "\n" if m % 20 == 0 else ""
        _custom_print(f"{prefix}{COLOR_GOLD}#{COLOR_GOLD}{_get_time_short_str()}{COLOR_WHITE}->{COLOR_LIGHT_GREEN}OK{COLOR_WHITE} ")

def _print_status_2():
    head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_RED} - No Wifi Connection {COLOR_WHITE}\t[{COLOR_LIGHT_RED}{COLOR_BOLD}ERROR{COLOR_WHITE}]\n"
    _custom_print(head)

def _print_status_3():
    head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_YELLOW} - Redirected \t\t\t[{COLOR_LIGHT_YELLOW}{COLOR_BOLD}WARING{COLOR_WHITE}]\n"
    _custom_print(head)

def _print_status_4():
    head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_RED} - Login Failed \t\t[{COLOR_LIGHT_RED}{COLOR_BOLD}ERROR{COLOR_WHITE}]\n"
    _custom_print(head)

def _print_status_5(account_name):
    head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_GREEN} - Logged Success \t\t[{COLOR_LIGHT_GREEN}{COLOR_BOLD}OK{COLOR_WHITE}]\n"
    body = (
        f"\tAccount:\t{COLOR_LIGHT_GREEN}{COLOR_BOLD}{account_name}{COLOR_WHITE}\n"
        f"\tWIFI SSID:\t{COLOR_SKY_BLUE}{_get_wifi_ssid()}{COLOR_WHITE}\n"
        f"\tWLAN IP:\t{COLOR_SKY_BLUE}{_get_wlan_ip()}{COLOR_WHITE}\n"
        f"\tWLAN MAC:\t{COLOR_SKY_BLUE}{_get_wlan_mac()}{COLOR_WHITE}\n"
        f"\tWLAN Gateway:\t{COLOR_SKY_BLUE}{_get_wlan_gateway()}{COLOR_WHITE}\n"
        f"\tWLAN DNS:\t{COLOR_SKY_BLUE}{_get_wlan_dns()}{COLOR_WHITE}\n"
    )
    _custom_print(head + body)

def _print_status_6():
    head = f"\n{COLOR_GOLD}---AutoLoginPy:{COLOR_WHITE}[{_get_time_str()}{COLOR_WHITE}]{COLOR_LIGHT_RED} - No Internet Connection {COLOR_WHITE}\t\t[{COLOR_LIGHT_RED}{COLOR_BOLD}ERROR{COLOR_WHITE}]\n"
    body = (
        f"\tWIFI SSID:\t{COLOR_SKY_BLUE}{_get_wifi_ssid()}{COLOR_WHITE}\n"
        f"\tWLAN IP:\t{COLOR_SKY_BLUE}{_get_wlan_ip()}{COLOR_WHITE}\n"
        f"\tWLAN MAC:\t{COLOR_SKY_BLUE}{_get_wlan_mac()}{COLOR_WHITE}\n"
        f"\tWLAN Gateway:\t{COLOR_SKY_BLUE}{_get_wlan_gateway()}{COLOR_WHITE}\n"
    )
    _custom_print(head + body)

# 外部入口
def PrintFunction(status_code, account_name):
    """
    status_code 映射关系:
      1:网络通畅
      2:无wifi连接
      3:重定向
      4:登录失败
      5:登录成功
      6:有连接但ping不通
    """
    if status_code == 1:
        _print_status_1()
    elif status_code == 2:
        _print_status_2()
    elif status_code == 3:
        _print_status_3()
    elif status_code == 4:
        _print_status_4()
    elif status_code == 5:
        _print_status_5(account_name)
    elif status_code == 6:
        _print_status_6()