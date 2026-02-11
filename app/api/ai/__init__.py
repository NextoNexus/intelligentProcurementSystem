"""
AI智能聊天API模块
"""
from fastapi import APIRouter

router = APIRouter()

# 导入路由（待实现）
# from . import routes
# router.include_router(routes.router)

# 临时路由
@router.get("/")
async def get_ai_info():
    """获取AI信息（临时）"""
    return {"message": "AI智能聊天API - 待实现"}