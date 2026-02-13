"""
用户相关模型
"""
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Text, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


# 用户角色关联表（多对多）
user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('role.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    comment='用户角色关联表'
)


class Role(Base):
    """角色模型"""
    __tablename__ = 'role'

    # 角色信息
    name = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='角色名称（如：admin, manager, employee）'
    )
    description = Column(
        Text,
        nullable=True,
        comment='角色描述'
    )
    is_system = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='是否为系统内置角色'
    )

    # 关系
    users = relationship(
        'User',
        secondary=user_role,
        back_populates='roles',
        lazy='selectin'
    )
    permissions = relationship(
        'Permission',
        secondary='role_permission',
        back_populates='roles',
        lazy='selectin'
    )

    def __repr__(self) -> str:
        return f'<Role {self.name}>'

    def __str__(self) -> str:
        return self.name


class Permission(Base):
    """权限模型"""
    __tablename__ = 'permission'

    # 权限信息
    code = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment='权限代码（如：user:create, procurement:approve）'
    )
    name = Column(
        String(100),
        nullable=False,
        comment='权限名称'
    )
    description = Column(
        Text,
        nullable=True,
        comment='权限描述'
    )
    module = Column(
        String(50),
        nullable=False,
        index=True,
        comment='所属模块（如：user, procurement, supplier）'
    )

    # 关系
    roles = relationship(
        'Role',
        secondary='role_permission',
        back_populates='permissions',
        lazy='selectin'
    )


# 角色权限关联表（多对多）
role_permission = Table(
    'role_permission',
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('role.id'), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permission.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    comment='角色权限关联表'
)


class User(Base):
    """用户模型"""
    __tablename__ = 'user'

    # 用户基本信息
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment='用户名'
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment='邮箱'
    )
    hashed_password = Column(
        String(255),
        nullable=False,
        comment='密码哈希'
    )
    full_name = Column(
        String(100),
        nullable=True,
        comment='姓名'
    )
    phone = Column(
        String(20),
        nullable=True,
        index=True,
        comment='手机号'
    )
    avatar_url = Column(
        String(500),
        nullable=True,
        comment='头像URL'
    )

    # 用户状态
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment='是否激活'
    )
    is_verified = Column(
        Boolean,
        default=False,
        nullable=False,
        comment='邮箱是否验证'
    )
    last_login_at = Column(
        DateTime,
        nullable=True,
        comment='最后登录时间'
    )
    last_login_ip = Column(
        String(45),
        nullable=True,
        comment='最后登录IP'
    )

    # 员工信息
    employee_id = Column(
        String(50),
        nullable=True,
        unique=True,
        index=True,
        comment='员工工号'
    )
    department = Column(
        String(100),
        nullable=True,
        comment='所属部门'
    )
    position = Column(
        String(100),
        nullable=True,
        comment='职位'
    )
    hire_date = Column(
        DateTime,
        nullable=True,
        comment='入职日期'
    )

    # 关系
    roles = relationship(
        'Role',
        secondary=user_role,
        back_populates='users',
        lazy='selectin'
    )

    # 采购相关关系
    procurement_requests = relationship(
        'ProcurementRequest',
        back_populates='requester',
        lazy='dynamic',
        cascade='all, delete-orphan',
        foreign_keys='ProcurementRequest.requester_id'
    )
    approved_requests = relationship(
        'ProcurementRequest',
        back_populates='approver',
        lazy='dynamic',
        foreign_keys='ProcurementRequest.approver_id'
    )

    def __repr__(self) -> str:
        return f'<User {self.username}>'

    @property
    def permissions(self) -> list:
        """获取用户所有权限"""
        perms = set()
        for role in self.roles:
            for perm in role.permissions:
                perms.add(perm.code)
        return list(perms)

    def has_role(self, role_name: str) -> bool:
        """检查用户是否具有指定角色"""
        return any(role.name == role_name for role in self.roles)

    def has_permission(self, permission_code: str) -> bool:
        """检查用户是否具有指定权限"""
        return permission_code in self.permissions

    @property
    def role_ids(self) -> list:
        """获取用户角色ID列表"""
        return [role.id for role in self.roles]

    @property
    def role_names(self) -> list:
        """获取用户角色名称列表"""
        return [role.name for role in self.roles]