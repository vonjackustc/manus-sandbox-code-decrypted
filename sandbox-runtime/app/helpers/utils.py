import asyncio
import logging
import os
from typing import List
import aiohttp
from app.models import PartUploadResult, PresignedUrlPart
from urllib.parse import quote

logger = logging.getLogger(__name__)

def truncate_text_from_back(text: str, max_len: int) -> str:
    """裁剪并保留最后 max_len 长度的文本"""
    if len(text) > max_len:
        return '[previous content truncated]...' + text[-max_len:]
    else:
        return '[previous content truncated]...' + text

def truncate_text(text: str, max_len: int) -> str:
    """裁剪并保留前 max_len 长度的文本"""
    if len(text) > max_len:
        return text[:max_len] + '...[content truncated]'
    else:
        return text + '...[content truncated]'

def ensure_dir_exists(dir_path: str) -> None:
    """确保文件所在目录存在"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

async def upload_to_presigned_url(data: bytes, presigned_url: str, content_type: str, filename: str) -> bool:
    """Upload data to a presigned URL using aiohttp."""
    pass


async def upload_part(session: aiohttp.ClientSession, url: str, data: bytes, part_number: int) -> PartUploadResult:
    """Upload a single part to S3 using presigned URL"""
    pass


class FilePartReader:
    
    def __init__(self, file_path: str, part_size: int):
        self.file_path = file_path
        self.part_size = part_size
        self._file = None
    
    async def __aenter__(self):
        self._file = open(self.file_path, 'rb')
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
    
    def read_part(self, part_number: int) -> bytes:
        """读取指定分片的数据"""
        _var_var_6 = (part_number - 1) * self.part_size
        self._file.seek(_var_var_6)
        return self._file.read(self.part_size)

async def upload_file_parts(file_path: str, presigned_urls: List[PresignedUrlPart], part_size: int, max_concurrent: int=4) -> List[PartUploadResult]:
    """
    并发上传文件分片

    Args:
        file_path: 文件路径
        presigned_urls: 预签名URL列表
        part_size: 分片大小（字节）
        max_concurrent: 最大并发数
    """
    pass