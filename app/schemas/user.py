"""
用户相关的Pydantic模型
"""
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, max_length=100, description="姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    employee_id: Optional[str] = Field(None, max_length=50, description="员工工号")
    department: Optional[str] = Field(None, max_length=100, description="部门")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    hire_date: Optional[datetime] = Field(None, description="入职日期")


class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str = Field(..., min_length=8, description="密码（至少8个字符）")
    is_active: bool = Field(default=True, description="是否激活")
    is_verified: bool = Field(default=False, description="邮箱是否验证")
    role_ids: Optional[List[UUID]] = Field(default_factory=list, description="角色ID列表")


class UserUpdate(BaseModel):
    """更新用户请求模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    full_name: Optional[str] = Field(None, max_length=100, description="姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    avatar_url: Optional[str] = Field(None, description="头像URL")
    employee_id: Optional[str] = Field(None, max_length=50, description="员工工号")
    department: Optional[str] = Field(None, max_length=100, description="部门")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    hire_date: Optional[datetime] = Field(None, description="入职日期")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_verified: Optional[bool] = Field(None, description="邮箱是否验证")
    password: Optional[str] = Field(None, min_length=8, description="新密码")


class UserResponse(UserBase):
    """用户信息响应模型"""
    id: UUID = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")
    is_verified: bool = Field(..., description="邮箱是否验证")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")
    last_login_ip: Optional[str] = Field(None, description="最后登录IP")
    roles: List[str] = Field(default_factory=list, description="角色名称列表")
    role_ids: List[UUID] = Field(default_factory=list, description="角色ID列表")
    permissions: List[str] = Field(default_factory=list, description="权限代码列表")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    @field_validator('roles', mode='before')
    @classmethod
    def convert_roles_to_strings(cls, v: Any) -> List[str]:
        """将Role对象列表转换为角色名称字符串列表"""
        if not v:
            return []
        # 如果已经是字符串，直接返回
        if isinstance(v[0], str):
            return v
        # 假设v是Role对象列表
        return [role.name if hasattr(role, 'name') else str(role) for role in v]

    @field_validator('role_ids', mode='before')
    @classmethod
    def convert_role_ids_to_uuid(cls, v: Any) -> List[UUID]:
        """将Role对象列表或UUID列表转换为UUID列表"""
        if not v:
            return []
        # 如果已经是UUID，直接返回
        if isinstance(v[0], UUID):
            return v
        # 假设v是Role对象列表，提取id
        return [role.id if hasattr(role, 'id') else role for role in v]

    class Config:
        from_attributes = True


class UserSimpleResponse(BaseModel):
    """简化用户响应模型（用于下拉选择等场景）"""
    id: UUID = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    full_name: Optional[str] = Field(None, description="姓名")
    department: Optional[str] = Field(None, description="部门")

    class Config:
        from_attributes = True