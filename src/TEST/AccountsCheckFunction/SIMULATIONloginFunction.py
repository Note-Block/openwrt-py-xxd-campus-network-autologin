import random

def SIMULATIONloginFunction(phone, full_id):
    # 模拟登录函数返回
    # 1成功 0失败 -1异常 -2Mac被封
    print("[SIMULATIONloginFunction] 传入参数(",phone,",",full_id,")")
    res = random.choices([1, 0, -1, -2], weights=[30, 40, 10, 20], k=1)[0]
    print(f"[SIMULATIONloginFunction] 返回值: {res}")
    return res

def change_wlan0_mac():
    print("[SIMULATIONloginFunction] 已更改MAC地址")