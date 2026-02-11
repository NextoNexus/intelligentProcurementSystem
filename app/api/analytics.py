"""
业务分析API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_analytics():
    """获取业务分析数据（待实现）"""
    return {"message": "业务分析API待实现"}