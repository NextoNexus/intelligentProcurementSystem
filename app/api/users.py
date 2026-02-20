"""
用户管理API路由
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from ..core.database import get_db
from ..core.security import get_password_hash
from ..core.dependencies import get_current_user, require_role
from ..models.user import User, Role, Permission, user_role
from ..schemas.user import (
    UserCreate, UserUpdate, UserResponse, UserSimpleResponse
)
from ..schemas.role import (
    RoleCreate, RoleUpdate, RoleResponse, RoleSimpleResponse,
    PermissionCreate, PermissionResponse, PermissionSimpleResponse
)

router = APIRouter()


# ========== 用户管理API ==========

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_role("admin"))])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    search: Optional[str] = Query(None, description="搜索关键词（用户名、姓名、邮箱）"),
    role_id: Optional[UUID] = Query(None, description="按角色ID过滤"),
    is_active: Optional[bool] = Query(None, description="按激活状态过滤"),
    department: Optional[str] = Query(None, description="按部门过滤"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户列表（仅管理员）

    支持分页、搜索和过滤
    """
    # 构建查询
    query = select(User).options(selectinload(User.roles))

    # 应用过滤条件
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (User.username.ilike(search_pattern)) |
            (User.full_name.ilike(search_pattern)) |
            (User.email.ilike(search_pattern)) |
            (User.employee_id.ilike(search_pattern))
        )

    if role_id:
        query = query.where(User.roles.any(Role.id == role_id))

    if is_active is not None:
        query = query.where(User.is_active == is_active)

    if department:
        query = query.where(User.department == department)

    # 应用分页
    query = query.offset(skip).limit(limit).order_by(User.created_at.desc())

    # 执行查询
    result = await db.execute(query)
    users = result.scalars().all()

    # 手动序列化用户对象以避免验证错误
    user_responses = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "employee_id": user.employee_id,
            "department": user.department,
            "position": user.position,
            "hire_date": user.hire_date,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "last_login_at": user.last_login_at,
            "last_login_ip": user.last_login_ip,
            "roles": [role.name for role in user.roles],
            "role_ids": [role.id for role in user.roles],
            "permissions": user.permissions,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
        user_responses.append(user_dict)
    return user_responses


