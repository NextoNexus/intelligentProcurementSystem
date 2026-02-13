"""
用户认证和授权API路由
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr, Field

from ..core.database import get_db
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from ..core.dependencies import get_current_user, require_role
from ..models.user import User, Role

router = APIRouter()

# ========== Pydantic模型（临时放在这里，后续移到schemas/）==========

class UserRegister(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=8, description="密码（至少8个字符）")
    full_name: Optional[str] = Field(None, max_length=100, description="姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    employee_id: Optional[str] = Field(None, max_length=50, description="员工工号")
    department: Optional[str] = Field(None, max_length=100, description="部门")
    position: Optional[str] = Field(None, max_length=100, description="职位")

class UserLogin(BaseModel):
    """用户登录请求模型"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")

class Token(BaseModel):
    """令牌响应模型"""
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="访问令牌过期时间（秒）")

class UserResponse(BaseModel):
    """用户信息响应模型"""
    id: str = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="姓名")
    phone: Optional[str] = Field(None, description="手机号")
    employee_id: Optional[str] = Field(None, description="员工工号")
    department: Optional[str] = Field(None, description="部门")
    position: Optional[str] = Field(None, description="职位")
    roles: List[str] = Field(default_factory=list, description="角色列表")
    permissions: List[str] = Field(default_factory=list, description="权限列表")

class RefreshTokenRequest(BaseModel):
    """刷新令牌请求模型"""
    refresh_token: str = Field(..., description="刷新令牌")

# ========== API端点 ==========

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册

    注册新用户，默认分配'employee'角色
    """
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_email = result.scalar_one_or_none()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )

    # 获取employee角色
    result = await db.execute(
        select(Role).where(Role.name == "employee")
    )
    employee_role = result.scalar_one_or_none()
    if not employee_role:
        # 如果角色不存在，创建默认角色
        employee_role = Role(
            name="employee",
            description="普通员工",
            is_system=True
        )
        db.add(employee_role)
        await db.flush()

    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        employee_id=user_data.employee_id,
        department=user_data.department,
        position=user_data.position,
        is_active=True,
        is_verified=False,  # 需要邮箱验证
    )
    user.roles.append(employee_role)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 返回用户信息
    try:
        user_permissions = user.permissions
    except Exception:
        # 如果权限表不存在或其他错误，返回空列表
        user_permissions = []

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        employee_id=user.employee_id,
        department=user.department,
        position=user.position,
        roles=[role.name for role in user.roles],
        permissions=user_permissions
    )

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录

    使用用户名/邮箱和密码登录，返回访问令牌和刷新令牌
    """
    # 查找用户（支持用户名或邮箱登录）
    result = await db.execute(
        select(User).where(
            (User.username == login_data.username) | (User.email == login_data.username)
        ).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未激活"
        )

    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    await db.commit()

    # 创建令牌数据
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "roles": [role.name for role in user.roles],
        "permissions": user.permissions
    }

    # 创建访问令牌和刷新令牌
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=30 * 60  # 30分钟
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    token_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    刷新访问令牌

    使用有效的刷新令牌获取新的访问令牌
    """
    # 验证刷新令牌
    payload = verify_token(token_request.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查令牌类型
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌类型错误，请使用刷新令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌中缺少用户标识",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 查找用户
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或未激活",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 创建新的访问令牌
    token_data = {
        "sub": str(user.id),
        "username": user.username,
        "email": user.email,
        "roles": [role.name for role in user.roles],
        "permissions": user.permissions
    }

    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        refresh_token=token_request.refresh_token,  # 刷新令牌保持不变
        expires_in=30 * 60
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前用户信息
    """
    # 从数据库获取完整用户信息
    result = await db.execute(
        select(User).where(User.id == current_user["id"]).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return UserResponse(
        id=str(user.id),
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        employee_id=user.employee_id,
        department=user.department,
        position=user.position,
        roles=[role.name for role in user.roles],
        permissions=user.permissions
    )

# @router.get("/users", response_model=List[UserResponse], dependencies=[Depends(require_role("admin"))])
# async def get_users(
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     获取用户列表（仅管理员）
#     """
#     result = await db.execute(
#         select(User).offset(skip).limit(limit).options(selectinload(User.roles))
#     )
#     users = result.scalars().all()
#
#     return [
#         UserResponse(
#             id=str(user.id),
#             username=user.username,
#             email=user.email,
#             full_name=user.full_name,
#             phone=user.phone,
#             employee_id=user.employee_id,
#             department=user.department,
#             position=user.position,
#             roles=[role.name for role in user.roles],
#             permissions=user.permissions
#         )
#         for user in users
#     ]

