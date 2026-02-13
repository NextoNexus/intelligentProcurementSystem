"""
角色相关的Pydantic模型
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field


class RoleBase(BaseModel):
    """角色基础模型"""
    name: str = Field(..., min_length=1, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")
    is_system: bool = Field(default=False, description="是否为系统内置角色")


class RoleCreate(RoleBase):
    """创建角色请求模型"""
    permission_ids: Optional[List[UUID]] = Field(default_factory=list, description="权限ID列表")


class RoleUpdate(BaseModel):
    """更新角色请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")
    permission_ids: Optional[List[UUID]] = Field(None, description="权限ID列表")


class RoleResponse(RoleBase):
    """角色信息响应模型"""
    id: UUID = Field(..., description="角色ID")
    user_count: int = Field(default=0, description="用户数量")
    permissions: List[str] = Field(default_factory=list, description="权限代码列表")
    permission_ids: List[UUID] = Field(default_factory=list, description="权限ID列表")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    """权限基础模型"""
    code: str = Field(..., min_length=1, max_length=100, description="权限代码")
    name: str = Field(..., min_length=1, max_length=100, description="权限名称")
    description: Optional[str] = Field(None, description="权限描述")
    module: str = Field(..., min_length=1, max_length=50, description="所属模块")


class PermissionCreate(PermissionBase):
    """创建权限请求模型"""
    pass


class PermissionResponse(PermissionBase):
    """权限信息响应模型"""
    id: UUID = Field(..., description="权限ID")
    role_count: int = Field(default=0, description="角色数量")
    created_at: Optional[datetime] = Field(None, description="创建时间")

    class Config:
        from_attributes = True


class RoleSimpleResponse(BaseModel):
    """简化角色响应模型（用于下拉选择等场景）"""
    id: UUID = Field(..., description="角色ID")
    name: str = Field(..., description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")

    class Config:
        from_attributes = True


class PermissionSimpleResponse(BaseModel):
    """简化权限响应模型"""
    id: UUID = Field(..., description="权限ID")
    code: str = Field(..., description="权限代码")
    name: str = Field(..., description="权限名称")
    module: str = Field(..., description="所属模块")

    class Config:
        from_attributes = True