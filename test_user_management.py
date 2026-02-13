#!/usr/bin/env python3
"""
用户管理API测试脚本
使用FastAPI TestClient进行测试，无需运行服务器
修复事件循环问题版本
"""
import sys
import os
import asyncio

# 在导入任何模块之前设置环境变量和事件循环策略（Windows）
os.environ["ANYIO_BACKEND"] = "asyncio"
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models.user import User, Role
from app.core.security import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# 注意：不再使用全局client，改为每个测试函数创建新的client

# 测试数据
TEST_ADMIN_USERNAME = "admin"
TEST_ADMIN_PASSWORD = "Admin123!"
TEST_ADMIN_EMAIL = "admin@company.com"

async def get_test_db():
    """获取测试数据库会话"""
    from app.core.config import settings
    from app.core.database import get_async_database_url, get_engine_kwargs
    database_url = str(settings.database_url)
    async_database_url = get_async_database_url(database_url)
    engine_kwargs = get_engine_kwargs(database_url)
    engine = create_async_engine(async_database_url, **engine_kwargs)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

def test_login():
    """测试登录获取令牌"""
    with TestClient(app) as client:
        response = client.post("/api/auth/login", json={
            "username": TEST_ADMIN_USERNAME,
            "password": TEST_ADMIN_PASSWORD
        })
        print(f"登录响应状态码: {response.status_code}")
        print(f"登录响应内容: {response.text}")
        assert response.status_code == 200, f"登录失败: {response.text}"
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        print(f"登录成功，access_token: {data['access_token'][:50]}...")
        return data["access_token"]

def test_get_users_no_auth():
    """测试未认证时获取用户列表"""
    with TestClient(app) as client:
        response = client.get("/api/users/")
        print(f"未认证获取用户列表状态码: {response.status_code}")
        # 应该返回401或403
        assert response.status_code in [401, 403], f"预期401/403，实际: {response.status_code}"
        print("未认证访问被拒绝，符合预期")

def test_get_users_with_auth():
    """测试认证后获取用户列表"""
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    with TestClient(app) as client:
        response = client.get("/api/users/", headers=headers)
        print(f"认证后获取用户列表状态码: {response.status_code}")
        print(f"响应内容: {response.text[:200]}...")
        if response.status_code != 200:
            print(f"错误详情: {response.text}")
        # 可能返回200（成功）或403（权限不足）
        # 由于admin用户应该有admin角色，应该返回200
        assert response.status_code == 200, f"获取用户列表失败: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"成功获取 {len(data)} 个用户")

def test_get_simple_users():
    """测试获取简化用户列表（需要认证）"""
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    with TestClient(app) as client:
        response = client.get("/api/users/simple/", headers=headers)
        print(f"获取简化用户列表状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"错误详情: {response.text}")
        assert response.status_code == 200, f"获取简化用户列表失败: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"成功获取 {len(data)} 个简化用户")

def test_get_roles():
    """测试获取角色列表"""
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}
    with TestClient(app) as client:
        response = client.get("/api/users/roles/", headers=headers)
        print(f"获取角色列表状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"错误详情: {response.text}")
        assert response.status_code == 200, f"获取角色列表失败: {response.text}"
        data = response.json()
        assert isinstance(data, list)
        print(f"成功获取 {len(data)} 个角色")

def test_create_user():
    """测试创建新用户"""
    token = test_login()
    headers = {"Authorization": f"Bearer {token}"}

    # 生成唯一用户名和邮箱
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    username = f"testuser_{unique_id}"
    email = f"{username}@example.com"

    user_data = {
        "username": username,
        "email": email,
        "password": "TestPass123!",
        "full_name": "测试用户",
        "phone": "13800138000",
        "employee_id": f"EMP{unique_id}",
        "department": "测试部门",
        "position": "测试职位",
        "is_active": True,
        "is_verified": False,
        "role_ids": []  # 暂时不分配角色
    }

    with TestClient(app) as client:
        response = client.post("/api/users/", json=user_data, headers=headers)
        print(f"创建用户状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        if response.status_code != 201:
            print(f"创建用户失败: {response.text}")
        assert response.status_code == 201, f"创建用户失败: {response.text}"
        data = response.json()
        assert data["username"] == username
        assert data["email"] == email
        print(f"成功创建用户: {username}")
        return data["id"]

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("开始用户管理API测试")
    print("=" * 60)

    try:
        # 测试登录
        print("\n1. 测试登录...")
        token = test_login()

        print("\n2. 测试未认证访问...")
        test_get_users_no_auth()

        print("\n3. 测试认证后获取用户列表...")
        test_get_users_with_auth()

        print("\n4. 测试获取简化用户列表...")
        test_get_simple_users()

        print("\n5. 测试获取角色列表...")
        test_get_roles()

        print("\n6. 测试创建用户...")
        user_id = test_create_user()

        print("\n" + "=" * 60)
        print("所有测试完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(run_tests())