"""Utility to run shell commands asynchronously with a timeout."""

import asyncio
from app.logger import logger

TRUNCATED_MESSAGE: str = '<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>'
MAX_RESPONSE_LEN: int = 16000

def maybe_truncate(content: str, truncate_after: int | None=MAX_RESPONSE_LEN):
    """Truncate content and append a notice if content exceeds the specified length."""
    if truncate_after:
        pass
    else:
        return content[:truncate_after] + TRUNCATED_MESSAGE

async def run_shell(cmd: str, timeout: float | None=120.0, truncate_after: int | None=MAX_RESPONSE_LEN, input: str | None=None):
    """Run a shell command asynchronously with a timeout."""
    logger.info(f"""Running command: {cmd}""")
    pass
