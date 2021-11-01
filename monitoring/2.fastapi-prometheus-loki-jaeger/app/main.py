from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from pythonjsonlogger import jsonlogger
from jaeger_client import Config as jaeger_config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing_instrumentation.client_hooks import install_all_patches
from starlette_opentracing import StarletteTracingMiddleWare
from starlette_exporter import PrometheusMiddleware, handle_metrics
from datetime import datetime
import logging
import random
import requests
import time

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
gunicorn_error_logger = logging.getLogger('gunicorn.error')
uvicorn_access_logger = logging.getLogger('uvicorn.access')
uvicorn_logger = logging.getLogger('uvicorn')
uvicorn_error_logger = logging.getLogger('uvicorn.error')
logHandler = logging.StreamHandler()
formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.handlers = [logHandler]
gunicorn_error_logger.handlers = logger.handlers
uvicorn_access_logger.handlers = logger.handlers
fastapi_logger.handlers = logger.handlers
uvicorn_error_logger.handlers = logger.handlers

app = FastAPI(
    title='test-app',
    description='test-app',
    version='0.1',
)

opentracing_config = jaeger_config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
        'local_agent': {'reporting_host': 'jaeger'},
    },
    scope_manager=ContextVarsScopeManager(),
    service_name='tracer',
)
jaeger_tracer = opentracing_config.initialize_tracer()
install_all_patches()
app.add_middleware(StarletteTracingMiddleWare, tracer=jaeger_tracer)

app.add_middleware(PrometheusMiddleware)
app.add_route('/metrics', handle_metrics)

@app.get('/')
def root(username: str):
    random_sleep = random.random()
    logger.info(f'{username}, random generated {random_sleep}')
    time.sleep(random_sleep)
    try:
        r = requests.get(f'https://api.github.com/users/{username}')
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'title': 'Call external API', 'content': {'error': str(err)}}
    return {'title': 'Call external API', 'content': r.json()}