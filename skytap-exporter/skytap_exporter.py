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
        # Define regional statistics to export
        statistics = {
            'concurrent_svms':         'Concurrent SVMs',
            'concurrent_storage_size': 'Concurrent Storage Size',
            'concurrent_vms':          'Concurrent VMs',
            'cumulative_svms':         'Cumulative SVM Hours',
        }

        # Initialize metrics
        metrics = {}
        for stat_key, stat_name in statistics.items():
            stat_key_snake_case = re.sub('([A-Z])', '_\\1', stat_key).lower()
            metrics[stat_key] = GaugeMetricFamily(name=f'skytap_usage_{stat_key_snake_case}',
                                                  documentation=f'{stat_name}',
                                                  labels=["type", "region"])

        # Request usage statistics from Skytap REST API
        # TODO Handle HTTP errors gracefully
        result = json.load(urllib.request.urlopen(self._target))

        # Save metrics
        for region_name, region_data in result.items():
            for stat_key, _ in statistics.items():
                # Gracefully handle missing keys or values with `or` and `try..except`
                try:
                    data = region_data[stat_key] or {}
                except KeyError:
                    data = {}
                # Export zeros for null results
                for type_key in ["usage", "limit"]:
                    metrics[stat_key].add_metric(labels=[type_key, region_name],
                                                 value=data.get(type_key, 0.0) or 0.0)  # data.get('usage', 0.0) can be None

        # Yield metrics
        for stat_key in statistics:
            yield metrics[stat_key]


if __name__ == "__main__":
    # Parse script arguments
    arguments = docopt(__doc__)
    rest_api_endpoint = arguments['--endpoint']
    http_server_port = int(arguments['--port'])

    # Add custom collector to Prometheus registry
    REGISTRY.register(SkytapUsageCollector(rest_api_endpoint))

    # Start HTTP server to expose metrics
    start_http_server(http_server_port)

    while True:
        time.sleep(1)