@router.get("/statistics/", dependencies=[Depends(require_role("admin"))])
async def get_user_statistics(
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户统计数据（仅管理员）

    返回总用户数、管理员数、部门领导数、活跃用户数等
    """
    try:
        # 总用户数
        total_result = await db.execute(select(func.count()).select_from(User))
        total_users = total_result.scalar() or 0

        # 活跃用户数
        active_result = await db.execute(
            select(func.count()).select_from(User).where(User.is_active == True)
        )
        active_users = active_result.scalar() or 0

        # 非活跃用户数
        inactive_users = total_users - active_users

        # 管理员数量（角色名为'admin'）
        admin_count_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name == "admin")
        )
        admin_count = admin_count_result.scalar() or 0

        # 部门领导数量（角色名为'department_head'或'manager'）
        # 首先检查哪些角色名称存在
        dept_head_count = 0
        # 尝试查询'department_head'角色
        dept_head_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name.in_(["department_head", "manager"]))
        )
        dept_head_count = dept_head_result.scalar() or 0

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

        # 最近7天新增用户数
        seven_days_ago = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        recent_users_result = await db.execute(
            select(func.count()).select_from(User)
            .where(User.created_at >= seven_days_ago)
        )
        recent_users = recent_users_result.scalar() or 0

        # 员工数量（角色名为'employee'）
        employee_count_result = await db.execute(
            select(func.count(func.distinct(User.id)))
            .select_from(User)
            .join(user_role, User.id == user_role.c.user_id)
            .join(Role, Role.id == user_role.c.role_id)
            .where(Role.name == "employee")
        )
        employee_count = employee_count_result.scalar() or 0

        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": inactive_users,
            "admin_count": admin_count,
            "department_head_count": dept_head_count,
            "employee_count": employee_count,
            "recent_users_7d": recent_users,
            "department_stats": department_stats,
            "last_updated": datetime.utcnow(),
            "status": "working"
        }

    except Exception as e:
        # 记录错误并返回错误信息
        import logging
        logging.error(f"获取用户统计数据失败: {str(e)}")
        return {
            "total_users": 0,
            "active_users": 0,
            "inactive_users": 0,
            "admin_count": 0,
            "department_head_count": 0,
            "employee_count": 0,
            "recent_users_7d": 0,
            "department_stats": [],
            "last_updated": datetime.utcnow(),
            "status": f"error: {str(e)}"
        }


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户详情（仅管理员）
    """
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新用户（仅管理员）
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

    # 检查员工工号是否已存在
    if user_data.employee_id:
        result = await db.execute(
            select(User).where(User.employee_id == user_data.employee_id)
        )
        existing_employee_id = result.scalar_one_or_none()
        if existing_employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="员工工号已存在"
            )

    # 获取角色
    roles = []
    if user_data.role_ids:
        result = await db.execute(
            select(Role).where(Role.id.in_(user_data.role_ids))
        )
        roles = result.scalars().all()

        if len(roles) != len(user_data.role_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分角色不存在"
            )

    # 创建用户
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        avatar_url=user_data.avatar_url,
        employee_id=user_data.employee_id,
        department=user_data.department,
        position=user_data.position,
        hire_date=user_data.hire_date,
        is_active=user_data.is_active,
        is_verified=user_data.is_verified,
    )

    # 添加角色
    for role in roles:
        user.roles.append(role)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户信息（仅管理员）
    """
    # 获取用户
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 检查用户名是否已被其他用户使用
    if user_data.username and user_data.username != user.username:
        result = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

    # 检查邮箱是否已被其他用户使用
    if user_data.email and user_data.email != user.email:
        result = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_email = result.scalar_one_or_none()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )

    # 检查员工工号是否已被其他用户使用
    if user_data.employee_id and user_data.employee_id != user.employee_id:
        result = await db.execute(
            select(User).where(User.employee_id == user_data.employee_id)
        )
        existing_employee_id = result.scalar_one_or_none()
        if existing_employee_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="员工工号已存在"
            )

    # 更新字段
    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

    # 处理密码更新
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除用户（仅管理员）

    注意：系统内置用户和当前登录用户不能被删除
    """
    # 获取用户
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 检查是否为系统内置用户（通过角色判断）
    for role in user.roles:
        if role.is_system and role.name == "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="系统管理员用户不能被删除"
            )

    # 删除用户
    await db.delete(user)
    await db.commit()

    return None


