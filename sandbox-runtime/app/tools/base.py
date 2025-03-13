import os
from dataclasses import dataclass, fields, replace
from typing import Any

wd = '/home/ubuntu'
IS_INSIDE_CONTAINER = os.path.exists(wd)
DEFAULT_WORKING_DIR = wd if IS_INSIDE_CONTAINER else os.path.normpath(os.path.join(__file__, '../../../'))
DEFAULT_USER = 'ubuntu' if IS_INSIDE_CONTAINER else os.environ.get('USER')
ToolResult = None

class CLIResult(ToolResult):
    '''A ToolResult that can be rendered as a CLI output.'''
    pass


class ToolFailure(ToolResult):
    '''A ToolResult that represents a failure.'''
    pass


class ToolError(Exception):
    '''Raised when a tool encounters an error.'''
    
    def __init__(self, message):
        self.message = message