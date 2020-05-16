from orchestrator import Orchestrator
from abstract import AbstractHandler

class Handler(AbstractHandler):
    orchest = Orchestrator()

    def __init__(self, app):
        app.add_routes(AbstractHandler.routes)

    @staticmethod
    async def validate_request(request):
        error_msg, body = await AbstractHandler.decode_request(request)
        module_name = None

        if not error_msg:
            if 'module' not in body:
                error_msg = 'Unable to find module in request'
            else:
                module_name = body['module']

        return error_msg, module_name

    @staticmethod
    @AbstractHandler.routes.post('/setup')
    @AbstractHandler.intercept_request
    async def setup_infra(request):
        error_msg, body = await AbstractHandler.decode_request(request)
        if not error_msg and 'ip' in body:
            AbstractHandler.start_func_background(
                Handler.orchest.setup_infra, (body['ip'],)
            )
        return error_msg, {}

    @staticmethod
    @AbstractHandler.routes.post('/setup_module')
    @AbstractHandler.intercept_request
    async def setup_module(request):
        error_msg, module = await Handler.validate_request(request)
        if not error_msg:
            AbstractHandler.start_func_background(
                Handler.orchest.setup_module(module)
            )
        return error_msg, {}

    @staticmethod
    @AbstractHandler.routes.post('/teardown_module')
    @AbstractHandler.intercept_request
    async def teardown_module(request):
        error_msg, module = await Handler.validate_request(request)
        if not error_msg:
            AbstractHandler.start_func_background(
                Handler.orchest.teardown_module(module)
            )
        return error_msg, {}

    @staticmethod
    @AbstractHandler.routes.get('/outputs/modules/{module}')
    @AbstractHandler.intercept_request
    async def get_output(request):
        module = request.match_info['module']
        error_msg, output = Handler.orchest.get_output(module)
        return error_msg, output

    @staticmethod
    @AbstractHandler.routes.get('/status')
    @AbstractHandler.intercept_request
    async def get_status(request):
        output = Handler.orchest.get_status()
        return None, output

    @staticmethod
    async def cleanup(app):
        Handler.orchest.cleanup()
        
