import datetime
from typing import Any, List, Union

import pandas as pd
from fbprophet import Prophet

from predictive_alerting.storage import Storage, GraphiteStorage


class TaskRunner:
    def __init__(self, storage: GraphiteStorage, predictor: Prophet):
        self.storage = storage
        self.predictor = predictor

    def run_task(self, metric_name: str, need_plot: bool = False):
        current_timestamp = datetime.datetime.now()
        from_timestamp = current_timestamp - datetime.timedelta(minutes=10)
        from_ts_as_str = from_timestamp.strftime(('%H:%M_%Y%m%d'))

        current_metrics = self.storage.read_metrics(
            metric_names=[metric_name],
            from_=from_timestamp,
        )

        metric_info = current_metrics[0]

        metric_name = metric_info['target']
        metric_values = metric_info['datapoints']

        metrics_as_pddf = pd.DataFrame(
            data=[(datetime.datetime.fromtimestamp(ts), value) for value,ts in metric_values if value is not None],
            columns=['ds', 'y'],
        )

        self.predictor.fit(current_metrics)





        self.predictor = self.predictor.fit(current_metrics)

        future_timestamps = self.predictor.make_future_dataframe(
            periods=90,
            freq='S',
        )

        future_predictions = self.predictor.predict(future_timestamps)

        if need_plot:
            self.predictor.plot(future_predictions)


        return future_predictions