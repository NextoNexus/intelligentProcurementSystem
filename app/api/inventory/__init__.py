"""
库存管理API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 导入路由（待实现）
# from . import routes
# router.include_router(routes.router)

# 临时路由
@router.get("/")
async def get_inventory():
    """获取库存信息（临时）"""
    return {"message": "库存管理API - 待实现"}