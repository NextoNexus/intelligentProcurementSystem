"""
报表管理API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 临时路由
@router.get("/")
async def get_reports():
    """获取报表信息（临时）"""
    return {"message": "报表管理API - 待实现"}