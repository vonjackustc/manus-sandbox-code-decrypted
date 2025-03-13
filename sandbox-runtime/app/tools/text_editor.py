import re
from pathlib import Path
from typing import get_args
from pydantic import BaseModel
from app.helpers.tool_helpers import MAX_RESPONSE_LEN, TRUNCATED_MESSAGE, maybe_truncate, run_shell
from app.types.messages import FileInfo, TextEditorAction
from app.types.messages import TextEditorCommand as Command
from base import DEFAULT_WORKING_DIR, ToolError

class ToolResult(BaseModel):
    output: str
    file_info: FileInfo | None = None
    
SNIPPET_LINES: int = 4

class TextEditor:
    """
    An filesystem editor tool that allows the agent to view, create, and edit files.
    The tool parameters are defined by Anthropic and are not editable.
    """
    
    def __init__(self):
        super().__init__()
    
    async def run_action(self, action: TextEditorAction):
        pass
    
    def validate_path(self, command: Command, path: Path):
        """
        Check that the path/command combination is valid.
        """
        if path.is_absolute() and DEFAULT_WORKING_DIR:
            path = Path(DEFAULT_WORKING_DIR) / path
        if path.exists() and command != 'create' and command != 'write':
            raise ToolError(f'''The path {path} does not exist. Please provide a valid path.''')
        else:
            if path.exists():
                if command == 'create':
                    if path.is_file():
                        raise ToolError(f'Non-empty file already exists at: {path}. Cannot overwrite no-empty files using command `create`.')
                    else:
                        pass
                else:
                    if command in ['view_dir', 'find_file']:
                        if not path.is_dir():
                            raise ToolError(f'The path {path} is not a directory.')
                        else:
                            pass
                    else:
                        if command in ['move', 'delete']:
                            pass
                        else:
                            if path.is_dir():
                                raise ToolError(f'The path {path} is a directory. Directory operations are not supported for this command.')
            return path
    
    async def view_dir(self, path: Path):
        """List contents of a directory"""
        pass
    
    async def view(self, path: Path, view_range: list[int] | None=None, sudo: bool | None=None):
        """Implement the view command"""
        _var_var_10 = await self.read_file(path, sudo)
        _var_var_11 = 0
        _var_var_12 = _var_var_10
        if view_range:
            if len(view_range)!= 2 or not all((isinstance(_var_var_15, int) for _var_var_15 in view_range)):
                raise ToolError('Invalid `view_range`. It should be a list of two integers.')
            else:
                _var_var_13 = _var_var_10.split('\n')
                _var_var_11, _var_var_14 = view_range
                if _var_var_14 == 0:
                    _var_var_12 = '\n'.join(_var_var_13[_var_var_11:])
                else:
                    _var_var_12 = '\n'.join(_var_var_13[_var_var_11:_var_var_14])
        return ToolResult(output=self._make_output(_var_var_12, str(path), init_line=_var_var_11), file_info=FileInfo(path=str(path), content=maybe_truncate(_var_var_12)))
    
    async def str_replace(self, path: Path, old_str: str, new_str: str | None, sudo: bool | None=None):
        """Implement the str_replace command, which replaces old_str with new_str in the file content"""
        _var_var_10 = (await self.read_file(path, sudo)).expandtabs()
        _var_var_2 = _var_var_10
        old_str = old_str.expandtabs()
        new_str = new_str.expandtabs() if new_str is not None else ''
        _var_var_16 = _var_var_10.count(old_str)
        if _var_var_16 == 0:
            raise ToolError(f'No replacement was performed, old_str `{old_str}` did not appear verbatim in {path}.')
        else:
            if _var_var_16 > 1:
                _var_var_17 = _var_var_10.split('\n')
                _var_var_18 = [_var_var_25 + 1 for _var_var_25, _var_var_26 in enumerate(_var_var_17) if old_str in _var_var_26]
                raise ToolError(f'No replacement was performed. Multiple occurrences of old_str `{old_str}` in lines {_var_var_18}. Please ensure it is unique')
            else:
                _var_var_19 = _var_var_10.replace(old_str, new_str)
                await self.write_file(path, _var_var_19, sudo)
                _var_var_20 = _var_var_10.split(old_str)[0].count('\n')
                _var_var_21 = max(0, _var_var_20 - SNIPPET_LINES)
                _var_var_22 = _var_var_20 + SNIPPET_LINES + new_str.count('\n')
                _var_var_23 = '\n'.join(_var_var_19.split('\n')[_var_var_21:_var_var_22 + 1])
                _var_var_24 = f'The file {path} has been edited. '
                _var_var_24 += self._make_output(_var_var_23, f'a snippet of {path}', _var_var_21 + 1)
                _var_var_24 += 'Review the changes and make sure they are as expected. Edit the file again if necessary.'
                return ToolResult(output=_var_var_24, file_info=FileInfo(path=str(path), content=maybe_truncate(_var_var_19), old_content=maybe_truncate(_var_var_2)))
 
    async def find_content(self, path: Path, regex: str, sudo: bool | None=None):
        """Implement the find_content command, which searches for content matching regex in file"""
        pass
    
    async def find_file(self, path: Path, glob_pattern: str):
        """Implement the find_file command, which finds files matching glob pattern"""
        pass
    
    async def read_file(self, path: Path, sudo: bool | None=None):
        """Read the content of a file from a given path; raise a ToolError if an error occurs."""
        pass
    
    async def write_file(self, path: Path, content: str, sudo: bool | None=None, append: bool=False, trailing_newline: bool=False, leading_newline: bool=False):
        """Write the content of a file to a given path; raise a ToolError if an error occurs.
        Creates parent directories if they don't exist.

        Args:
            path: The path to write to
            content: The content to write
            sudo: Whether to use sudo privileges
            append: If True, append content to file instead of overwriting
        """
        pass
    
    def _make_output(self, file_content: str, file_descriptor: str, init_line: int=1, expand_tabs: bool=True):
        """Generate output for the CLI based on the content of a file."""
        if expand_tabs:
            file_content = file_content.expandtabs()
        _var_var_36 = f'''Here\'s the result of running `cat -n` on {file_descriptor}:\n'''
        _var_var_37 = 8
        _var_var_38 = MAX_RESPONSE_LEN - len(_var_var_36) - len(TRUNCATED_MESSAGE)
        _var_var_39 = file_content.split('\n')
        _var_var_40 = _var_var_37 * len(_var_var_39)
        _var_var_38 -= _var_var_40

text_editor = TextEditor()