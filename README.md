# Skytap dashboard, powered by Grafana and Prometheus

## Usage

```bash
git clone https://github.com/lvaylet/grafana-prometheus-skytap.git
cd grafana-prometheus-skytap
docker-compose up  # to display the logs in the console
docker-compose up -d  # to run the container as a daemon
```

Log in to `http://localhost:3000` as `admin/pass`, then start adding data sources and dashboards.
Go to `http://localhost:9090` to access Prometheus and display the metrics.

## References

- [Monitoring with Prometheus, Grafana & Docker](https://finestructure.co/blog/2016/5/16/monitoring-with-prometheus-grafana-docker-part-1)
- [Writing JSON Exporters in Python](https://www.robustperception.io/writing-json-exporters-in-python/)
- [Writing a Jenkins exporter in Python](https://www.robustperception.io/writing-a-jenkins-exporter-in-python/)
- [kawamuray/prometheus-json-exporter](https://github.com/kawamuray/prometheus-json-exporter)
- [lovoo/jenkins_exporter](https://github.com/lovoo/jenkins_exporter)
- [Metric and Label Naming](https://prometheus.io/docs/practices/naming/)
