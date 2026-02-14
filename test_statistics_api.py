#!/usr/bin/env python3
"""
测试用户统计API端点
"""
import requests
import json
import sys
import time

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
STATS_URL = f"{BASE_URL}/api/users/statistics/"

def test_statistics_api():
    """测试统计API"""
    print("=== 测试用户统计API ===")

    # 1. 管理员登录
    login_data = {
        "username": "admin",
        "password": "Admin123!"
    }

    print(f"登录管理员账号: {login_data['username']}")
    try:
        login_response = requests.post(LOGIN_URL, json=login_data)
        login_response.raise_for_status()
        login_result = login_response.json()
        access_token = login_result.get("access_token")

        if not access_token:
            print("错误: 登录响应中没有access_token")
            print(f"响应: {login_result}")
            return False

        print("登录成功，获取到access_token")

    except requests.exceptions.RequestException as e:
        print(f"登录失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return False

    # 2. 获取用户统计数据
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print(f"请求统计端点: {STATS_URL}")
    try:
        stats_response = requests.get(STATS_URL, headers=headers)
        stats_response.raise_for_status()
        stats_result = stats_response.json()

        print("统计API响应成功!")
        print(f"响应状态码: {stats_response.status_code}")
        print(f"响应数据:")
        print(json.dumps(stats_result, indent=2, ensure_ascii=False))

        # 验证必要字段存在
        required_fields = [
            "total_users", "active_users", "inactive_users",
            "admin_count", "department_head_count", "last_updated", "status"
        ]

        for field in required_fields:
            if field not in stats_result:
                print(f"警告: 响应中缺少字段 '{field}'")
            else:
                print(f"  {field}: {stats_result[field]}")

        # 验证数据类型
        if not isinstance(stats_result["total_users"], int):
            print("错误: total_users 不是整数")
            return False

        if not isinstance(stats_result["active_users"], int):
            print("错误: active_users 不是整数")
            return False

        if stats_result["status"] != "working":
            print(f"警告: status 字段值为 '{stats_result['status']}'，期望 'working'")

        print("\n=== 统计结果 ===")
        print(f"总用户数: {stats_result['total_users']}")
        print(f"活跃用户数: {stats_result['active_users']}")
        print(f"非活跃用户数: {stats_result['inactive_users']}")
        print(f"管理员数量: {stats_result['admin_count']}")
        print(f"部门领导数量: {stats_result['department_head_count']}")

        # 显示额外字段（如果存在）
        if 'employee_count' in stats_result:
            print(f"员工数量: {stats_result['employee_count']}")
        if 'recent_users_7d' in stats_result:
            print(f"最近7天新增用户数: {stats_result['recent_users_7d']}")
        if 'department_stats' in stats_result and stats_result['department_stats']:
            print("按部门分布:")
            for dept_stat in stats_result['department_stats']:
                print(f"  - {dept_stat['department']}: {dept_stat['count']} 人")

        print(f"\n最后更新时间: {stats_result['last_updated']}")
        print(f"状态: {stats_result['status']}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"统计API请求失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return False

if __name__ == "__main__":
    # 检查后端是否运行
    try:
        health_check = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"后端服务运行正常 (状态码: {health_check.status_code})")
    except requests.exceptions.ConnectionError:
        print("错误: 后端服务未运行或无法连接")
        print("请先启动后端服务: uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
        sys.exit(1)

    # 运行测试
    success = test_statistics_api()
    sys.exit(0 if success else 1)