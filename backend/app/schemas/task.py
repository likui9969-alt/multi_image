from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaskResponse(BaseModel):
    id: int
    original_filename: str
    style_type: Optional[str]
    status: str
    result_image_path: Optional[str] = None
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProcessRequest(BaseModel):
    task_id: int
    style_type: str


class ProcessResponse(BaseModel):
    task_id: int
    result_url: str
    result_image_path: Optional[str] = None
    status: str


class HistoryResponse(BaseModel):
    """分页历史记录响应"""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class UploadResponse(BaseModel):
    """上传响应"""
    task_id: int
    file_path: str
    url: str
    filename: str
    stored_filename: str
    size: int
    status: str
