import asyncio
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# 导入项目模块
from app.core.security import get_password_hash
from app.core.config import settings
from app.core.database import get_async_database_url, get_engine_kwargs
from app.models.user import User, Role

async def create_admin_user():
  """创建管理员用户"""
  # 1. 创建数据库引擎和会话
  database_url = str(settings.database_url)
  async_database_url = get_async_database_url(database_url)
  engine_kwargs = get_engine_kwargs(database_url)
  engine = create_async_engine(async_database_url, **engine_kwargs)
  async_session = sessionmaker(
      engine, class_=AsyncSession, expire_on_commit=False
  )

  async with async_session() as session:
      # 2. 检查admin角色是否存在
      result = await session.execute(
          select(Role).where(Role.name == "admin")
      )
      admin_role = result.scalar_one_or_none()

      if not admin_role:
          print("错误：admin角色不存在！请先运行数据库初始化脚本。")
          print("执行命令：uv run alembic upgrade head")
          return

      # 3. 检查管理员用户是否已存在
      result = await session.execute(
          select(User).where(User.username == "admin")
      )
      existing_admin = result.scalar_one_or_none()

      if existing_admin:
          print("管理员用户已存在，跳过创建。")
          return

      # 4. 创建管理员用户
      admin_user = User(
          username="admin",
          email="admin@company.com",
          hashed_password=get_password_hash("Admin123!"),  # 默认密码，建议首次登录后修改
          full_name="系统管理员",
          phone="138-0000-0000",
          employee_id="ADMIN-001",
          department="信息技术部",
          position="系统管理员",
          is_active=True,
          is_verified=True,
          hire_date=datetime.utcnow(),
      )

      # 5. 分配admin角色
      admin_user.roles.append(admin_role)

      # 6. 保存到数据库
      session.add(admin_user)
      await session.commit()

      print("[成功] 管理员用户创建成功！")
      print("用户名: admin")
      print("密码: Admin123! (请首次登录后立即修改)")
      print("邮箱: admin@company.com")

if __name__ == "__main__":
  asyncio.run(create_admin_user())