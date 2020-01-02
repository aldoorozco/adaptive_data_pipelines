from abstract import AbstractHandler
from airflow_job import Job

class Handler(AbstractHandler):
    job = Job()
    def __init__(self, app):
        app.add_routes(AbstractHandler.routes)

    @staticmethod
    async def validate_request(request):
        error_msg, decoded_body = await AbstractHandler.validate_request(request)
        job_info = None

        if not error_msg:
            if 'job_info' not in decoded_body:
                error_msg = 'Unable to find job_info in request'
            else:
                job_info = decoded_body['job_info']

        return error_msg, job_info

    @staticmethod
    @AbstractHandler.routes.post('/create_pipeline')
    @AbstractHandler.intercept_request
    async def create_pipeline(request):
        error_msg, job_info = await Handler.validate_request(request)
        if not error_msg:
            Handler.start_func_background(Handler.job.run, job_info)
        return error_msg
