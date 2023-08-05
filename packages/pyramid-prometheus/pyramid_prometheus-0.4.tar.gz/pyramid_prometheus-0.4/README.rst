Pyramid Integration for Prometheus
==================================

A tween which exposes basic Pyramid statistics to Prometheus.

Setup
-----

You can either include the exporter in your project's ``__init__.py``::

    config = Configurator(.....)
    config.include('pyramid_prometheus')

Or you can use the pyramid.includes configuration value in your ``.ini``
file::

    [app:myapp]
    pyramid.includes = pyramid_exclog

Settings
--------

:``prometheus.port``:
    port number to expose metrics on. If not set, metrics
    are not exposed

:``prometheus.slow_request_threshold``:
    Number of seconds as a float.
    If a request takes longer than this, it is logged in the metric
    ``pyramid_slow_requests``
