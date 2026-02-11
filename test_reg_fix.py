#!/usr/bin/env python3
import subprocess
import time
import requests
import sys
import os

print("启动服务器...")
# 启动服务器，输出到控制台
proc = subprocess.Popen([
    sys.executable, "-m", "uvicorn",
    "app.main:app",
    "--host", "0.0.0.0",
    "--port", "8000"
], stdout=sys.stdout, stderr=sys.stderr)

print("等待10秒服务器启动...")
time.sleep(10)

print("发送注册请求...")
url = "http://localhost:8000/api/auth/register"
data = {
    "username": "fix_test_user",
    "email": "fix_test@example.com",
    "password": "TestPass123",
    "full_name": "Fix Test",
    "phone": "13800138000"
}

try:
    resp = requests.post(url, json=data, timeout=10)
    print(f"状态码: {resp.status_code}")
    print(f"响应: {resp.text}")
    if resp.status_code == 201:
        print("注册成功!")
    else:
        print("注册失败")
except Exception as e:
    print(f"请求错误: {e}")

print("停止服务器...")
proc.terminate()
proc.wait(timeout=5)
print("完成")