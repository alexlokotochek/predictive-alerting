Setup prometheus to scrap example-app metrics (default port 8000)

If you're running docker not on mac - please replace `docker.for.mac.localhost` with `localhost` in prometheus.yml
Replace path-to with current dir pwd

```
docker run \
    -p 9090:9090 \
    -v <path-to>/prometheus.yml:/etc/prometheus/prometheus.yml \
    -it \
    prom/prometheus
```
Dashboard is accessible via http://localhost:9090

![Dashboard](https://github.com/alexlokotochek/predictive-alerting/blob/master/integrations/prometheus/example.png)


Metric example: rate(example_app_test_metric_sum[1m])/rate(example_app_test_metric_count[1m])