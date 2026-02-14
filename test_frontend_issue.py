#!/usr/bin/env python3
"""
诊断前端用户管理页面问题
"""
import json
import requests
import sys

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def test_api_health():
    """测试API健康状态"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"[OK] API健康检查: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] API健康检查失败: {e}")
        return False

def test_api_version():
    """测试API版本信息"""
    try:
        response = requests.get(f"{BASE_URL}/api/version", timeout=5)
        print(f"[OK] API版本信息: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] API版本检查失败: {e}")
        return False

def test_login():
    """测试登录API"""
    try:
        login_data = {
            "username": "admin",
            "password": "Admin123!"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] 登录成功: access_token长度={len(data['access_token'])}")
            return data
        else:
            print(f"[ERROR] 登录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[ERROR] 登录请求失败: {e}")
        return None

def test_users_api_with_token(access_token):
    """测试用户管理API"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/users/",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            users = response.json()
            print(f"[OK] 用户API成功: 返回{len(users)}个用户")
            for user in users:
                print(f"  - {user['username']} ({user['roles']})")
            return True
        else:
            print(f"[ERROR] 用户API失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 用户API请求失败: {e}")
        return False

def test_user_statistics_api(access_token):
    """测试用户统计API"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/users/statistics/",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] 用户统计API成功: {stats}")
            return True
        else:
            print(f"[ERROR] 用户统计API失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 用户统计API请求失败: {e}")
        return False

def test_roles_api(access_token):
    """测试角色API"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/users/roles/simple/",
            headers=headers,
            timeout=5
        )
        if response.status_code == 200:
            roles = response.json()
            print(f"[OK] 角色API成功: 返回{len(roles)}个角色")
            for role in roles:
                print(f"  - {role['name']} ({role.get('description', '无描述')})")
            return True
        else:
            print(f"[ERROR] 角色API失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] 角色API请求失败: {e}")
        return False

def test_frontend_proxy():
    """测试前端代理到后端"""
    try:
        # 测试通过前端URL访问API
        response = requests.get(f"{FRONTEND_URL}/api/version", timeout=5)
        print(f"[OK] 前端代理测试: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] 前端代理测试失败: {e}")
        print(f"   确保前端服务器正在运行: npm run dev (在frontend目录)")
        return False

def main():
    print("=" * 60)
    print("前端用户管理页面问题诊断")
    print("=" * 60)

    print("\n1. 测试后端API健康状态...")
    if not test_api_health():
        print("[WARNING]  后端可能未启动，请运行: uv run uvicorn app.main:app --reload")
        return

    print("\n2. 测试API版本信息...")
    test_api_version()

    print("\n3. 测试前端代理配置...")
    test_frontend_proxy()

    print("\n4. 测试登录功能...")
    login_result = test_login()
    if not login_result:
        print("[WARNING]  登录失败，无法继续测试")
        return

    access_token = login_result['access_token']

    print("\n5. 测试用户管理API...")
    if not test_users_api_with_token(access_token):
        print("[WARNING]  用户API失败，检查权限设置")

    print("\n6. 测试用户统计API...")
    if not test_user_statistics_api(access_token):
        print("[WARNING]  用户统计API失败")

    print("\n7. 测试角色API...")
    if not test_roles_api(access_token):
        print("[WARNING]  角色API失败")

    print("\n" + "=" * 60)
    print("诊断完成")
    print("=" * 60)

    # 提供建议
    print("\n可能的解决方案:")
    print("1. 检查浏览器控制台错误 (F12 -> Console)")
    print("2. 检查网络请求 (F12 -> Network)")
    print("3. 检查localStorage中的access_token是否正确设置")
    print("4. 确保用户有admin角色权限")
    print("5. 检查CORS配置 (app/main.py中的CORS设置)")

if __name__ == "__main__":
    main()