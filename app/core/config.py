"""
应用配置管理模块
使用pydantic的BaseSettings从环境变量加载配置
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field


class Settings(BaseSettings):
    """应用配置类"""

    # 基础配置
    app_name: str = Field(default="智能物资采购系统", description="应用名称")
    app_version: str = Field(default="0.1.0", description="应用版本")
    debug: bool = Field(default=False, description="调试模式")

    # 数据库配置
    database_url: PostgresDsn = Field(
        default="postgresql://user:password@localhost:5432/procurement_db",
        description="PostgreSQL数据库连接URL"
    )
    database_pool_size: int = Field(default=20, description="数据库连接池大小")
    database_max_overflow: int = Field(default=40, description="数据库连接池最大溢出")

    # 安全配置
    secret_key: str = Field(default="your-secret-key-here-change-in-production", description="JWT密钥")
    algorithm: str = Field(default="HS256", description="加密算法")
    access_token_expire_minutes: int = Field(default=30, description="访问令牌过期时间（分钟）")
    refresh_token_expire_days: int = Field(default=7, description="刷新令牌过期时间（天）")

    # AI服务配置
    ai_provider_api_key: str = Field(default="", description="AI服务提供商API密钥")
    ai_model: str = Field(default="gpt-4o-mini", description="AI模型名称")
    ai_base_url: str = Field(default="https://api.openai.com/v1", description="AI服务基础URL")

    # CORS配置
    cors_origins: List[str] = Field(default=["http://localhost:5173", "http://localhost:3000"], description="CORS允许的源")
    cors_allow_credentials: bool = Field(default=True, description="是否允许CORS凭证")

    # 日志配置
    log_level: str = Field(default="INFO", description="日志级别")
    log_file: str = Field(default="logs/app.log", description="日志文件路径")

    # 邮件配置（可选）
    smtp_host: Optional[str] = Field(default=None, description="SMTP主机")
    smtp_port: Optional[int] = Field(default=587, description="SMTP端口")
    smtp_user: Optional[str] = Field(default=None, description="SMTP用户")
    smtp_password: Optional[str] = Field(default=None, description="SMTP密码")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例（用于依赖注入）"""
    return settings