import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.image_task import ImageTask

router = APIRouter(prefix="/api/images", tags=["图片上传"])


def validate_image(filename: str) -> bool:
    ext = Path(filename).suffix.lower()
    return ext in settings.ALLOWED_EXTENSIONS


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not validate_image(file.filename):
        raise HTTPException(status_code=400, detail="不支持的文件格式，仅支持 JPG/PNG/WEBP")

    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"文件大小不能超过 {settings.MAX_UPLOAD_SIZE_MB}MB")

    ext = Path(file.filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    save_path = Path(settings.UPLOAD_DIR) / unique_name
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_bytes(content)

    task = ImageTask(
        user_id=current_user.id,
        original_filename=file.filename,
        original_image_path=str(save_path),
        status="uploaded",
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    # 统一返回字段：file_path / url / filename / size / task_id / status
    return {
        "task_id": task.id,
        "file_path": str(save_path).replace("\\", "/"),
        "url": f"/uploads/{unique_name}",
        "filename": file.filename,
        "stored_filename": unique_name,
        "size": len(content),
        "status": task.status,
    }
