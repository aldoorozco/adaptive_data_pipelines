from aiohttp import web
import os
from handler import Handler 
import logging

if __name__ == '__main__':
    app = web.Application()
    # Handler automatically registers its internal routes to the app
    handler = Handler(app)
    app.on_cleanup.append(Handler.cleanup)
    logging.basicConfig(level=logging.WARN)
    web.run_app(app, host='0.0.0.0', port=os.getenv('SERVICE_PORT', 5000))
