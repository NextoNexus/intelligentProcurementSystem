"""
业务分析API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 临时路由
@router.get("/")
async def get_analytics():
    """获取分析信息（临时）"""
    return {"message": "业务分析API - 待实现"}