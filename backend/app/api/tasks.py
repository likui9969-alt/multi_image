from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.image_task import ImageTask
from app.schemas.task import ProcessRequest, ProcessResponse, TaskResponse
from app.ai_service import call_style_transfer

router = APIRouter(prefix="/api/tasks", tags=["任务管理"])


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_status(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """查询任务状态"""
    task = db.query(ImageTask).filter(
        ImageTask.id == task_id,
        ImageTask.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return _build_task_response(task)


process_router = APIRouter(prefix="/api/process", tags=["图片处理"])


@process_router.post("", response_model=ProcessResponse)
async def process_image(
    req: ProcessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """提交风格转换任务

    1. 查找已上传的任务
    2. 调用 Stability AI（或 Mock）进行风格转换
    3. 保存结果图片
    4. 返回 task_id + result_url
    """
    task = db.query(ImageTask).filter(
        ImageTask.id == req.task_id,
        ImageTask.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    if task.status == "processing":
        raise HTTPException(status_code=400, detail="任务正在处理中，请稍后再试")

    # 标记为处理中
    task.status = "processing"
    task.style_type = req.style_type
    db.commit()

    # ============================
    # 核心：调用 AI 风格转换
    # ============================
    try:
        result_data = await call_style_transfer(
            task.original_image_path, req.style_type
        )

        result_dir = Path(settings.RESULT_DIR)
        result_dir.mkdir(parents=True, exist_ok=True)
        result_filename = f"{task.id}_{req.style_type}.png"
        result_path = result_dir / result_filename
        result_path.write_bytes(result_data)

        task.result_image_path = str(result_path)
        task.status = "completed"

    except PermissionError as e:
        # API Key 错误
        task.status = "failed"
        task.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

    except RuntimeError as e:
        # 网络/余额/频率限制/服务器错误
        task.status = "failed"
        task.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=502, detail=str(e))

    except Exception as e:
        task.status = "failed"
        task.error_message = str(e)[:500]
        db.commit()
        raise HTTPException(status_code=500, detail=f"转换失败: {e}")

    finally:
        db.commit()
        db.refresh(task)

    result_url = f"/results/{task.id}_{req.style_type}.png"
    return ProcessResponse(
        task_id=task.id,
        result_url=result_url,
        result_image_path=str(result_path),
        status="completed",
    )


# ============================================================
# 辅助函数
# ============================================================
def _build_task_response(task: ImageTask) -> TaskResponse:
    """构造 TaskResponse，补充 result_url"""
    data = TaskResponse.model_validate(task)
    if task.result_image_path:
        filename = Path(task.result_image_path).name
        data.result_url = f"/results/{filename}"
    return data
