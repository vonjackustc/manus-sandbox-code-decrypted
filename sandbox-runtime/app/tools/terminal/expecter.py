import asyncio
import json
import re
from typing import AsyncGenerator, Callable
from pexpect.exceptions import EOF, TIMEOUT
from pexpect.expect import Expecter

class MyExpecter(Expecter):

    def my_expect_loop(self = None, PS1_REG = None, get_user_input = None):
        _var_var_0 = self.spawn
        _var_var_1 = self.existing_data()