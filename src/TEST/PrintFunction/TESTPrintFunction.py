from PrintFunction import PrintFunction
import time

def main():
    print("=== 开始执行终端彩色打印模板测试 ===")
    
    print("\n[测试状态 1]: 网络通畅")
    PrintFunction(1, "网络通畅")
    time.sleep(0.5)

    print("\n[测试状态 2]: 无wifi连接")
    PrintFunction(2, "无wifi连接")
    time.sleep(0.5)

    print("\n[测试状态 3]: 重定向")
    PrintFunction(3, "重定向")
    time.sleep(0.5)

    print("\n[测试状态 4]: 登录失败")
    PrintFunction(4, "登录失败")
    time.sleep(0.5)

    print("\n[测试状态 5]: 登录成功")
    PrintFunction(5, "TestAccountName")
    time.sleep(0.5)

    print("\n[测试状态 6]: 有连接但ping不通")
    PrintFunction(6, "有连接但ping不通")

if __name__ == "__main__":
    main()