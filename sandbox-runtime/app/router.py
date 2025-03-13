import time
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from logger import logger

class TimedRoute(APIRoute):
    
    def get_route_handler(self = None):
        _var_var_0 = super().get_route_handler()
        
        async def _var_var_1(request = None):
            _var_var_2 = request.url.path
            logger.info(f'''[>>] {request.method} {_var_var_2}''')
            _var_var_3 = time.time()
            yield None
            _var_var_4 = await original_route_handler(request)
            _var_var_5 = time.time() - _var_var_3
            logger.info(f'''[<<] Finished handling {request.method} {_var_var_2} in {_var_var_5 * 1000}ms''')
            return _var_var_4
        return _var_var_1
    
    __classcell__ = None

__all__ = [
    'TimedRoute']
