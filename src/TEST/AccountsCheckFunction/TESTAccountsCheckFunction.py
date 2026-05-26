from AccountsCheckFunction import AccountsCheckFunction
import json
import os

def main():
    print("账户选择测试...")
    
    result = AccountsCheckFunction()
    
    print("-" * 40)
    print("[AccountsCheckFunction] -> 返回值:", result)

if __name__ == "__main__":
    main()