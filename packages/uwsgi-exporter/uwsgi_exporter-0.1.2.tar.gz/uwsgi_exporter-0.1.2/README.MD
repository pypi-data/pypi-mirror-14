# UWSGI_EXPORTER
Prometheus uwsgi stats exporter allows you to export metrics from uwsgi [stats server](http://uwsgi-docs.readthedocs.io/en/latest/StatsServer.html) to [Prometheus](https://prometheus.io/).

## Configuration
You must configure uwsgi stats server to return stats using HTTP.

## Usage
`uwsgi_exporter.py --stats_addr <uwsgi_stats_server_addr> --bind_address <uwsgi_exporter_listen_addr> --bind_port <uwsgi_exporter_listen_port>`

`stats_addr` can be unix or tcp socket. `bind_address` and `bind_port` has default values (`127.1` and `1717` respectively) and not required. 

## Example
`uwsgi_exporter.py --stats_addr /path/to/uwsgi_stats.sock --bind_address 127.1 --bind_port 1717`
