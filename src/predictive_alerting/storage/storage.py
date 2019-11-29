from typing import Any, Dict, List, Optional

import requests


class Storage:
    def __init__(self, *, connection_params: Dict[str, Any]):
        self.connection_params = connection_params

    def read_metrics(self, *, metric_names: List[str]) -> Dict[str, Any]:
        raise NotImplementedError()


class GraphiteStorage(Storage):
    def _generate_graphite_render_url(
            self,
            *,
            graphite_host: str,
            graphite_port: str,
            metric_names: List[str],
            from_: Optional[str] = None,
            until_: Optional[str] = None,
            format_: str = 'json',
    ) -> str:
        # TODO: ADD maxDataPoints, noNullPoints

        targets = '&target='.join(metric_names)
        graphite_render_url = f'http://{graphite_host}:{graphite_port}/render/?target={targets}&format={format_}'

        if from_ is not None:
            graphite_render_url += f'&from={from_}'
        if until_ is not None:
            graphite_render_url += f'&until={until_}'

        return graphite_render_url

    def read_metrics(
            self,
            *,
            metric_names: List[str],
            from_: Optional[str] = None,
            until_: Optional[str] = None,
            format_: str = 'json',
    ) -> Dict[str, Any]:
        graphite_host = self.connection_params['GRAPHITE_HOST']
        graphite_port = self.connection_params['GRAPHITE_PORT']

        graphite_render_url = self._generate_graphite_render_url(
            graphite_host=graphite_host,
            graphite_port=graphite_port,
            metric_names=metric_names,
            from_=from_,
            until_=until_,
            format_=format_
        )

        metrics_response = requests.get(
            url=graphite_render_url
        )
        metrics = metrics_response.json()

        return metrics