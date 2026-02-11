"""
认证授权API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 导入路由
from . import routes

# 注册路由
router.include_router(routes.router)