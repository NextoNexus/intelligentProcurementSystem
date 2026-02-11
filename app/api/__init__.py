"""
API路由模块
导出所有API路由
"""
from .auth import router as auth
from .suppliers import router as suppliers
from .procurement import router as procurement
from .inventory import router as inventory
from .ai import router as ai
from .finance import router as finance
from .analytics import router as analytics
from .reports import router as reports

__all__ = [
    "auth",
    "suppliers",
    "procurement",
    "inventory",
    "ai",
    "finance",
    "analytics",
    "reports",
]