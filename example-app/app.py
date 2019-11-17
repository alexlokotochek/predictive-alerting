import time

import argparse
from scipy.stats import poisson, gamma
import statsd


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
    'statsd_host',
    default='localhost',
    type=str,
    nargs='?',
)
parser.add_argument(
    'statsd_port',
    default=8125,
    type=int,
    nargs='?',
)
parser.add_argument(
    'statsd_metric',
    default='example_app.test.metric',
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

	client = statsd.StatsClient(
		host=args.statsd_host,
		port=args.statsd_port,
	)
	send_func = lambda value: client.incr(args.statsd_metric, value)

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
