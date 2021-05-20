# Lab 04: Deploy and configure Grafana using Docker Compose

## Summary

 - Deploy Grafana using Docker Compose
 - Configure a Prometheus Datasource
 - Import a community dashboard
 - Create your own dashboard


## Deploy Grafana using Docker Compose

- Let's add a Grafana container to our docker compose file to visualize our metrics

```
nano ~/monitoring-lab/docker-compose.yml
```

- Add the grafana service (note that it includes a volume named "grafana_data"):

```
  grafana:
    image: "grafana/grafana:7.5.2"
    container_name: grafana
    restart: unless-stopped
    mem_limit: 4G
    ports:
      - "80:3000"
    volumes:
      - "grafana_data:/var/lib/grafana"
    networks:
      - monitoring
    environment:
      # INSTALL SOME GRAFANA PLUGINS AUTOMATICALLY
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource,grafana-piechart-panel,novalabs-annotations-panel,vonage-status-panel,fetzerch-sunandmoon-datasource,natel-discrete-panel,natel-influx-admin-panel
      # YOU CAN CHANGE THE ADMIN PASSWORD USING THIS VARIABLE
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

- And add the grafana volume to the volumes sections at the end of the file:
```
volumes:
  prometheus_data:
  grafana_data:
```

- Deploy Grafana using docker compose by run

```
cd ~/monitoring-lab
docker-compose up -d
```


## Configure a Prometheus Datasource

- Browse to grafana from your browser (can take few minutes to start)

```
http://localhost:80
```

- Login using the following credentials

```
username: admin
password: admin
```

- Go to "Configuration/Data Sources" and click on "Add data source"

<kbd>
  <img src="/images/grafana-01.png" width="600">
</kbd><br/><br/>

- Select "Prometheus", set the Url below and click "Save & Test" (for everything else keep defaults)

```
URL: http://prometheus:9090
```

- Ensure that the data source is working

<kbd>
  <img src="/images/grafana-02.png" width="600">
</kbd><br/><br/>


## Import a community dashboard

- To import a dashboard click on "New/Import"

<kbd>
  <img src="/images/grafana-03.png" width="600">
</kbd><br/><br/>

- Paste the following id and click "Load"

```
Id: 1860
```

<kbd>
  <img src="/images/grafana-04.png" width="600">
</kbd><br/><br/>

- Set the dashboard options as below and click "Import"

```
Name: My Imported Dashboard
Folder: General
Prometheus: Prometheus (your data source)
```

<kbd>
  <img src="/images/grafana-05.png" width="600">
</kbd><br/><br/>

- Change the time range to 5 minutes as shown in the picture

<kbd>
  <img src="/images/grafana-06.png" width="600">
</kbd><br/><br/>


## Create your own dashboard

- Let's create a dasboard from scratch in a new folder, to create the folder click on "New/Folder"

<kbd>
  <img src="/images/grafana-07.png" width="600">
</kbd><br/><br/>

- Name it "Custom Dashboards" and click on "Create"

- Create a new dashboard by click on "New/Dashboard" (or just click on "Create Dashboard")

<kbd>
  <img src="/images/grafana-08.png" width="600">
</kbd><br/><br/>

- Let's create a variable for our dashboard by click on "Dashboard Settings" and go to "Variables"

<kbd>
  <img src="/images/grafana-09.png" width="600">
</kbd><br/><br/>

- Then create a new variable with the following details:

```
Name: target
Label: Target
Type: Query
Hide: <empty>
Data Source: Prometheus
Refresh: On Dashboard Load
Query: label_values(node_uname_info, job)
Sort: Alphabetical (asc)
```

<kbd>
  <img src="/images/grafana-10.png" width="600">
</kbd><br/><br/>

- Come back to the dashboard editor by click on "Go Back" or by click "Esc"

<kbd>
  <img src="/images/grafana-11.png" width="600">
</kbd><br/><br/>

- Click on "Add Query" and configure it with the following details, then click on the next step:

```
Query: Prometheus (your data source)
PromQL Query: up{job="$target"}
```

<kbd>
  <img src="/images/grafana-12.png" width="600">
</kbd><br/><br/>

- Configure the visualization with the following details, then move to the next step:

```
Value/Show: Current
Type: Singlestat
Coloring/Background: Enabled
Coloring/Thresholds: 1,0.9
(Invert the colors to set green for "1" and red for "0")
Value Mappings: add "1=Up" and "0=Down"
```

<kbd>
  <img src="/images/grafana-13.png" width="600">
</kbd><br/><br/>

- Set the widget title and description as described below, then click the "save" icon

```
Title: Server Status
Description: Show if the status is running or not
```

<kbd>
  <img src="/images/grafana-14.png" width="600">
</kbd><br/><br/>

- Save the dashboard as "My Custom Dashboard" in the "Custom Dashboards" folder

<kbd>
  <img src="/images/grafana-15.png" width="600">
</kbd><br/><br/>

- To test your dashboard let's stop the node_exporter container

```
docker-compose stop node-exporter
```

- Check your dashboard to see that the dashboard was updated (may take a minute), then start your node_export service again

```
docker-compose start node-exporter
```
