from aiohttp import web
from functools import wraps
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
                error = await func(*args, **kwargs)
                if not error:
                    print('Successfully executed function')
                    return web.Response(text='Success', headers=AbstractHandler.cors_header)
                else:
                    print(f'Something went wrong: {error}')
                    return web.Response(status=400, text=error, headers=AbstractHandler.cors_header)
            except Exception as e:
                print(f'Exception found while executing: {e}')
                return web.Response(status=500, text=str(e), headers=AbstractHandler.cors_header)
        return wrapped

    @staticmethod
    def start_func_background(func, *args):
        """
        Executes a given 'func' in the background and returns immediately
        """
        a = tuple([a for a in args])
        thread = Thread(target=func, args=a)
        thread.daemon = True
        thread.start()

    @staticmethod
    async def validate_request(request):
        error_msg = None
        decoded_body = None

        if request.body_exists:
            value = await request.content.read()
            decoded_body = json.loads(value.decode())
            print(f'Decoded body: {decoded_body}')
        else:
            error_msg = 'Body not found in request'

        return error_msg, decoded_body
