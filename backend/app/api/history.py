from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.image_task import ImageTask
from app.schemas.task import TaskResponse

router = APIRouter(prefix="/api/history", tags=["历史记录"])


@router.get("")
def list_history(
    page: int = Query(1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量，1-100"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取当前用户的历史记录（分页）"""
    base_query = (
        db.query(ImageTask)
        .filter(ImageTask.user_id == current_user.id)
        .order_by(ImageTask.created_at.desc())
    )

    total = base_query.count()
    offset = (page - 1) * page_size
    items = base_query.offset(offset).limit(page_size).all()

    return {
        "items": [TaskResponse.model_validate(t) for t in items],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if page_size > 0 else 0,
    }


@router.delete("/{task_id}")
def delete_history(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.query(ImageTask).filter(
        ImageTask.id == task_id,
        ImageTask.user_id == current_user.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="记录不存在")

    db.delete(task)
    db.commit()
    return {"message": "删除成功"}
