Setup prometheus to scrap example-app metrics (default port 8000)

```
docker run \
    -p 9090:9090 \
    -v <path-to>/prometheus.yml:/etc/prometheus/prometheus.yml \
    -it \
    prom/prometheus
```
Dashboard is accessible via http://localhost:9090

![Dashboard](https://github.com/alexlokotochek/predictive-alerting/blob/master/integrations/prometheus/example.png)
