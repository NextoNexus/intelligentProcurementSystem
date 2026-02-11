"""
财务管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_finance_data():
    """获取财务数据（待实现）"""
    return {"message": "财务管理API待实现"}