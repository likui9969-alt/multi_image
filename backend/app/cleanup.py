"""文件清理服务：按 TTL 自动清理 uploads / results 目录中的过期文件"""
import os
import time
import logging
from pathlib import Path
from threading import Thread

from app.config import settings

logger = logging.getLogger(__name__)


def cleanup_expired_files(ttl_hours: int = None) -> int:
    """
    清理 uploads 和 results 目录中超过 TTL 的文件。
    返回已删除的文件数量。
    """
    ttl = ttl_hours if ttl_hours is not None else settings.FILE_TTL_HOURS
    if ttl <= 0:
        return 0  # 关闭清理

    now = time.time()
    cutoff = now - ttl * 3600
    deleted = 0

    for directory in (settings.UPLOAD_DIR, settings.RESULT_DIR):
        dir_path = Path(directory)
        if not dir_path.exists():
            continue

        for entry in dir_path.iterdir():
            try:
                if not entry.is_file():
                    continue
                mtime = entry.stat().st_mtime
                if mtime < cutoff:
                    entry.unlink()
                    deleted += 1
                    logger.info("清理过期文件: %s (mtime=%s)", entry, mtime)
            except Exception as e:
                logger.warning("清理文件失败 %s: %s", entry, e)

    return deleted


def _cleanup_loop(interval_seconds: int = 3600):
    """后台清理循环，默认每小时执行一次"""
    while True:
        try:
            cleanup_expired_files()
        except Exception as e:
            logger.error("文件清理任务异常: %s", e)
        time.sleep(interval_seconds)


def start_cleanup_daemon(interval_seconds: int = 3600) -> Thread:
    """启动后台清理守护线程"""
    thread = Thread(target=_cleanup_loop, args=(interval_seconds,), daemon=True)
    thread.start()
    logger.info(
        "文件清理守护线程已启动 (TTL=%s 小时, 间隔=%s 秒)",
        settings.FILE_TTL_HOURS,
        interval_seconds,
    )
    return thread
