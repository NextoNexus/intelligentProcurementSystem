"""
库存管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_inventory():
    """获取库存列表（待实现）"""
    return {"message": "库存管理API待实现"}

@router.get("/{item_id}")
async def get_inventory_item(item_id: str):
    """获取库存项详情（待实现）"""
    return {"message": f"获取库存项 {item_id} 详情（待实现）"}