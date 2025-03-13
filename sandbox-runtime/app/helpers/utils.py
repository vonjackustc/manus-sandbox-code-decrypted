import asyncio
import logging
import os
from typing import List
import aiohttp
from app.models import PartUploadResult, PresignedUrlPart
from urllib.parse import quote

logger = logging.getLogger(__name__)

def truncate_text_from_back(text, max_len):
    '''裁剪并保留最后 max_len 长度的文本'''
    if len(text) > max_len:
        pass
    else:
        None('[previous content truncated]...' + text[-max_len:])
        return None
    return '[previous content truncated]...' + text[-max_len:]

def truncate_text(text, max_len):
    '''裁剪并保留前 max_len 长度的文本'''
    if len(text) > max_len:
        pass
    else:
        None(text[:max_len] + '...[content truncated]')
        return None
    return text[:max_len] + '...[content truncated]'

def ensure_dir_exists(dir_path):
    '''确保文件所在目录存在'''
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

async def upload_to_presigned_url(data, presigned_url, content_type, filename):
    '''Upload data to a presigned URL using aiohttp.'''
    pass


async def upload_part(session, url, data, part_number):
    '''Upload a single part to S3 using presigned URL'''
    pass


class FilePartReader:
    
    def __init__(self, file_path, part_size):
        self.file_path = file_path
        self.part_size = part_size
        self._file = None
    
    async def __aenter__(self):
        pass
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def read_part(self, part_number):
        '''读取指定分片的数据'''
        _var_var_6 = (part_number - 1) * self.part_size
        self._file.seek(_var_var_6)
        return self._file.read(self.part_size)

async def upload_file_parts(file_path, presigned_urls, part_size, max_concurrent):
    '''
    并发上传文件分片

    Args:
        file_path: 文件路径
        presigned_urls: 预签名URL列表
        part_size: 分片大小（字节）
        max_concurrent: 最大并发数
    '''
    pass