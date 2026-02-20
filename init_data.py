#!/usr/bin/env python3
"""
使用SQLAlchemy插入初始数据，避免编码问题
"""
import asyncio
import sys
import os
from uuid import uuid4

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

from app.models.user import Role, Permission, user_role, role_permission
from app.core.config import settings

async def init_database():
    """初始化数据库数据"""
    print("开始初始化数据库...")

    # 使用同步URL转换为异步URL
    # 将postgresql:// 转换为 postgresql+asyncpg://
    database_url = str(settings.database_url)
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print(f"连接数据库: {database_url}")

    # 创建异步引擎
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow
    )

    # 创建会话工厂
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        try:
            # 测试数据库连接
            await session.execute(text("SELECT 1"))
            print("数据库连接成功")

            # 检查表是否存在
            try:
                result = await session.execute(
                    text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'role')")
                )
                roles_exist = result.scalar()

                result = await session.execute(
                    text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'permission')")
                )
                permissions_exist = result.scalar()

                if not roles_exist or not permissions_exist:
                    print("错误: 表不存在。请先运行Alembic迁移:")
                    print("  uv run alembic upgrade head")
                    return False
            except Exception as e:
                print(f"检查表时出错: {e}")
                print("请确保已运行Alembic迁移")
                return False

            print("创建系统角色...")

            # 系统角色定义
            system_roles = [
                {"name": "admin", "description": "System Administrator", "is_system": True},
                {"name": "department_head", "description": "Department Head", "is_system": True},
                {"name": "management", "description": "Management Level", "is_system": True},
                {"name": "employee", "description": "Regular Employee", "is_system": True},
            ]

            # 创建或获取角色
            role_objects = {}
            for role_data in system_roles:
                result = await session.execute(
                    select(Role).where(Role.name == role_data["name"])
                )
                role = result.scalar_one_or_none()

                if not role:
                    role = Role(
                        id=uuid4(),
                        name=role_data["name"],
                        description=role_data["description"],
                        is_system=role_data["is_system"]
                    )
                    session.add(role)
                    await session.flush()
                    print(f"  创建角色: {role.name}")
                else:
                    print(f"  角色已存在: {role.name}")

                role_objects[role_data["name"]] = role

            print("创建系统权限...")

            # 系统权限定义
            system_permissions = [
                {"code": "user:create", "name": "Create User", "description": "Can create new users", "module": "user"},
                {"code": "user:read", "name": "View User", "description": "Can view user information", "module": "user"},
                {"code": "user:update", "name": "Update User", "description": "Can update user information", "module": "user"},
                {"code": "user:delete", "name": "Delete User", "description": "Can delete users", "module": "user"},
                {"code": "procurement:create", "name": "Create Procurement Request", "description": "Can create procurement requests", "module": "procurement"},
                {"code": "procurement:approve", "name": "Approve Procurement Request", "description": "Can approve procurement requests", "module": "procurement"},
                {"code": "supplier:create", "name": "Create Supplier", "description": "Can create suppliers", "module": "supplier"},
                {"code": "supplier:read", "name": "View Supplier", "description": "Can view supplier information", "module": "supplier"},
                {"code": "inventory:read", "name": "View Inventory", "description": "Can view inventory information", "module": "inventory"},
                {"code": "inventory:update", "name": "Update Inventory", "description": "Can update inventory information", "module": "inventory"},
            ]

            # 创建或获取权限
            permission_objects = {}
            for perm_data in system_permissions:
                result = await session.execute(
                    select(Permission).where(Permission.code == perm_data["code"])
                )
                permission = result.scalar_one_or_none()

                if not permission:
                    permission = Permission(
                        id=uuid4(),
                        code=perm_data["code"],
                        name=perm_data["name"],
                        description=perm_data["description"],
                        module=perm_data["module"]
                    )
                    session.add(permission)
                    await session.flush()
                    print(f"  创建权限: {permission.code}")
                else:
                    print(f"  权限已存在: {permission.code}")

                permission_objects[perm_data["code"]] = permission

            # 提交角色和权限
            await session.commit()

            print("分配角色权限...")

            # 为admin角色分配所有权限
            admin_role = role_objects["admin"]
            for permission in permission_objects.values():
                if permission not in admin_role.permissions:
                    admin_role.permissions.append(permission)

            # 为department_head角色分配权限
            dept_head_role = role_objects["department_head"]
            dept_head_perms = ["user:read", "user:create", "procurement:create", "procurement:approve", "supplier:read", "inventory:read"]
            for perm_code in dept_head_perms:
                if perm_code in permission_objects:
                    permission = permission_objects[perm_code]
                    if permission not in dept_head_role.permissions:
                        dept_head_role.permissions.append(permission)

            # 为management角色分配权限
            management_role = role_objects["management"]
            management_perms = ["user:read", "procurement:approve", "supplier:read", "inventory:read"]
            for perm_code in management_perms:
                if perm_code in permission_objects:
                    permission = permission_objects[perm_code]
                    if permission not in management_role.permissions:
                        management_role.permissions.append(permission)

            # 为employee角色分配权限
            employee_role = role_objects["employee"]
            employee_perms = ["user:read", "procurement:create", "supplier:read", "inventory:read"]
            for perm_code in employee_perms:
                if perm_code in permission_objects:
                    permission = permission_objects[perm_code]
                    if permission not in employee_role.permissions:
                        employee_role.permissions.append(permission)

            # 提交权限分配
            await session.commit()

            print("数据库初始化完成!")
            print("\n已创建的角色和权限:")
            for role_name, role in role_objects.items():
                perm_count = len(role.permissions)
                print(f"  {role_name}: {perm_count} 个权限")
                if perm_count > 0:
                    perm_codes = [perm.code for perm in role.permissions]
                    print(f"    权限: {', '.join(perm_codes)}")

            return True

        except Exception as e:
            await session.rollback()
            print(f"初始化数据库时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            await session.close()

def main():
    """主函数"""
    print("智能采购系统 - 数据库初始化工具")
    print("=" * 50)

    # 检查数据库配置
    print(f"数据库URL: {settings.database_url}")
    print(f"应用名称: {settings.app_name}")

    # 运行初始化
    success = asyncio.run(init_database())

    if success:
        print("\n[OK] 初始化成功!")
        print("请启动应用程序并访问用户管理页面查看角色权限。")
        return 0
    else:
        print("\n[ERROR] 初始化失败!")
        print("请检查:")
        print("  1. PostgreSQL服务是否运行")
        print("  2. 数据库连接配置是否正确 (.env文件)")
        print("  3. 是否已运行Alembic迁移 (uv run alembic upgrade head)")
        return 1

if __name__ == "__main__":
    sys.exit(main())