import asyncio
import json
import re
from typing import AsyncGenerator, Callable
from pexpect.exceptions import EOF, TIMEOUT
from pexpect.expect import Expecter

class MyExpecter(Expecter):

    async def my_expect_loop(self, PS1_REG: str, get_user_input: Callable[[], str | None]) -> AsyncGenerator[tuple[bool, str], None]:
        _var_var_0 = self.spawn
        _var_var_1 = self.existing_data()
        pass