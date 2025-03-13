import asyncio
from typing import Any
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from logger import logger
from tools.terminal import terminal_manager
from types.messages import TerminalInputMessage, TerminalOutputMessage, TerminalStatus

class TerminalSocketServer:    
    async def handle_connection(self, ws: WebSocket):
        pass
    
    async def send_resp(self, ws: WebSocket, resp: TerminalOutputMessage):
        pass
    
    async def handle_msg(self, msg: TerminalInputMessage, ws: WebSocket):
        logger.info(f'Handle terminal socket msg#{msg.action_id} {msg}')
        await self._do_handle_msg(msg, ws)
        logger.info(f'Finished handling msg#{msg.action_id}')
    
    async def _do_handle_msg(self, msg: TerminalInputMessage, ws: WebSocket):
        pass