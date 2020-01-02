from abstract import AbstractHandler
from dag_handler import DagHandler

class Handler(AbstractHandler):
    dag = DagHandler()
    def __init__(self, app):
        app.add_routes(AbstractHandler.routes)

    @staticmethod
    async def validate_request(request):
        error_msg, decoded_body = await AbstractHandler.validate_request(request)

        return error_msg, decoded_body

    @staticmethod
    @AbstractHandler.routes.post('/create_dag')
    @AbstractHandler.intercept_request
    async def create_pipeline(request):
        error_msg, job_info = await Handler.validate_request(request)
        if not error_msg:
            AbstractHandler.start_func_background(Handler.dag.run, job_info)
        return error_msg
