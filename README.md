# Skytap Dashboard

> powered by [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/) and [Docker](https://www.docker.com/)

## Usage

```bash
git clone https://github.com/lvaylet/grafana-prometheus-skytap.git
cd grafana-prometheus-skytap
docker-compose up  # to display the logs in the console
docker-compose up -d  # to run the container as a daemon
docker-compose logs -f  [<service>]  # to display logs
docker-compose stop  # to stop the containers
docker-compose rm  # to remove the containers
```

Log in to `http://localhost:3000` as `admin/pass`, then start adding data sources and dashboards.

Go to `http://localhost:9090` to access Prometheus and display the metrics.

Reload Prometheus configuration with `curl -X POST http://localhost:9090/-/reload` when config files are updated ([source](https://www.robustperception.io/reloading-prometheus-configuration/)).

Use `docker-compose up -d --no-deps --build <service_name>` to replace an existing container without tearing down the entire suite of containers ([source](http://staxmanade.com/2016/09/how-to-update-a-single-running-docker-compose-container/)).

## References

- [Monitoring with Prometheus, Grafana & Docker](https://finestructure.co/blog/2016/5/16/monitoring-with-prometheus-grafana-docker-part-1)
- [Writing JSON Exporters in Python](https://www.robustperception.io/writing-json-exporters-in-python/)
- [Writing a Jenkins exporter in Python](https://www.robustperception.io/writing-a-jenkins-exporter-in-python/)
- [RobustPerception/python_examples](https://github.com/RobustPerception/python_examples/blob/master/jenkins_exporter/jenkins_exporter.py)
- [kawamuray/prometheus-json-exporter](https://github.com/kawamuray/prometheus-json-exporter)
- [lovoo/jenkins_exporter](https://github.com/lovoo/jenkins_exporter)
- [Metric and Label Naming](https://prometheus.io/docs/practices/naming/)
