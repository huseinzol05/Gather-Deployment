from fastapi import FastAPI, Request
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
import json_logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class JSONLogWebFormatter(json_logging.JSONLogFormatter):
    def _format_log_object(self, record, request_util):
        json_log_object = super(JSONLogWebFormatter, self)._format_log_object(record, request_util)
        if 'correlation_id' not in json_log_object:
            json_log_object.update({
                'correlation_id': request_util.get_correlation_id(within_formatter=True),
            })
        if json_log_object['logger'] == 'jaeger_tracing' and 'Reporting span ' in json_log_object['msg']:
            splitted = json_log_object['msg'].split('Reporting span ')[1].split(':')[0]
            json_log_object.update({
                'trace_message': f'traceID={splitted}',
                'traceID': splitted,
            })
        return json_log_object

app = FastAPI(
    title='test-app',
    description='test-app',
    version='0.1',
)

json_logging.CREATE_CORRELATION_ID_IF_NOT_EXISTS = True
json_logging.init_fastapi(enable_json=True, custom_formatter=JSONLogWebFormatter)
json_logging.init_request_instrument(app)
logger.handlers = logging.getLogger('json_logging').handlers

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
def root(username: str, request: Request):
    random_sleep = random.random()
    logger.info(f'{username}, random generated {random_sleep}')
    time.sleep(random_sleep)
    try:
        r = requests.get(f'https://api.github.com/users/{username}')
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return {'title': 'Call external API', 'content': {'error': str(err)}}
    return {'title': 'Call external API', 'content': r.json()}