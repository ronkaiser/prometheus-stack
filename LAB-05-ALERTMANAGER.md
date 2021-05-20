# Lab 05: Deploy and Configure Alertmanager

## Note

In this section we will configure alertmanager to send emails, however you don't need a valid smtp server if you are looking for a "proof of concept" only (if you configure alertmanager with wrong smtp details everything will work the same but the email will not be sent)

## Summary

 - Configure your workspace
 - Create the Alertmanager configuration file
 - Configure Prometheus to work with Alertmanager
 - Configure some alerting rules
 - Deploy Alertmanager using Docker Compose
 - Restart Prometheus to apply the new configuration
 - Explore Alertmanager

## Configure your workspace

- Create a dedicated folder for your alertmanager files

```
mkdir ~/monitoring-lab/alertmanager
```

## Create the Alertmanager configuration file

- Let's create a basic configuration file for Alertmanager 

```
nano ~/monitoring-lab/alertmanager/alertmanager.yml
```

- The content of the file should be the below (set the smtp configuration if you want alertmanager to send emails, for this demo is not required due we just want to test the trigger)

```
# Global Configuration
global:
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'email@mail.com'
  smtp_auth_username: 'email@mail.com'
  smtp_auth_identity: 'email@mail.com'
  smtp_auth_password: 'password'
  smtp_require_tls: true

# The root node of the routing tree.
route:
  group_by: ['severity']
  # When a new group of alerts is created by an incoming alert, wait at least 'group_wait' to send the initial notification
  group_wait: 30s
  # When the first notification was sent, wait 'group_interval' to send a batch of new alerts
  group_interval: 1m
  # If an alert has successfully been sent, wait 'repeat_interval' to resend them
  repeat_interval: 6h
  # Default receivers
  receiver: 'email'

# Inhibition rules allow to mute a set of alerts given that another alert is firing.
inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'

# Receivers details (email, slack, integrations configs, etc)
receivers:
  - name: 'email'
    email_configs:
    - to: 'email@mail.com'
```


## Configure Prometheus to work with Alertmanager

- Update the Prometheus configuration file to connect it with Alertmanager

```
nano ~/monitoring-lab/prometheus/prometheus.yml
```

- Let's add the following section under the global configuration

```
# Alertmanager configuration
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: ['alertmanager:9093']
```

- Your prometheus.yml should have the content below

```
# Global configuration
global:
  # How frequently to scrape targets by default.
  scrape_interval:     15s
  # How long until a scrape request times out.
  scrape_timeout: 10s
  # How frequently to evaluate rules.
  evaluation_interval: 15s 

# Alertmanager configuration
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: ['alertmanager:9093']

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

## Configure some alerting rules

- Let's create an alerts file to define the following 3 rules:
  - The server has been down for more than 5 minutes
  - The server has been using more than 85% of his memory RAM in the last 5 minutes
  - The server has been using more than 85% of his cpu in the last 5 minutes

```
nano ~/monitoring-lab/prometheus/alerts.yml
```

- The content of the file should be the below:

```
groups:
  - name: critical-alerts
    rules:
    - alert: 'Instance Down'
      expr: up == 0
      for: 1m
      labels:
        severity: critical
      annotations:
        summary: "[ {{ $labels.name }} ] is down"
        description: "[ {{ $labels.name }} ] has been down for more than 1 minute"
  - name: usage-alerts
    rules:
    - alert: 'RAM Usage'
      expr: 100 - ((node_memory_MemAvailable_bytes * 100) / node_memory_MemTotal_bytes) > 15
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Server {{ $labels.instance }} reach the RAM memory limit"
        description: "Server {{ $labels.instance }} has been using more than 85% of his memory RAM in the last 5 minutes"
    - alert: 'Disk Usage'
      expr: max(((node_filesystem_size_bytes{fstype=~"ext4|vfat"} - node_filesystem_free_bytes{fstype=~"ext4|vfat"}) / node_filesystem_size_bytes{fstype=~"ext4|vfat"}) * 100) by (name) > 20
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Server {{ $labels.instance }} reach the disk usage limit"
        description: "Server {{ $labels.instance }} has been using more than 85% of his disk space in the last 5 minutes"
    - alert: 'CPU Usage'
      expr: (1 - avg(irate(node_cpu_seconds_total{mode="idle"}[10m])) by (name)) * 100 > 5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Server {{ $labels.instance }} reach the cpu usage limit"
        description: "Server {{ $labels.instance }} has been using more than 85% of his cpu in the last 5 minutes"
```

- Update the Prometheus configuration file to use the created rules

```
nano ~/monitoring-lab/prometheus/prometheus.yml
```

- Let's add the following section under the alertmanager configuration

```
# Alerts rules
rule_files:
  - 'alerts.yml'
```

- Your prometheus.yml should have the content below

```
# Global configuration
global:
  # How frequently to scrape targets by default.
  scrape_interval:     15s
  # How long until a scrape request times out.
  scrape_timeout: 10s
  # How frequently to evaluate rules.
  evaluation_interval: 15s 

# Alertmanager configuration
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets: ['alertmanager:9093']

# Alerts rules
rule_files:
  - 'alerts.yml'

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

## Deploy Alertmanager using Docker Compose

- Let's add an Alertmanager container to our docker compose file

```
nano ~/monitoring-lab/docker-compose.yml
```

- Add the alertmanager service (note that it includes a volume named "alertmanager_data"):

```
  alertmanager:
    image: "prom/alertmanager:v0.21.0"
    container_name: alertmanager
    restart: unless-stopped
    mem_limit: 4G
    ports:
     - "9093:9093"
    command:
     - "--config.file=/etc/alertmanager/alertmanager.yml"
     - "--storage.path=/alertmanager"
    volumes:
     - "./alertmanager/:/etc/alertmanager/"
     - "alertmanager_data:/alertmanager"
    networks:
     - "monitoring"
```
- And add the alertmanager volume to the volumes sections at the end of the file:
```
volumes:
  prometheus_data:
  grafana_data:
  alertmanager_data:
```
- Deploy alertmanager using docker compose by run

```
cd ~/monitoring-lab
docker-compose up -d
```


## Restart Prometheus to apply the new configuration

- Use docker-compose to restart the prometheus container and apply the new configuration

```
docker-compose restart prometheus
```

## Explore Alertmanager

- Browse to prometheus using the following Url

```
http://localhost:9090
```

- Browse to the "Alerts" section to check the alerts status

<kbd>
  <img src="/images/alertmanager-01.png" width="600">
</kbd><br/><br/>

- Browse to "Status/Rules" section to check the configured rules

<kbd>
  <img src="/images/alertmanager-02.png" width="600">
</kbd><br/><br/>

- Finally, to check the Alertmanager portal browse to:

```
http://localhost:9093
```

- To generate an alert, let's stop the node_exporter container

```
docker-compose stop node-exporter
```

- After a minute you will see the alert in the alertmanager portal
