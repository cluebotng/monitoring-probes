# ClueBot Monitoring Probes

Prometheus metric exporter which runs checks specific to ClueBot {III, NG} components.

## Testing locally

```
$ fastapi dev monitoring_probes/api.py 
```

## Build locally

```
$ pack build --builder heroku/builder:24 monitoring-probes
```

## Production configuration

Expected secrets:

* `TOOL_REPLICA_USER` - username to access `enwiki.p`
* `TOOL_REPLICA_PASSWORD` - password to access `enwiki.p`
