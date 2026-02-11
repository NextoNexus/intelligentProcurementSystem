"""
数据库配置模块
SQLAlchemy数据库引擎和会话管理
"""
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from .config import settings


def get_async_database_url(database_url: str) -> str:
    """
    根据数据库URL获取异步数据库连接URL

    Args:
        database_url: 原始数据库URL

    Returns:
        异步数据库连接URL
    """
    if database_url.startswith("postgresql://"):
        # PostgreSQL使用asyncpg驱动
        return database_url.replace("postgresql://", "postgresql+asyncpg://")
    elif database_url.startswith("sqlite://"):
        # SQLite使用aiosqlite驱动
        return database_url.replace("sqlite://", "sqlite+aiosqlite://")
    elif database_url.startswith("sqlite+aiosqlite://"):
        # 已经是aiosqlite格式
        return database_url
    else:
        # 默认返回原始URL，让SQLAlchemy处理
        return database_url


def get_engine_kwargs(database_url: str) -> dict:
    """
    根据数据库类型获取引擎参数

    Args:
        database_url: 数据库URL

    Returns:
        引擎参数字典
    """
    kwargs = {
        "echo": settings.debug,  # 调试模式下显示SQL语句
        "pool_pre_ping": True,  # 连接前ping检测
    }

    if database_url.startswith("sqlite"):
        # SQLite特定配置
        kwargs.update({
            "connect_args": {"check_same_thread": False},
            "poolclass": NullPool,  # SQLite不支持连接池
        })
    else:
        # PostgreSQL/其他数据库配置
        kwargs.update({
            "pool_size": settings.database_pool_size,
            "max_overflow": settings.database_max_overflow,
            "pool_recycle": 3600,  # 连接回收时间（秒）
        })

    return kwargs


# 创建异步引擎
async_database_url = get_async_database_url(str(settings.database_url))
engine_kwargs = get_engine_kwargs(str(settings.database_url))

engine = create_async_engine(
    async_database_url,
    **engine_kwargs
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 声明性基类
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    获取数据库会话依赖
    用于FastAPI依赖注入
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    初始化数据库，创建所有表
    注意：在生产环境中应使用Alembic迁移
    """
    # 导入所有模型以确保它们注册到Base.metadata
    from app import models  # noqa: F401
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """关闭数据库连接"""
    await engine.dispose()