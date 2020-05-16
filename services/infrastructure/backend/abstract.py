from aiohttp import web
from functools import wraps
from orchestrator import Orchestrator
from threading import Thread
from multidict import MultiDict
import sys
import json

class AbstractHandler:
    routes = web.RouteTableDef()

    cors_header = MultiDict({'Access-Control-Allow-Origin': 'http://localhost:8080'})

    def __init__(self):
        pass

    @staticmethod
    def intercept_request(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                error, body = await func(*args, **kwargs)
                if not error:
                    return web.json_response(body, headers=AbstractHandler.cors_header)
                else:
                    return web.Response(status=400, text=error, headers=AbstractHandler.cors_header)
            except Exception as e:
                print(f'Exception found while executing: {e}')
                return web.Response(status=500, text=e, headers=AbstractHandler.cors_header)
        return wrapped

    @staticmethod
    def start_func_background(func):
        """
        Executes a given 'func' in the background and returns immediately
        """
        thread = Thread(target=func, args=())
        thread.daemon = True
        thread.start()

    @staticmethod
    async def decode_request(request):
        error_msg = None
        decoded_body = None

        if request.body_exists:
            value = await request.content.read()
            decoded_body = json.loads(value.decode())
            print(f'Decoded body: {decoded_body}')
        else:
            error_msg = 'Body not found in request'

        return error_msg, decoded_body
