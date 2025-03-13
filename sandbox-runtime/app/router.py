import time
from typing import Callable
from fastapi import Request, Response
from fastapi.routing import APIRoute
from .logger import logger

class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            _var_var_2 = request.url.path
            logger.info(f'[>>] {request.method} {_var_var_2}')
            _var_var_3 = time.time()
            _var_var_4 = await original_route_handler(request)
            _var_var_5 = time.time() - _var_var_3
            logger.info(f'[<<] Finished handling {request.method} {_var_var_2} in {_var_var_5 * 1000}ms')
            return _var_var_4
        
        return custom_route_handler

__all__ = ['TimedRoute']