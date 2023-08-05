import sys

try:
    from unitest import mock
except ImportError:
    import mock
import pytest
from pyramid import testing, urldispatch
from prometheus_client.core import CollectorRegistry

import pyramid_prometheus

class LoggingHandler:

    def __init__(self):
        self.requests = []

    def __call__(self, request):
        self.requests.append(request)
        return request.response

def get_samples(prometheus_registry):
    samples = {}
    for metric in prometheus_registry.collect():
        for metric_name, labels, value in metric.samples:
            labels = tuple(sorted(labels.items()))
            samples.setdefault(metric_name, {})[labels] = value
    return samples

@pytest.fixture
def handler():
    return LoggingHandler()

@pytest.fixture
def config(request):
    config = testing.setUp()
    return config

@pytest.fixture
def prometheus_registry():
    return CollectorRegistry()

@pytest.fixture
def tween_factory(config, handler, prometheus_registry):
    def f():
        return pyramid_prometheus.tween_factory(handler, config.registry, prometheus_registry=prometheus_registry)
    return f

@mock.patch('pyramid_prometheus.start_http_server')
def test_includeme(start_http_server, config):
    pyramid_prometheus.includeme(config)
    assert not start_http_server.called

@mock.patch('pyramid_prometheus.start_http_server')
def test_includeme_with_port(start_http_server, config):
    config.registry.settings['prometheus.port'] = '9105'
    pyramid_prometheus.includeme(config)
    start_http_server.assert_called_once_with(9105)

def test_tween(config, handler):
    tween = pyramid_prometheus.tween_factory(handler, config.registry)
    req = testing.DummyRequest()
    req.matched_route = None
    got_resp = tween(req)
    #from prometheus_client import REGISTRY
    #for metric in REGISTRY.collect():
    #    assert metric.samples == 0
    assert got_resp == req.response

def test_tween_with_route(tween_factory, prometheus_registry):
    tween = tween_factory()
    req = testing.DummyRequest()
    route = urldispatch.Route('index_page', '/pattern')
    req.matched_route = route
    got_resp = tween(req)
    assert got_resp == req.response
    assert get_samples(prometheus_registry)['pyramid_requests_total'] == {(('method', 'GET'), ('status', '200')): 1.0}

def test_slow_request(tween_factory, prometheus_registry):
    tween = tween_factory()
    req = testing.DummyRequest()
    req.matched_route = None
    with mock.patch('pyramid_prometheus.time') as time:
        time.side_effect = [1, 3]
        got_resp = tween(req)
    assert get_samples(prometheus_registry)['pyramid_slow_requests'] == {(('route_name', ''), ('url', 'http://example.com')): 1.0}
    assert got_resp == req.response
