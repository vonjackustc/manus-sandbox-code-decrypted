import asyncio
import os
import random
import urllib
import urllib.parse as urllib
from datetime import datetime
from typing import Literal
from playwright._impl._errors import TargetClosedError
from app.helpers.tool_helpers import run_shell
from app.helpers.utils import upload_to_presigned_url
from app.logger import logger
from app.tools.base import DEFAULT_WORKING_DIR
from app.types.browser_types import BrowserActionResult
from app.types.messages import BrowserActionRequest
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from browser_use.browser.context import BrowserContext, ScreenshotError
from browser_use.browser.context import PageDeadError
from browser_use.controller.service import Controller

class BrowserDeadError(Exception):
    pass


class BrowserManager:
    """
    browser agent 基于 browser-use 和 playwright, 用于执行所有浏览器相关操作
    """
    browser: Browser
    browser_context: BrowserContext
    controller: Controller
    include_attributes: list[str]
    status: Literal['started', 'initializing', 'ready'] = 'started'
    
    def __init__(self, *, chrome_instance_path: str | None=None, headless: bool | None=None):
        _var_var_0 = chrome_instance_path or os.getenv('CHROME_INSTANCE_PATH', None)
        if headless is None:
            if _var_var_0 is not None:
                headless = False
            else:
                headless = True
        logger.info(f'CHROME_INSTANCE_PATH: {_var_var_0}')
        self.browser = Browser(config=BrowserConfig(headless=headless, chrome_instance_path=_var_var_0))
        self.browser_context = BrowserContext(browser=self.browser, config=BrowserContextConfig())
        self.controller = Controller()
        self.include_attributes = ['title', 'type', 'name', 'role', 'tabindex', 'aria-label', 'placeholder', 'value', 'alt', 'aria-expanded']
        from .browser_actions import register_browser_actions
        register_browser_actions(self)
    
    async def initialize(self):
        self.status = 'initializing'
        await self.browser_context.get_session()
        self.status = 'ready'
    
    async def recreate_page(self):
        _var_var_2 = await self.browser_context.get_current_page()
        await self.browser_context.create_new_tab()
        await _var_var_2.close()
    
    async def execute_action(self, cmd: BrowserActionRequest) -> BrowserActionResult:
        pass

    async def restart_browser(self):
        await self.browser.close()
        await self.browser_context.close()
        logger.info('try restart chrome')
        _var_var_14, _var_var_15, _var_var_16 = await run_shell('sudo supervisorctl restart chrome')
        if _var_var_16:
            raise Exception(_var_var_16)
        else:
            logger.info(_var_var_15)
            logger.info('chrome restarted')
            await self.browser.get_playwright_browser()
    
    async def health_check(self):
        pass
    
    def get_screenshot_save_path(self, page_url: str):
        _var_var_21 = f'{DEFAULT_WORKING_DIR}/screenshots'
        _var_var_22 = urllib.parse.urlparse(page_url)
        _var_var_23 = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        _var_var_24 = random.randint(1000, 9999)
        if _var_var_22.scheme in ('http', 'https') and _var_var_22.hostname:
            _var_var_25 = _var_var_22.hostname.replace('.com', '').replace('www.', '').replace('.', '_')
        else:
            _var_var_25 = page_url.split('/').pop().replace('.', '_')
        return f'{_var_var_21}/{_var_var_25}_{_var_var_23}_{_var_var_24}.webp'
        
    async def upload_screenshots(self, cmd: BrowserActionRequest, clean_screenshot: bytes, marked_screenshot: bytes):
        if cmd.screenshot_presigned_url:
            if await upload_to_presigned_url(marked_screenshot, cmd.screenshot_presigned_url, 'image/webp', 'marked.webp'):
                logger.info(f'Screenshot uploaded successfully to {cmd.screenshot_presigned_url}')
            else:
                logger.error('Failed to upload screenshot')
        else:
            logger.info('No presigned URL provided for screenshot, skipped uploading')
        if cmd.clean_screenshot_presigned_url:
            if await upload_to_presigned_url(clean_screenshot, cmd.clean_screenshot_presigned_url, 'image/webp', 'clean.webp'):
                logger.info(f'Clean screenshot uploaded successfully to {cmd.clean_screenshot_presigned_url}')
            else:
                logger.error('Failed to upload clean screenshot')
        else:
            logger.info('No presigned clean URL provided for screenshot, skipped uploading')