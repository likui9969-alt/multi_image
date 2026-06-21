from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import engine, Base
from app.api import auth, images, history
from app.api.tasks import router as tasks_router, process_router
from app.cleanup import start_cleanup_daemon

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

# CORS：从环境变量读取白名单，默认仅允许本地开发地址
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库表
Base.metadata.create_all(bind=engine)

# 注册路由（每个 router 仅注册一次）
app.include_router(auth.router)
app.include_router(images.router)
app.include_router(tasks_router)   # /api/tasks
app.include_router(process_router)  # /api/process
app.include_router(history.router)  # /api/history


@app.get("/api/health", tags=["健康检查"])
def health():
    """轻量健康检查接口，不暴露 Swagger UI 信息"""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.on_event("startup")
def _on_startup():
    """应用启动时初始化后台任务"""
    # 启动文件清理守护线程（TTL 由 FILE_TTL_HOURS 控制）
    if settings.FILE_TTL_HOURS > 0:
        start_cleanup_daemon(interval_seconds=3600)


# 创建并挂载静态文件目录
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.RESULT_DIR).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/results", StaticFiles(directory=settings.RESULT_DIR), name="results")
