"""
FastAPI应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from .core.config import settings
from .core.database import init_db, close_db
from .api import auth, suppliers, procurement, inventory, ai

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file) if settings.log_file else logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="企业智能物资采购管理系统",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(auth, prefix="/api/auth", tags=["认证"])
app.include_router(suppliers, prefix="/api/suppliers", tags=["供应商管理"])
app.include_router(procurement, prefix="/api/procurement", tags=["采购管理"])
app.include_router(inventory, prefix="/api/inventory", tags=["库存管理"])
app.include_router(ai, prefix="/api/ai", tags=["AI智能聊天"])

# 挂载静态文件（前端构建文件）
# app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info(f"启动{settings.app_name} v{settings.app_version}")
    logger.info(f"调试模式: {settings.debug}")

    # 初始化数据库
    try:
        await init_db()
        logger.info("数据库初始化完成")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("关闭应用...")
    await close_db()
    logger.info("数据库连接已关闭")


@app.get("/")
async def root():
    """根端点"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "运行中",
        "docs": "/docs" if settings.debug else "文档已禁用",
    }


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}


@app.get("/api/version")
async def get_version():
    """获取API版本信息"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "api_version": "v1",
        "debug": settings.debug,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )