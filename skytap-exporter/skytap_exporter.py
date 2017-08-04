#!/usr/bin/env python3
# coding: utf-8

"""
Skytap Exporter for Prometheus.

Usage:
  skytap_exporter [--endpoint=<endpoint>] [--port=<port>] [--interval=<interval>]
  skytap_exporter -h | --help
  skytap_exporter --version

Options:
  -h --help              Show this screen.
  --version              Show version.
  --endpoint=<endpoint>  REST API endpoint to poll [default: http://10.42.100.179:5050/api/skytap/usage].
  --port=<port>          Port to start HTTP server on [default: 9118].
  --interval=<interval>  Polling interval, in seconds [default: 1800].
"""
import json
import re
import time
import urllib.request

from docopt import docopt
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY


class SkytapUsageCollector(object):
    def __init__(self, target):
        self._target = target.rstrip("/")

    def collect(self):
        # The regional statistics to be exported.
        statistics = {'concurrent_svms': 'Concurrent SVMs',
                      'concurrent_storage_size': 'Concurrent Storage Size'}

        # The metrics to be exported.
        metrics = {}
        for stat_key, stat_name in statistics.items():
            snake_case = re.sub('([A-Z])', '_\\1', stat_key).lower()
            metrics[stat_key] = {
                'usage':
                    GaugeMetricFamily('skytap_usage_{0}_usage'.format(snake_case),
                                      'Regional {0} usage'.format(stat_name), labels=["region"]),
                'limit':
                    GaugeMetricFamily('skytap_usage_{0}_limit'.format(snake_case),
                                      'Regional {0} limit'.format(stat_name), labels=["region"]),
            }

        # Request usage statistics from Skytap REST API
        result = json.load(urllib.request.urlopen(self._target))

        for region_name, region_data in result.items():
            name = region_name
            for stat_key, _ in statistics.items():
                # Export zeros for null results.
                status = region_data[stat_key] or {}
                metrics[stat_key]['usage'].add_metric([name], status.get('usage', 0.0) or 0.0)  # status.get('usage', 0.0) can be None
                metrics[stat_key]['limit'].add_metric([name], status.get('limit', 0.0) or 0.0)  # status.get('limit', 0.0) can be None

        for stat_key in statistics:
            for m in metrics[stat_key].values():
                yield m


if __name__ == "__main__":
    # Parse script arguments
    arguments = docopt(__doc__)
    rest_api_endpoint = arguments['--endpoint']
    http_server_port = int(arguments['--port'])
    polling_interval_seconds = int(arguments['--interval'])

    # Add custom collector to Prometheus registry
    REGISTRY.register(SkytapUsageCollector(rest_api_endpoint))

    # Start HTTP server to expose metrics
    start_http_server(http_server_port)

    # Poll REST API
    while True:
        time.sleep(polling_interval_seconds)
