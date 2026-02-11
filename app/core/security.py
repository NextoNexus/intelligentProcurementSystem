"""
安全配置模块
密码哈希、JWT令牌生成与验证
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

# 密码上下文
# 暂时使用pbkdf2_sha256，bcrypt在Windows上有兼容性问题
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建访问令牌

    Args:
        data: 要编码的数据（通常是用户ID和角色）
        expires_delta: 过期时间间隔，如未提供则使用默认设置

    Returns:
        JWT令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建刷新令牌

    Args:
        data: 要编码的数据
        expires_delta: 过期时间间隔，如未提供则使用默认设置

    Returns:
        JWT令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    验证JWT令牌

    Args:
        token: JWT令牌字符串

    Returns:
        解码后的数据字典，如果验证失败则返回None
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


def decode_token(token: str) -> Dict[str, Any]:
    """
    解码JWT令牌（不验证过期）

    Args:
        token: JWT令牌字符串

    Returns:
        解码后的数据字典

    Raises:
        JWTError: 令牌无效或解码失败
    """
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm], options={"verify_exp": False})


def get_token_type(token: str) -> Optional[str]:
    """
    获取令牌类型（access或refresh）

    Args:
        token: JWT令牌字符串

    Returns:
        令牌类型字符串，如果无效则返回None
    """
    try:
        payload = decode_token(token)
        return payload.get("type")
    except JWTError:
        return None