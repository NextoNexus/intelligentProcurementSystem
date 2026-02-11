"""
依赖注入模块
FastAPI依赖项定义
"""
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_db
from .security import verify_token
from .config import settings

# HTTP Bearer认证方案
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
    db: AsyncSession = Depends(get_db)
) -> dict:
    """
    获取当前用户依赖

    Args:
        credentials: HTTP Bearer认证凭证
        db: 数据库会话

    Returns:
        用户信息字典

    Raises:
        HTTPException: 认证失败
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查令牌类型
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌类型无效，请使用访问令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 这里应该从数据库查询用户信息
    # 暂时返回payload中的信息
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌中缺少用户标识",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # TODO: 从数据库查询用户详细信息
    user_info = {
        "id": user_id,
        "username": payload.get("username", ""),
        "email": payload.get("email", ""),
        "roles": payload.get("roles", []),
        "permissions": payload.get("permissions", []),
    }

    return user_info


async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    """
    获取当前活跃用户（状态检查）

    Args:
        current_user: 当前用户

    Returns:
        活跃用户信息

    Raises:
        HTTPException: 用户未激活
    """
    # TODO: 添加用户状态检查
    # if not current_user.get("is_active"):
    #     raise HTTPException(status_code=400, detail="用户未激活")
    return current_user


def require_role(required_role: str):
    """
    角色权限检查依赖工厂

    Args:
        required_role: 需要的角色

    Returns:
        依赖函数
    """
    async def role_checker(
        current_user: Annotated[dict, Depends(get_current_active_user)]
    ) -> dict:
        user_roles = current_user.get("roles", [])
        if required_role not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要{required_role}角色权限",
            )
        return current_user

    return role_checker


def require_permission(required_permission: str):
    """
    权限检查依赖工厂

    Args:
        required_permission: 需要的权限

    Returns:
        依赖函数
    """
    async def permission_checker(
        current_user: Annotated[dict, Depends(get_current_active_user)]
    ) -> dict:
        user_permissions = current_user.get("permissions", [])
        if required_permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要{required_permission}权限",
            )
        return current_user

    return permission_checker


# 类型别名，方便在其他地方使用
CurrentUser = Annotated[dict, Depends(get_current_user)]
ActiveUser = Annotated[dict, Depends(get_current_active_user)]
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]