import time

import argparse
from scipy.stats import poisson, gamma
from prometheus_client import Summary, start_http_server

parser = argparse.ArgumentParser()

parser.add_argument(
    'rps',
    default=100,
    type=int,
    nargs='?',
)
parser.add_argument(
    'response_time_avg',
    default=100,
    type=int,
    nargs='?',
)
parser.add_argument(
    'prometheus_port',
    default=8000,
    type=int,
    nargs='?',
)
parser.add_argument(
    'prometheus_metric',
    default='example_app_test_metric',
    type=str,
    nargs='?',
)


def gen_distances(mu, N):
    return [1. + x for x in poisson.rvs(mu=mu, size=N)]


def gen_response_times(alpha, N):
    return gamma.rvs(a=alpha, size=N)


def send_batch(alpha, mu, send_func, batch_size=100):
    response_times = gen_response_times(alpha, batch_size)
    distances_between_requests = gen_distances(mu, batch_size)
    for distance, response_time in zip(distances_between_requests, response_times):
        # sleep for distance milliseconds before the next request
        time.sleep(distance / 1000)
        # send response time
        send_func(response_time)


def run_app():
    args = parser.parse_args()

    start_http_server(args.prometheus_port)

    summary = Summary(args.prometheus_metric, '')
    send_func = lambda value: summary.observe(value)

    rps = args.rps
    assert rps > 0, 'RPS should be > 0'

    # Mu and alpha have these formulas - more info in ipynb
    mu = 1000 / rps
    alpha = args.response_time_avg
    assert alpha > 0, 'response_time_avg should be > 0'

    while(True):
        send_batch(alpha, mu, send_func)
        

 
if __name__ == '__main__':
    run_app()
