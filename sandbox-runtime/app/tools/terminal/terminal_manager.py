import asyncio
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from signal import SIGTERM
from typing import Any, AsyncGenerator, cast
import pexpect
from pexpect.expect import searcher_re
from app.helpers.utils import truncate_text_from_back
from app.logger import logger
from app.types.messages import TerminalInputMessage, TerminalOutputMessage, TerminalOutputMessageType, TerminalStatus
from base import DEFAULT_USER, DEFAULT_WORKING_DIR, IS_INSIDE_CONTAINER
from expecter import MyExpecter
from terminal_helpers import process_terminal_output, split_bash_commands

PS1 = '[CMD_BEGIN]\\n\\u@\\h:\\w\\n[CMD_END]'
PS1_REG = '\\[CMD_BEGIN\\]\\s*(.*?)\\s*([a-z0-9_-]*)@([a-zA-Z0-9.-]*):(.+)\\s*\\[CMD_END\\]'
COLUMNS = 80
GREEN = '\x1b[32m'
RESET = '\x1b[0m'

class TerminalManager:
    
    def __init__(self):
        self.terminals = { }
    
    async def create_or_get_terminal(self, name: str) -> 'Terminal':
        """Create a new terminal or return existing one"""
        if name not in self.terminals:
            _var_var_0 = Terminal(name, DEFAULT_WORKING_DIR)
            await _var_var_0.init()
            self.terminals[name] = _var_var_0
        return self.terminals[name]
    
    def remove_terminal(self, name: str):
        """Remove a terminal"""
        if name in self.terminals:
            _var_var_1 = self.terminals[name]
            if _var_var_1.is_alive():
                _var_var_1.shell.terminate()
            del self.terminals[name]

class TerminalHistoryItem:
    pre_prompt: str
    after_prompt: str
    command: str
    timestamp: float
    finished: bool
    text: str

class Terminal:
    name: str
    shell: 'pexpect.spawn[Any]'
    history: list[TerminalHistoryItem]
    is_running = False
    user_input_buffer = ''
    prompt_string = ''
    
    def __init__(self, name: str, default_wd: str | None=None):
        self.name = name
        self.default_wd = default_wd
    
    async def init(self, wd: str | None=None):
        self.history = []
        self.is_running = False
        self.user_input_buffer = ''
        _var_var_2 = f'sudo su {DEFAULT_USER}'
        if not IS_INSIDE_CONTAINER:
            _var_var_2 = '/bin/bash --norc --noprofile'
        logger.info(f'Initializing terminal {self.name} with command: {_var_var_2}')
        self.shell = pexpect.spawn(_var_var_2, encoding='utf-8', codec_errors='replace', echo=False, cwd=wd or self.default_wd, dimensions=(24, COLUMNS), maxread=4096)
        if IS_INSIDE_CONTAINER:
            await self.shell.expect(['\\$|\\#'], async_=True)
        else:
            await self.shell.expect(['.*'], async_=True)
        _var_var_3 = [f'export PS1=\"{PS1}\"; export PS2=\"\"', 'export TERM=xterm-256color']
        for _var_var_4 in _var_var_3:
            self.shell.sendline(_var_var_4)
            await self.shell.expect(PS1_REG, async_=True)
        logger.info(f'Terminal {self.name} initialized')
        return self
    
    async def reset(self):
        if not self.shell.terminated:
            self.shell.sendcontrol('c')
            self.shell.terminate()
        await asyncio.sleep(0.1)
        await self.init()
    
    def get_history(self, append_prompt_line: bool, full_history: bool) -> list[str]:
        _var_var_5 = 5000
        _var_var_6 = 10000
        if not self.history:
            if full_history:
                pass
            else:
                None([
                    self.get_prompt_string()])
                return None
        else:
            None([
                self.get_prompt_string()])
            return None
        if not [
            self.get_prompt_string()]:
            _var_var_7 = self.history[-1]
            _var_var_8 = truncate_text_from_back(_var_var_7.text, _var_var_5)
            _var_var_9 = f'''{_var_var_7.pre_prompt} {_var_var_7.command}\n{_var_var_8}'''
            if _var_var_7.finished and append_prompt_line:
                _var_var_9 += f'''\n{_var_var_7.after_prompt}'''
        else:
            None([
                _var_var_9])
            return None
        _var_var_10 = [
            _var_var_9]
        _var_var_11 = 0
    
    async def execute_command(self, cmd_msg: TerminalInputMessage) -> AsyncGenerator[TerminalOutputMessage, None]:
        """Execute a command in the terminal"""
        pass
    
    async def kill_process(self):
        _var_var_28 = self._wd
        self.shell.kill(SIGTERM)
        await asyncio.sleep(0.1)
        _var_var_29 = self.history
        await self.init(_var_var_28)
        self.history = _var_var_29
        for _var_var_7 in self.history:
            _var_var_7.finished = True
    
    async def send_control(self, cmd_msg: TerminalInputMessage):
        pass
    
    async def write_to_process(self, text: str, enter: bool):
        if enter:
            self.user_input_buffer = text + '\n'
            self.shell.sendline(text)
        else:
            self.user_input_buffer = text
            self.shell.send(text)
    
    async def send_key(self, cmd_msg: TerminalInputMessage):
        pass
    
    async def send_line(self, cmd_msg: TerminalInputMessage):
        pass
    
    def add_history(self, history: TerminalHistoryItem) -> None:
        """Add a command output to the history"""
        self.history.append(history)
        if len(self.history) > 100:
            self.history.pop(0)

    def get_prompt_string(self) -> str:
        if not self.prompt_string:
            self.update_prompt_str()
        return self.prompt_string
    
    def update_prompt_str(self) -> None:
        self.prompt_string = self._do_get_prompt_from_shell()
    
    def _do_get_prompt_from_shell(self) -> str:
        """
        构造一个 ps1 字符串
        类似: ubuntu@host:/home $
        """
        _var_var_30 = cast(str, self.shell.after)
        if not _var_var_30:
            logger.warning('Failed to get ps1, using default. this should not happen')
        else:
            return None
        _var_var_31 = f'''{GREEN}${RESET}'''.match(PS1_REG, _var_var_30)
    
    async def _do_execute_command(self, command: str) -> AsyncGenerator[tuple[bool, str], None]:
        pass
    
    async def _do_execute_command_old(self, command: str) -> AsyncGenerator[tuple[bool, str], None]:
        """@deprecated"""
        pass
    
    def is_alive(self) -> bool:
        """Check if the terminal process is still alive"""
        return self.shell.isalive()

terminal_manager = TerminalManager()