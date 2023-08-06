from time import time

from prometheus_client import start_http_server, Histogram, Counter, REGISTRY
from pyramid.tweens import EXCVIEW

_pyramid_request_latency = Histogram('pyramid_request_latency', 'Latency of requests', ['route'])
_pyramid_request_total = Counter('pyramid_requests_total', 'HTTP Requests', ['method', 'status'])
_pyramid_slow_requests = Counter('pyramid_slow_requests', 'HTTP Requests', ['route_name', 'url'])

def tween_factory(handler, registry):
    settings = registry.settings
    slow_request_threshold = float(settings.get('prometheus.slow_request_threshold', '1'))
    ignore_initial_request_count = int(settings.get('prometheus.ignore_initial_request_count', '10'))
    request_count = []

    def tween(request):
        start = time()
        status = '500'
        try:
            response = handler(request)
            status = str(response.status_int)
            return response
        finally:
            if len(request_count) < ignore_initial_request_count:
                # sigh, really want to use nonlocal and python 3 here
                request_count.append(None)
            else:
                duration = time() - start
                if request.matched_route is None:
                    route_name = ''
                else:
                    route_name = request.matched_route.name
                _pyramid_request_latency.labels(route_name).observe(duration)
                _pyramid_request_total.labels(request.method, status).inc()
                if duration > slow_request_threshold:
                    _pyramid_slow_requests.labels(route_name, request.url).inc()
    return tween


def includeme(config):
    settings = config.registry.settings
    port = settings.get('prometheus.port', None)
    if port:
        # if you don't specify port, you have to expose the metrics yourself somehow
        start_http_server(int(port))
    config.add_tween('pyramid_prometheus.tween_factory', over=EXCVIEW)
