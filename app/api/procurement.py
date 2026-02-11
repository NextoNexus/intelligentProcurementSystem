"""
采购管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/requests")
async def get_procurement_requests():
    """获取采购需求列表（待实现）"""
    return {"message": "采购管理API待实现"}

@router.post("/requests")
async def create_procurement_request():
    """创建采购需求（待实现）"""
    return {"message": "创建采购需求（待实现）"}