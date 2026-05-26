import json
import os
import time


from accountList import ACCOUNTS
from SIMULATIONloginFunction import SIMULATIONloginFunction, change_wlan0_mac #----------模拟

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS_FILE = os.path.join(BASE_DIR, 'status.json')     #------------状态文件

COOLDOWN_SECONDS = 12 * 60  # 被封冷却时间 12min * 60s
INIT_OFFSET = 99 * 60       # 初始偏移

def sync_status(accounts):
    # 同步内存与 status.json
    status = {}
    now = int(time.time())
    init_time = now - INIT_OFFSET
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content: 
                    status = json.loads(content)
        except Exception as e:
            print(f"[ACF Debug] 读取 status.json 失败: {e}")
            status = {}

    current_phones = {str(a['phone']) for a in accounts}
    status_phones = set(status.keys())

    changed = False
    # 清理已删号
    for p in (status_phones - current_phones):
        status.pop(p, None)
        changed = True
        
    # 初始化新加号
    for p in (current_phones - status_phones):
        status[p] = {
            "last_use": init_time,
            "cooldown_until": init_time
        }
        changed = True

    if changed or not os.path.exists(STATUS_FILE):
        save_status(status)
        
    return status

def save_status(status):
    # 保存状态到status.json
    temp_file = f"{STATUS_FILE}.tmp"
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        if os.path.exists(temp_file):
            os.replace(temp_file, STATUS_FILE)
    except Exception as e:
        print(f"[ACF Debug] status.json 保存失败: {e}")

def AccountsCheckFunction():
    # 外部调用
    
    
    accounts = ACCOUNTS

    if not accounts:
        print("[ACF Debug] accountList.py 内无任何可用账号")
        return "NULL"

    # 同步历史冷却
    status = sync_status(accounts)
    
    attempted_count = 0
    max_attempts = len(accounts)

    while attempted_count < max_attempts:
        # 获取时间戳
        current_loop_time = int(time.time())
        
        # 筛选账号
        available_phones = [
            p for p, v in status.items() 
            if v.get("cooldown_until", 0) <= current_loop_time
        ]
        
        if not available_phones:
            print("[ACF Debug] 所有账号均冷却")
            try:
                os.system(f'echo "\033[1;93mACF():\033[1;31mAll Accounts is Lock\033[0m" > /dev/tty1')
            except:
                pass
            return "NULL"

        # 最久未使用排序
        available_phones.sort(key=lambda p: status[p].get("last_use", 0))

        target_phone = available_phones[0]
        attempted_count += 1
        
        acc_detail = next((a for a in accounts if str(a['phone']) == target_phone), None)
        if not acc_detail:
            continue

        trace_try_msg = f"ACF():try:Acc:\033[1;36m{acc_detail['name']}\033[1;93m,Phone:\033[1;36m{target_phone}\033[0m"
        print(f"[Debug Scheduler] {trace_try_msg}")
        
        try:
            os.system(f'echo "\033[1;93m{trace_try_msg}\033[0m" > /dev/tty1')
        except:
            pass

        # 调用登录
        res = SIMULATIONloginFunction(target_phone, acc_detail['id'])

        if res == 1:
            # 登录成功
            now = int(time.time())
            status[target_phone]["last_use"] = now
            status[target_phone]["cooldown_until"] = 0
            save_status(status)
            
            try:
                os.system('echo "\033[1;93mACF():Return:\033[1;32mSuccess\033[0m" > /dev/tty1')
            except:
                pass
            return acc_detail['name']
            
        elif res == -2:
            # MAC 被封
            try:
                os.system('echo "\033[1;93mACF():Return:\033[1;31mBlacklist_Trigger_Change_MAC\033[0m" > /dev/tty1')
            except:
                pass
            
            # 调用更换 MAC
            change_wlan0_mac()
            
            
            now_after_hardware = int(time.time())
            status[target_phone]["last_use"] = now_after_hardware
            status[target_phone]["cooldown_until"] = now_after_hardware + COOLDOWN_SECONDS
            save_status(status)
            
            print("[ACF Debug] MAC 已更改 下一个账号重试")
            
            try:
                os.system('echo "\033[1;93mACF():\033[1;32mMAC Change Done. \033[1;93mNext Acc...\033[0m" > /dev/tty1')
            except:
                pass
            
            time.sleep(1)
            
        else:
            # 其他失败
            now = int(time.time())
            status[target_phone]["last_use"] = now
            status[target_phone]["cooldown_until"] = now + COOLDOWN_SECONDS
            save_status(status)
            
            try:
                os.system('echo "\033[1;93mACF():Return:\033[1;31mFail\033[0m" > /dev/tty1')
            except:
                pass
            time.sleep(2)

    return "NULL"