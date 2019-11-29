import datetime
from typing import Any, List, Union

import pandas as pd
from fbprophet import Prophet

from predictive_alerting.storage import Storage


class TaskRunner:
    def __init__(self, storage: Storage, predictor):
        self.storage = storage
        self.predictor = predictor

    def run_task(self, metric_name: str, need_plot: bool = False):
        minutes_to_get_metrics = 10
        current_timestamp = datetime.datetime.now()
        from_timestamp = current_timestamp
        from_timestamp -= datetime.timedelta(
            minutes=minutes_to_get_metrics,
        )

        metric_values = self.storage.read_metrics(
            metric_name=metric_name,
            from_timestamp=from_timestamp,
        )

        metrics_as_pddf = pd.DataFrame(
            data=[
                (datetime.datetime.fromtimestamp(ts), value) 
                for value,ts in metric_values 
                if value is not None
            ],
            columns=['ds', 'y'],
        )
        metrics_as_pddf['ds'] = pd.to_datetime(metrics_as_pddf['ds'])

        train_test_ts_bound = from_timestamp
        train_test_bs_bound += datetime.timedelta(
            minutes=int(minutes_to_get_metrics * 0.9),
        )

        df_train, df_test = (
            metrics_as_pddf[metrics_as_pddf['ds'] <= train_test_ts_bound],
            metrics_as_pddf[metrics_as_pddf['ds'] > train_test_ts_bound],
        )

        self.predictor.fit(df_train)

        future_predictions = self.predictor.predict(df_test[['ds']])

        df_test['yhat_lower'] = future_predictions['yhat_lower']
        df_test['yhat'] = future_predictions['yhat']
        df_test['yhat_upper'] = future_predictions['yhat_upper']

        bad_points = []
        for ds, y, yhat_lower, yhat, yhat_upper in df_test.values:
            if not (yhat_lower <= y <= yhat_upper):
                bad_points.append((
                    ds,
                    y,
                    yhat_lower,
                    yhat,
                    yhat_upper,
                ))

        if need_plot:
            self.predictor.plot(future_predictions)


        return metric_name, bad_points