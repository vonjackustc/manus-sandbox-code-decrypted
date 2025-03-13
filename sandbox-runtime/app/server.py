import asyncio
import math
import mimetypes
import os
import shutil
import tempfile
import time
from enum import Enum
from pathlib import Path
from typing import Dict, List
import httpx
from fastapi import Body, FastAPI, HTTPException, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from helpers.utils import upload_to_presigned_url, upload_file_parts
from logger import logger
from models import MultipartUploadRequest, MultipartUploadResponse
from router import TimedRoute
from terminal_socket_server import TerminalSocketServer
from tools.base import ToolError
from tools.browser.browser_manager import BrowserDeadError, BrowserManager, PageDeadError
from tools.terminal import terminal_manager
from tools.text_editor import text_editor
from types.messages import BrowserActionRequest, BrowserActionResponse, TerminalApiResponse, TerminalWriteApiRequest, TextEditorAction, TextEditorActionResult

app = FastAPI()
app.router.route_class = TimedRoute
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])


class FileUploadRequest(BaseModel):
    file_path: str
    presigned_url: str

MULTIPART_THRESHOLD = 10485760

@app.post('/file/upload_to_s3')
async def upload_file(cmd: FileUploadRequest=Body()):
    """
    Upload a file to S3. If file size exceeds threshold, return size information instead.
    
    Request body:
    {
        "file_path": str,         # The local file path to upload
        "presigned_url": str      # The presigned URL to upload to
        }
        
        Returns:
        - For small files: Uploads the file and returns success response
        - For large files: Returns file information for multipart upload
    """
    pass

@app.post('/file/multipart_upload_to_s3')
async def multipart_upload(cmd: MultipartUploadRequest=Body(...)):
    """
    使用预签名URLs上传文件分片
    
    Request body:
    {
        "file_path": str,              # 要上传的文件路径
        "presigned_urls": [            # 预签名URL列表
        {
            "part_number": int,    # 分片编号（从1开始）
            "url": str             # 该分片的预签名URL
            },
            ...
            ],
            "part_size": int              # 每个分片的大小（字节）
            }
    """
    pass

@app.get('/file')
async def get_file(path: str):
    """
    Download file endpoint
    Query params:
    path: str - The file path to download
    """
    pass

class DownloadItem(BaseModel):
    url: str
    filename: str


class DownloadRequest(BaseModel):
    files: List[DownloadItem]
    folder: str | None = None


class DownloadResult(BaseModel):
    filename: str
    success: bool
    error: str | None = None

@app.post('/request-download-attachments')
async def batch_download(cmd: DownloadRequest=Body()):
    """
    Batch download files endpoint
    Request body:
    {
        "files": [
            {
                "url": "https://example.com/file1.pdf",
                "filename": "file1.pdf"
                },
                ...
                ],
                "folder": "optional/subfolder/path"  # Optional folder to save files /home/ubuntu/upload/optional/subfolder/
                }
    """
    pass
        
browser_manager = BrowserManager()

@app.get('/browser/status')
async def browser_status():
    """Endpoint for browser status"""
    pass

@app.post('/browser/action')
async def browser_action(cmd: BrowserActionRequest=Body()):
    """Endpoint for browser action"""
    pass

@app.post('/text_editor')
async def text_editor_endpoint(cmd: TextEditorAction=Body()):
    """Endpoint for text editor"""
    pass

terminal_socket_server = TerminalSocketServer()

@app.websocket('/terminal')
async def websocket_endpoint(ws: WebSocket):
    return await terminal_socket_server.handle_connection(ws)
    
@app.post('/terminal/{terminal_id}/reset')
async def reset_terminal(terminal_id: str):
    """Reset a specific terminal"""
    pass

@app.post('/terminal/reset-all')
async def reset_all_terminals():
    """Reset all terminals"""
    pass

@app.get('/terminal/{terminal_id}/view')
async def view_terminal(terminal_id: str, full: bool=Query(True)):
    """View terminal history
    
    Args:
    terminal_id: The terminal ID
    full_history: If True, returns full history. If False, returns only last command output
    """
    pass
        
@app.post('/terminal/{terminal_id}/kill')
async def kill_terminal_process(terminal_id: str):
    """Kill the current process in a terminal"""
    pass

@app.post('/terminal/{terminal_id}/write')
async def write_terminal_process(terminal_id: str, cmd: TerminalWriteApiRequest=Body()):
    """write text to terminal process"""
    pass

class InitSandboxRequest(BaseModel):
    secrets: Dict[(str, str)]

@app.post('/init-sandbox')
async def init_sandbox(request: InitSandboxRequest):
    """初始化沙箱环境
    
    接收 secrets 并写入到用户的 .secrets 目录下，每个 secret 作为单独的文件
    - secrets 目录会在 $HOME/.secrets 下创建
    - 每个 secret 的 key 作为文件名
    - 如果文件已存在且内容不同，会将原文件备份（添加时间戳后缀）
    
    Args:
    request: InitSandboxRequest containing secrets dictionary
    
    Returns:
    Dict with status and processed files info
    
    Raises:
    HTTPException: If HOME environment variable is not set or other errors
    """
    pass
        
        
@app.get('/healthz')
async def healthz():
    if browser_manager.status == 'started':
        asyncio.create_task(browser_manager.initialize())
    return {'status': 'ok'}

class ProjectType(Enum, str):
    FRONTEND = 'frontend'
    BACKEND = 'backend'
    NEXTJS = 'nextjs'

class ZipAndUploadRequest(BaseModel):
    directory: str
    upload_url: str
    project_type: ProjectType

class ZipAndUploadResponse(BaseModel):
    status: str
    message: str
    error: str | None = None

@app.post('/zip-and-upload')
async def zip_and_upload(request: ZipAndUploadRequest):
    """
    Zip a directory (excluding node_modules) and upload to S3
    Request body:
    {
        "directory": "/path/to/directory",
        "upload_url": "https://s3-presigned-url...",
        "project_type": "frontend" | "backend" | "nextjs"
    }
    """
    pass

def create_zip_archive(source_dir: str, output_zip: str) -> tuple[bool, str]:
    """
    Create a zip archive of a directory, excluding node_modules and .next

    Args:
        source_dir: Path to the directory to zip
        output_zip: Path for the output zip file

    Returns:
        tuple[bool, str]: (success, error_message)
    """
    _var_var_54 = Path(source_dir).resolve()
    if not _var_var_54.is_dir():
        return (False, f'''Directory \'{source_dir}\' does not exist''')
    if not None.endswith('.zip'):
        output_zip += '.zip'
    _var_var_53 = [
        'node_modules',
        '.next',
        '.open-next',
        '.turbo',
        '.wrangler',
        '.git']
    pass
