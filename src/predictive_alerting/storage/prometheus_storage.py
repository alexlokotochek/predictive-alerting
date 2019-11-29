from predictive_alerting.storage import Storage
from typing import Any, Dict, List, Optional

import requests
import datetime


class PrometheusStorage(Storage):
    def _generate_prometheus_url(
            self,
            *,
            prometheus_host: str,
            prometheus_port: str,
            metric_name: str,
            from_timestamp: datetime.datetime = None,
            until_: Optional[int] = None,
            step: Optional[int] = 5,
    ) -> str:
        start = from_timestamp.timestamp()
        end = datetime.datetime.now().timestamp()
        prometheus_render_url = (
            f'http://{prometheus_host}:{prometheus_port}/api/v1/query_range'
            f'?query=rate({metric_name}_sum[1m])/rate({metric_name}_count[1m])'
            f'&start={start}&end={end}&step={step}'
        )
        return prometheus_render_url

    def read_metric(
            self,
            *,
            metric_name: str,
            from_timestamp: Optional[datetime.datetime] = None,
            until_: Optional[int] = None,
            format_: str = None,
    ) -> Dict[str, Any]:
        prometheus_host = self.connection_params['PROMETHEUS_HOST']
        prometheus_port = self.connection_params['PROMETHEUS_PORT']

        prometheus_render_url = self._generate_prometheus_url(
            prometheus_host=prometheus_host,
            prometheus_port=prometheus_port,
            metric_name=metric_name,
            from_timestamp=from_timestamp,
            until_=until_,
        )

        metric_response = requests.get(
            url=prometheus_render_url
        )
        metric_response = metric_response.json()
        values = [
            (float(v[1]), v[0]) 
            for v in metric_response['data']['result'][0]['values']
        ]

        return values
