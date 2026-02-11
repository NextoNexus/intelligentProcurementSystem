"""
财务管理API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 临时路由
@router.get("/")
async def get_finance():
    """获取财务信息（临时）"""
    return {"message": "财务管理API - 待实现"}