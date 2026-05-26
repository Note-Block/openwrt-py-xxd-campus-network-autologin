from loginFunction import loginFunction

def run_test():
    
    test_phone = "13388888888"
    test_full_id = "12345620260101"

    print(f"登录测试")

    # 调用登录
    result = loginFunction(test_phone, test_full_id)

    print(result)
if __name__ == "__main__":
    run_test()