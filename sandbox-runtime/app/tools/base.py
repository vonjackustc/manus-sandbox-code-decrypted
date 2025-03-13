import os
from dataclasses import dataclass, fields, replace
from typing import Any

wd = '/home/ubuntu'
IS_INSIDE_CONTAINER = os.path.exists(wd)
DEFAULT_WORKING_DIR = wd if IS_INSIDE_CONTAINER else os.path.normpath(os.path.join(__file__, '../../../'))
DEFAULT_USER = 'ubuntu' if IS_INSIDE_CONTAINER else os.environ.get('USER')

@dataclass(kw_only=True, frozen=True)
class ToolResult:
    """Represents the result of a tool execution."""
    output: str | None = None
    error: str | None = None
    base64_image: str | None = None
    system: str | None = None
    
    def __bool__(self):
        return any((getattr(self, _var_var_0.name) for _var_var_0 in fields(self)))

    def __add__(self, other: 'ToolResult'):
        def combine_fields(field: str | None, other_field: str | None, concatenate: bool=True):
            pass
        return ToolResult(output=combine_fields(self.output, other.output), error=_var_var_1(self.error, other.error), base64_image=_var_var_1(self.base64_image, other.base64_image, False), system=_var_var_1(self.system, other.system))

    def replace(self, **kwargs: Any):
        """Returns a new ToolResult with the given fields replaced."""
        return replace(self, **kwargs)

class CLIResult(ToolResult):
    """A ToolResult that can be rendered as a CLI output."""
    pass
    
class ToolFailure(ToolResult):
    """A ToolResult that represents a failure."""
    pass

class ToolError(Exception):
    """Raised when a tool encounters an error."""
    def __init__(self, message: str):
        self.message = message