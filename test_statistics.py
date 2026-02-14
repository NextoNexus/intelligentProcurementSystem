#!/usr/bin/env python3
"""
测试用户统计接口的业务逻辑
"""
import asyncio
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, func

from app.core.config import settings
from app.core.database import get_async_database_url, get_engine_kwargs
from app.models.user import User, Role, user_role


async def test_statistics():
    """测试统计查询逻辑"""
    # 创建数据库引擎和会话
    database_url = str(settings.database_url)
    async_database_url = get_async_database_url(database_url)
    engine_kwargs = get_engine_kwargs(database_url)
    engine = create_async_engine(async_database_url, **engine_kwargs)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as db:
        print("=== 测试用户统计查询 ===")

        # 总用户数
        total_result = await db.execute(select(func.count()).select_from(User))
        total_users = total_result.scalar() or 0
        print(f"总用户数: {total_users}")

        # 活跃用户数
        active_result = await db.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )
        active_users = active_result.scalar() or 0
        print(f"活跃用户数: {active_users}")

        # 非活跃用户数
        inactive_users = total_users - active_users
        print(f"非活跃用户数: {inactive_users}")

        # 管理员数量（角色名为'admin'）
        admin_count_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name == "admin")
        )
        admin_count = admin_count_result.scalar() or 0
        print(f"管理员数量: {admin_count}")

        # 部门领导数量（角色名为'department_head'或'manager'）
        dept_head_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name.in_(["department_head", "manager"]))
        )
        dept_head_count = dept_head_result.scalar() or 0
        print(f"部门领导数量: {dept_head_count}")

        # 员工数量（角色名为'employee'）
        employee_count_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name == "employee")
        )
        employee_count = employee_count_result.scalar() or 0
        print(f"员工数量: {employee_count}")

        # 按部门统计用户分布
        department_stats_result = await db.execute(
            select(User.department, func.count(User.id).label("count"))
            .where(User.department.isnot(None))
            .group_by(User.department)
            .order_by(func.count(User.id).desc())
        )
        department_stats = [
            {"department": dept, "count": count}
            for dept, count in department_stats_result.all()
        ]
        print(f"按部门统计: {department_stats}")

        # 最近7天新增用户数
        seven_days_ago = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        recent_users_result = await db.execute(
            select(func.count()).select_from(User)
            .where(User.created_at >= seven_days_ago)
        )
        recent_users = recent_users_result.scalar() or 0
        print(f"最近7天新增用户数: {recent_users}")

        # 查询所有角色及其用户数
        role_stats_result = await db.execute(
            select(Role.name, func.count(func.distinct(User.id)).label("count"))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .group_by(Role.name)
            .order_by(Role.name)
        )
        role_stats = role_stats_result.all()
        print(f"角色分布统计:")
        for role_name, count in role_stats:
            print(f"  - {role_name}: {count}")

        print("=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(test_statistics())