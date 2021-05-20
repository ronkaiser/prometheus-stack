# Lab 01: Deploy Prometheus using Docker Compose

## Summary

 - Configure your workspace
 - Create Prometheus configuration file
 - Deploy Prometheus using Docker Compose
 - Explore prometheus

## Configure your workspace

- During the tutorial we will create several files that will be pased as volumes to the different applications. To make it easier let's create a new directory to be used as our workspace (we will use "~/monitoring-lab" but you can use a different one if you prefer)

```
mkdir ~/monitoring-lab
```

- Create a dedicated folder for your prometheus files

```
mkdir ~/monitoring-lab/prometheus
```

## Create Prometheus configuration file

- Now let's create a basic configuration file for prometheus (I will use nano, you can use a different editor)

```
nano ~/monitoring-lab/prometheus/prometheus.yml
```

- The content of the file should be the below:

```
# Global Configuration
global:
  scrape_interval:     15s
  evaluation_interval: 15s 
  scrape_timeout: 10s

scrape_configs:

  - job_name: 'prometheus'
    static_configs:
    - targets: ['localhost:9090']
```

## Deploy Prometheus using Docker Compose

- Let's create a docker-compose file in the workspace root

```
nano ~/monitoring-lab/docker-compose.yml
```

- The content of the docker-compose file should be the following:

```
version: '2.4'
services:
  prometheus:
    image: "prom/prometheus:v2.26.0"
    container_name: prometheus
    # REPLACE LOCALHOST WITH THE SERVER IP IF YOU WILL ACCESS IT FROM ANOTHER SERVER
    hostname: localhost
    restart: unless-stopped
    mem_limit: 4G
    ports:
     - "9090:9090"
    command:
     - '--config.file=/etc/prometheus/prometheus.yml'
    volumes:
     - "./prometheus/:/etc/prometheus/"
     - "prometheus_data:/prometheus"
    networks:
     - "monitoring"
volumes:
  prometheus_data:
networks:
  monitoring:
```

- Deploy prometheus using docker compose

```
cd ~/monitoring-lab
docker-compose up -d
```

## Explore prometheus

- Browse to your prometheus instance from any browser

```
http://localhost:9090/
```

- Let's run our first query by write the below in the "Expression" field and click "Execute"

```
scrape_duration_seconds
```

<kbd>
  <img src="/images/prometheus-01.png" width="600">
</kbd><br/><br/>

- Right now you are seeing the time it took to Prometheus to scrape (collect) it metrics the last time, but let's click on "Graph" to see the historical data

<kbd>
  <img src="/images/prometheus-02.png" width="600">
</kbd><br/><br/>

- But what is being monitored by prometheus? click on "Targets" under "Status" to check it

<kbd>
  <img src="/images/prometheus-03.png" width="600">
</kbd><br/><br/>

- In addition, you can see the current prometheus configuration under "Status/Configuration" and the prometheus information in "Status/Runtime & Build Information"

<kbd>
  <img src="/images/prometheus-04.png" width="600">
</kbd><br/><br/>

- Finally, if you check the current rules under "Status/Rules" and the current alerts under "Alerts" you will see that they are empty (later we will configure some)

<kbd>
  <img src="/images/prometheus-05.png" width="600">
</kbd><br/><br/>