"""
报表管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_reports():
    """获取报表列表（待实现）"""
    return {"message": "报表管理API待实现"}