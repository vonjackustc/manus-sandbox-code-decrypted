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
app.add_middleware(CORSMiddleware, allow_origins = [
    '*'], allow_credentials = True, allow_methods = [
    '*'], allow_headers = [
    '*'])

class FileUploadRequest(BaseModel):
    file_path: str
    presigned_url: str

MULTIPART_THRESHOLD = 10485760
upload_file = lambda cmd: None
multipart_upload = lambda cmd: None
get_file = lambda path: None

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

batch_download = lambda cmd: None
browser_manager = BrowserManager()
browser_status = None
browser_action = lambda cmd: None
text_editor_endpoint = lambda cmd: None
terminal_socket_server = TerminalSocketServer()
websocket_endpoint = lambda ws: None
reset_terminal = lambda terminal_id: None
reset_all_terminals = None
view_terminal = lambda terminal_id, full: None
kill_terminal_process = lambda terminal_id: None
write_terminal_process = lambda terminal_id, cmd: None

class InitSandboxRequest(BaseModel):
    secrets: Dict[(str, str)]

init_sandbox = lambda request: None
healthz = None

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

zip_and_upload = lambda request: None

def create_zip_archive(source_dir, output_zip):
    '''
    Create a zip archive of a directory, excluding node_modules and .next

    Args:
        source_dir: Path to the directory to zip
        output_zip: Path for the output zip file

    Returns:
        tuple[bool, str]: (success, error_message)
    '''
    '__pyarmor_enter_39554__(...)'
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

