"""
供应商管理API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_suppliers():
    """获取供应商列表（待实现）"""
    return {"message": "供应商管理API待实现"}

@router.get("/{supplier_id}")
async def get_supplier(supplier_id: str):
    """获取供应商详情（待实现）"""
    return {"message": f"获取供应商 {supplier_id} 详情（待实现）"}