"""
数据库模型基类
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

from ..core.database import Base as DatabaseBase


class Base(DatabaseBase):
    """所有模型的抽象基类"""
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """自动从类名生成表名（驼峰转蛇形）"""
        name = cls.__name__
        return ''.join(
            ['_' + c.lower() if c.isupper() else c for c in name]
        ).lstrip('_')

    # 公共字段
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        nullable=False,
        comment="主键ID"
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="更新时间"
    )
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="软删除标记"
    )
    deleted_at = Column(
        DateTime,
        nullable=True,
        comment="删除时间"
    )

    def to_dict(self, exclude: list = None) -> dict:
        """
        将模型实例转换为字典

        Args:
            exclude: 要排除的字段列表

        Returns:
            字典表示的模型数据
        """
        exclude = exclude or []
        result = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                # 处理特殊类型
                if isinstance(value, datetime):
                    value = value.isoformat()
                elif isinstance(value, uuid.UUID):
                    value = str(value)
                result[column.name] = value
        return result

    def update(self, **kwargs) -> None:
        """
        更新模型字段

        Args:
            **kwargs: 要更新的字段和值
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def soft_delete(self) -> None:
        """软删除"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()