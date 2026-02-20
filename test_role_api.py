#!/usr/bin/env python3
"""
测试角色API的权限返回逻辑
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uuid import uuid4
from app.schemas.role import RoleResponse

# 模拟权限对象
class MockPermission:
    def __init__(self, id, code, name, module):
        self.id = id
        self.code = code
        self.name = name
        self.module = module

# 模拟角色对象
class MockRole:
    def __init__(self, id, name, description, is_system, permissions):
        self.id = id
        self.name = name
        self.description = description
        self.is_system = is_system
        self.permissions = permissions
        self.created_at = None
        self.updated_at = None

def test_role_response():
    """测试RoleResponse模型的权限转换"""
    # 创建模拟权限
    perm1 = MockPermission(id=uuid4(), code="user:create", name="创建用户", module="user")
    perm2 = MockPermission(id=uuid4(), code="user:read", name="查看用户", module="user")

    # 创建模拟角色
    role = MockRole(
        id=uuid4(),
        name="admin",
        description="系统管理员",
        is_system=True,
        permissions=[perm1, perm2]
    )

    # 手动构建字典（模拟API端点的逻辑）
    permission_codes = [perm.code for perm in role.permissions]
    permission_ids = [perm.id for perm in role.permissions]

    role_dict = {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
        "user_count": 5,
        "permissions": permission_codes,
        "permission_ids": permission_ids,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }

    # 使用Pydantic模型验证
    try:
        response = RoleResponse(**role_dict)
        print("[OK] RoleResponse验证成功")
        print(f"  权限代码: {response.permissions}")
        print(f"  权限ID: {response.permission_ids}")
        print(f"  用户数量: {response.user_count}")
        return True
    except Exception as e:
        print(f"[ERROR] RoleResponse验证失败: {e}")
        return False

def test_empty_permissions():
    """测试空权限列表"""
    role = MockRole(
        id=uuid4(),
        name="employee",
        description="普通员工",
        is_system=True,
        permissions=[]
    )

    permission_codes = [perm.code for perm in role.permissions]
    permission_ids = [perm.id for perm in role.permissions]

    role_dict = {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
        "user_count": 10,
        "permissions": permission_codes,
        "permission_ids": permission_ids,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }

    try:
        response = RoleResponse(**role_dict)
        print("[OK] 空权限列表验证成功")
        print(f"  权限代码: {response.permissions} (应为空列表)")
        print(f"  权限ID: {response.permission_ids} (应为空列表)")
        return True
    except Exception as e:
        print(f"[ERROR] 空权限列表验证失败: {e}")
        return False

if __name__ == "__main__":
    print("测试角色API权限返回逻辑")
    print("=" * 50)

    success1 = test_role_response()
    success2 = test_empty_permissions()

    print("=" * 50)
    if success1 and success2:
        print("[OK] 所有测试通过")
        sys.exit(0)
    else:
        print("[ERROR] 测试失败")
        sys.exit(1)