@router.put("/{user_id}/roles", response_model=UserResponse, dependencies=[Depends(require_role("admin"))])
async def update_user_roles(
    user_id: UUID,
    role_ids: List[UUID],
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户角色（仅管理员）
    """
    # 获取用户
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.roles))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 获取角色
    result = await db.execute(
        select(Role).where(Role.id.in_(role_ids))
    )
    roles = result.scalars().all()

    if len(roles) != len(role_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="部分角色不存在"
        )

    # 更新用户角色
    user.roles.clear()
    for role in roles:
        user.roles.append(role)

    await db.commit()
    await db.refresh(user)

    return user


@router.put("/{user_id}/password", dependencies=[Depends(require_role("admin"))])
async def reset_user_password(
    user_id: UUID,
    new_password: str,
    db: AsyncSession = Depends(get_db)
):
    """
    重置用户密码（仅管理员）
    """
    # 获取用户
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 更新密码
    user.hashed_password = get_password_hash(new_password)
    await db.commit()

    return {"message": "密码重置成功"}


@router.get("/simple/", response_model=List[UserSimpleResponse])
async def get_simple_users(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取简化用户列表（用于下拉选择等场景）

    所有登录用户可用
    """
    result = await db.execute(
        select(User).where(User.is_active == True).order_by(User.username)
    )
    users = result.scalars().all()

    return users


# ========== 角色管理API ==========

@router.get("/roles/", response_model=List[RoleResponse], dependencies=[Depends(require_role("admin"))])
async def get_roles(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    is_system: Optional[bool] = Query(None, description="是否系统内置角色"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取角色列表（仅管理员）
    """
    query = select(Role).options(selectinload(Role.permissions))

    if is_system is not None:
        query = query.where(Role.is_system == is_system)

    query = query.offset(skip).limit(limit).order_by(Role.name)

    result = await db.execute(query)
    roles = result.scalars().all()

    # 如果没有角色，直接返回
    if not roles:
        return []

    # 提取角色ID列表
    role_ids = [role.id for role in roles]

    # 查询每个角色的用户数量
    user_count_query = (
        select(user_role.c.role_id, func.count(user_role.c.user_id).label('user_count'))
        .where(user_role.c.role_id.in_(role_ids))
        .group_by(user_role.c.role_id)
    )
    user_count_result = await db.execute(user_count_query)
    user_counts = {role_id: count for role_id, count in user_count_result.all()}

    # 为每个角色添加用户数量和权限信息
    response_roles = []
    for role in roles:
        # 获取权限代码列表和权限ID列表
        permission_codes = [perm.code for perm in role.permissions]
        permission_ids = [perm.id for perm in role.permissions]

        # 构建响应字典
        role_dict = {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "is_system": role.is_system,
            "user_count": user_counts.get(role.id, 0),
            "permissions": permission_codes,
            "permission_ids": permission_ids,
            "created_at": role.created_at,
            "updated_at": role.updated_at
        }
        response_roles.append(role_dict)

    return response_roles


@router.get("/roles/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_role("admin"))])
async def get_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    获取角色详情（仅管理员）
    """
    result = await db.execute(
        select(Role).where(Role.id == role_id).options(selectinload(Role.permissions))
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )

    # 查询该角色的用户数量
    user_count_query = (
        select(func.count(user_role.c.user_id))
        .where(user_role.c.role_id == role_id)
    )
    user_count_result = await db.execute(user_count_query)
    user_count = user_count_result.scalar() or 0

    # 获取权限代码列表和权限ID列表
    permission_codes = [perm.code for perm in role.permissions]
    permission_ids = [perm.id for perm in role.permissions]

    # 构建响应字典
    role_dict = {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
        "user_count": user_count,
        "permissions": permission_codes,
        "permission_ids": permission_ids,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }

    return role_dict


@router.post("/roles/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新角色（仅管理员）
    """
    # 检查角色名是否已存在
    result = await db.execute(
        select(Role).where(Role.name == role_data.name)
    )
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名称已存在"
        )

    # 获取权限
    permissions = []
    if role_data.permission_ids:
        result = await db.execute(
            select(Permission).where(Permission.id.in_(role_data.permission_ids))
        )
        permissions = result.scalars().all()

        if len(permissions) != len(role_data.permission_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分权限不存在"
            )

    # 创建角色
    role = Role(
        name=role_data.name,
        description=role_data.description,
        is_system=role_data.is_system,
    )

    # 添加权限
    for permission in permissions:
        role.permissions.append(permission)

    db.add(role)
    await db.commit()
    await db.refresh(role)

    # 新创建的角色没有用户
    role.user_count = 0

    # 获取权限代码列表和权限ID列表
    permission_codes = [perm.code for perm in role.permissions]
    permission_ids = [perm.id for perm in role.permissions]

    # 构建响应字典
    role_dict = {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
        "user_count": 0,
        "permissions": permission_codes,
        "permission_ids": permission_ids,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }

    return role_dict


@router.put("/roles/{role_id}", response_model=RoleResponse, dependencies=[Depends(require_role("admin"))])
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新角色信息（仅管理员）
    """
    # 获取角色
    result = await db.execute(
        select(Role).where(Role.id == role_id).options(selectinload(Role.permissions))
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )

    # 检查是否为系统内置角色
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统内置角色不能被修改"
        )

    # 检查角色名是否已被其他角色使用
    if role_data.name and role_data.name != role.name:
        result = await db.execute(
            select(Role).where(Role.name == role_data.name)
        )
        existing_role = result.scalar_one_or_none()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名称已存在"
            )

    # 更新字段
    update_data = role_data.model_dump(exclude_unset=True)

    # 处理权限更新
    if "permission_ids" in update_data:
        permission_ids = update_data.pop("permission_ids")

        # 获取权限
        result = await db.execute(
            select(Permission).where(Permission.id.in_(permission_ids))
        )
        permissions = result.scalars().all()

        if len(permissions) != len(permission_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="部分权限不存在"
            )

        # 更新角色权限
        role.permissions.clear()
        for permission in permissions:
            role.permissions.append(permission)

    for field, value in update_data.items():
        setattr(role, field, value)

    await db.commit()
    await db.refresh(role)

    # 查询该角色的用户数量
    user_count_query = (
        select(func.count(user_role.c.user_id))
        .where(user_role.c.role_id == role_id)
    )
    user_count_result = await db.execute(user_count_query)
    user_count = user_count_result.scalar() or 0

    # 获取权限代码列表和权限ID列表
    permission_codes = [perm.code for perm in role.permissions]
    permission_ids = [perm.id for perm in role.permissions]

    # 构建响应字典
    role_dict = {
        "id": role.id,
        "name": role.name,
        "description": role.description,
        "is_system": role.is_system,
        "user_count": user_count,
        "permissions": permission_codes,
        "permission_ids": permission_ids,
        "created_at": role.created_at,
        "updated_at": role.updated_at
    }

    return role_dict


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_role(
    role_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除角色（仅管理员）

    注意：系统内置角色不能被删除
    """
    # 获取角色
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )

    # 检查是否为系统内置角色
    if role.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="系统内置角色不能被删除"
        )

    # 检查是否有用户使用该角色
    result = await db.execute(
        select(func.count()).select_from(User).where(User.roles.any(Role.id == role_id))
    )
    user_count = result.scalar()

    if user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该角色被 {user_count} 个用户使用，无法删除"
        )

    # 删除角色
    await db.delete(role)
    await db.commit()

    return None


@router.get("/roles/simple/", response_model=List[RoleSimpleResponse])
async def get_simple_roles(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取简化角色列表（用于下拉选择等场景）

    所有登录用户可用
    """
    result = await db.execute(
        select(Role).order_by(Role.name)
    )
    roles = result.scalars().all()

    return roles


# ========== 权限管理API ==========

@router.get("/permissions/", response_model=List[PermissionResponse], dependencies=[Depends(require_role("admin"))])
async def get_permissions(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    module: Optional[str] = Query(None, description="按模块过滤"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取权限列表（仅管理员）
    """
    query = select(Permission)

    if module:
        query = query.where(Permission.module == module)

    query = query.offset(skip).limit(limit).order_by(Permission.module, Permission.code)

    result = await db.execute(query)
    permissions = result.scalars().all()

    return permissions


@router.get("/permissions/{permission_id}", response_model=PermissionResponse, dependencies=[Depends(require_role("admin"))])
async def get_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    获取权限详情（仅管理员）
    """
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )

    return permission


@router.post("/permissions/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role("admin"))])
async def create_permission(
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建新权限（仅管理员）
    """
    # 检查权限代码是否已存在
    result = await db.execute(
        select(Permission).where(Permission.code == permission_data.code)
    )
    existing_permission = result.scalar_one_or_none()
    if existing_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限代码已存在"
        )

    # 创建权限
    permission = Permission(
        code=permission_data.code,
        name=permission_data.name,
        description=permission_data.description,
        module=permission_data.module,
    )

    db.add(permission)
    await db.commit()
    await db.refresh(permission)

    return permission


@router.put("/permissions/{permission_id}", response_model=PermissionResponse, dependencies=[Depends(require_role("admin"))])
async def update_permission(
    permission_id: UUID,
    permission_data: PermissionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    更新权限信息（仅管理员）
    """
    # 获取权限
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )

    # 检查权限代码是否已被其他权限使用
    if permission_data.code != permission.code:
        result = await db.execute(
            select(Permission).where(Permission.code == permission_data.code)
        )
        existing_permission = result.scalar_one_or_none()
        if existing_permission:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="权限代码已存在"
            )

    # 更新字段
    update_data = permission_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permission, field, value)

    await db.commit()
    await db.refresh(permission)

    return permission


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role("admin"))])
async def delete_permission(
    permission_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    删除权限（仅管理员）
    """
    # 获取权限
    result = await db.execute(
        select(Permission).where(Permission.id == permission_id)
    )
    permission = result.scalar_one_or_none()

    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )

    # 检查是否有角色使用该权限
    result = await db.execute(
        select(func.count()).select_from(Role).where(Role.permissions.any(Permission.id == permission_id))
    )
    role_count = result.scalar()

    if role_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该权限被 {role_count} 个角色使用，无法删除"
        )

    # 删除权限
    await db.delete(permission)
    await db.commit()

    return None


@router.get("/permissions/simple/", response_model=List[PermissionSimpleResponse])
async def get_simple_permissions(
    module: Optional[str] = Query(None, description="按模块过滤"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    获取简化权限列表（用于下拉选择等场景）

    所有登录用户可用
    """
    query = select(Permission)

    if module:
        query = query.where(Permission.module == module)

    query = query.order_by(Permission.module, Permission.code)

    result = await db.execute(query)
    permissions = result.scalars().all()

    return permissions