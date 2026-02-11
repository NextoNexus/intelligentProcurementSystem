"""
AI智能聊天API路由
"""
from fastapi import APIRouter

router = APIRouter()

@router.post("/chat")
async def chat_with_ai():
    """与AI聊天（待实现）"""
    return {"message": "AI聊天功能待实现"}

@router.post("/query")
async def query_database():
    """只读数据库查询（待实现）"""
    return {"message": "只读数据库查询功能待实现"}