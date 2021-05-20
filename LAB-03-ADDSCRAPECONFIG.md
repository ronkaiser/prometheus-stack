# Lab 03: Add a scrape configuration for prometheus

Now that our node_exporter is up and running let's configure prometheus to get it metrics by update the prometheus configuration

## Summary

 - Create a targets file
 - Configure Prometheus to scrape the targets file
 - Restart prometheus to apply the new configuration
 - Check that Prometheus is tracking your server

## Create a targets file

- Let's create a new file under the prometheus directory

```
nano ~/monitoring-lab/prometheus/targets.yml
```

- Add the content below to the file

```
- targets: ['nodeexporter:9100']
  labels:
    name: 'My Server'
```

- Note that we configure a target that track the node_exporter accessible at "nodeexporter:9100" and we add to it the label "name = My Server" (you can add multiple targets/labels)

## Configure Prometheus to scrape the targets file

- Now we need to edit our "prometheus.yml" to add our target file to the scrape configuration

```
nano ~/monitoring-lab/prometheus/prometheus.yml
```

- The content of the "prometheus.yml" file should be the below:

```
# Global configuration
global:
  # How frequently to scrape targets by default.
  scrape_interval:     15s
  # How long until a scrape request times out.
  scrape_timeout: 10s
  # How frequently to evaluate rules.
  evaluation_interval: 15s 
    
# A list of scrape configurations.
scrape_configs:
  # The job name assigned to scraped metrics by default.
  - job_name: 'prometheus'
    # List of labeled statically configured targets for this job.
    static_configs:
    # The targets specified by the static config.
    - targets: ['localhost:9090']

  - job_name: 'My Targets'
    file_sd_configs:
      - files:
         - targets.yml
```

## Restart Prometheus to apply the new configuration

- Use docker-compose to restart the prometheus container and apply the new configuration

```
docker-compose restart prometheus
```

## Check that Prometheus is tracking your server

- Let's check that the new server it's being tracked by browse to

```
http://localhost:9090/targets
```

<kbd>
  <img src="/images/scrape-01.png" width="600">
</kbd><br/><br/>
