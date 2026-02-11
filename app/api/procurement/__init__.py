"""
采购管理API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 导入路由（待实现）
# from . import routes
# router.include_router(routes.router)

# 临时路由
@router.get("/")
async def get_procurement():
    """获取采购信息（临时）"""
    return {"message": "采购管理API - 待实现"}