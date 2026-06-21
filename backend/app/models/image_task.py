from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func

from app.database import Base


class ImageTask(Base):
    __tablename__ = "image_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    original_filename = Column(String(255), nullable=False)
    original_image_path = Column(String(500), nullable=False)
    result_image_path = Column(String(500), nullable=True)
    style_type = Column(String(50), nullable=True)
    status = Column(String(20), nullable=False, default="uploaded", index=True)
    error_message = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
