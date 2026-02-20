#!/usr/bin/env python3
"""
分配角色权限（修复版本）
使用原始SQL避免异步问题
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings

async def assign_permissions():
    """分配角色权限"""
    print("开始分配角色权限...")

    # 使用同步URL转换为异步URL
    database_url = str(settings.database_url)
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    print(f"连接数据库: {database_url}")

    # 创建异步引擎
    engine = create_async_engine(
        database_url,
        echo=False,
    )

    async with engine.begin() as conn:
        try:
            # 首先清除所有现有权限分配（仅对系统角色）
            print("清除现有权限分配...")
            await conn.execute(text("""
                DELETE FROM role_permission
                WHERE role_id IN (
                    SELECT id FROM role WHERE is_system = true
                )
            """))

            # 为admin角色分配所有权限
            print("为admin角色分配所有权限...")
            await conn.execute(text("""
                INSERT INTO role_permission (role_id, permission_id, created_at)
                SELECT r.id, p.id, NOW()
                FROM role r, permission p
                WHERE r.name = 'admin'
                ON CONFLICT (role_id, permission_id) DO NOTHING
            """))

            # 为department_head角色分配权限
            print("为department_head角色分配权限...")
            await conn.execute(text("""
                INSERT INTO role_permission (role_id, permission_id, created_at)
                SELECT r.id, p.id, NOW()
                FROM role r, permission p
                WHERE r.name = 'department_head'
                AND p.code IN ('user:read', 'user:create', 'procurement:create', 'procurement:approve', 'supplier:read', 'inventory:read')
                ON CONFLICT (role_id, permission_id) DO NOTHING
            """))

            # 为management角色分配权限
            print("为management角色分配权限...")
            await conn.execute(text("""
                INSERT INTO role_permission (role_id, permission_id, created_at)
                SELECT r.id, p.id, NOW()
                FROM role r, permission p
                WHERE r.name = 'management'
                AND p.code IN ('user:read', 'procurement:approve', 'supplier:read', 'inventory:read')
                ON CONFLICT (role_id, permission_id) DO NOTHING
            """))

            # 为employee角色分配权限
            print("为employee角色分配权限...")
            await conn.execute(text("""
                INSERT INTO role_permission (role_id, permission_id, created_at)
                SELECT r.id, p.id, NOW()
                FROM role r, permission p
                WHERE r.name = 'employee'
                AND p.code IN ('user:read', 'procurement:create', 'supplier:read', 'inventory:read')
                ON CONFLICT (role_id, permission_id) DO NOTHING
            """))

            # 提交事务
            await conn.commit()

            print("权限分配完成!")

            # 验证分配结果
            print("\n验证权限分配:")
            result = await conn.execute(text("""
                SELECT r.name, COUNT(rp.permission_id) as perm_count,
                       STRING_AGG(p.code, ', ') as permissions
                FROM role r
                LEFT JOIN role_permission rp ON r.id = rp.role_id
                LEFT JOIN permission p ON rp.permission_id = p.id
                WHERE r.is_system = true
                GROUP BY r.id, r.name
                ORDER BY r.name
            """))

            roles = result.fetchall()
            for role in roles:
                print(f"  {role.name}: {role.perm_count} 个权限")
                if role.permissions:
                    print(f"    权限: {role.permissions}")

            return True

        except Exception as e:
            await conn.rollback()
            print(f"分配权限时出错: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """主函数"""
    print("角色权限分配工具")
    print("=" * 50)

    # 检查数据库配置
    print(f"数据库URL: {settings.database_url}")

    # 运行分配
    success = asyncio.run(assign_permissions())

    if success:
        print("\n[OK] 权限分配成功!")
        print("请启动应用程序并访问用户管理页面查看角色权限。")
        return 0
    else:
        print("\n[ERROR] 权限分配失败!")
        print("请检查:")
        print("  1. 角色和权限是否已创建")
        print("  2. 数据库连接是否正常")
        return 1

if __name__ == "__main__":
    sys.exit(main())