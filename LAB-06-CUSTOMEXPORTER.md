# Lab 06: Write a custom prometheus exporter

## Summary

 - Configure your workspace
 - Create an exporter using python
 - Configure the Dockerfile for your exporter
 - Deploy your custom exporter using Docker Compose
 - Configure prometheus to collect the metrics from your exporter
 - Inspect your exporter metrics


 ## Configure your workspace

- Create a dedicated folder for your custom exporter files

```
mkdir ~/monitoring-lab/customexporter
```

 ## Create an exporter using python

- Create a requirements file to add flask as dependency

```
nano ~/monitoring-lab/customexporter/requirements.txt
```

- Add the following content

```
Flask==1.0.0
```

- Write the application code

```
nano ~/monitoring-lab/customexporter/app.py
```

- Add the following content (it will return a random number in "localhost:5000/metrics" in the following format "custom_metric <random-number>")

```
from flask import Flask
from random import randrange

app = Flask(__name__)

@app.route("/metrics", methods=["GET"])
def metrics():
    random = randrange(10)
    return "custom_metric" + " " + str(random)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

 ## Configure the Dockerfile for your exporter

- Create a Dockerfile for our exporter

```
nano ~/monitoring-lab/customexporter/Dockerfile
```

- Add the following content

```
FROM python:3.7.7
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
```

 ## Deploy your custom exporter using Docker Compose

- Let's add our exporter container to our docker compose file

```
nano ~/monitoring-lab/docker-compose.yml
```

- Add the following service:

```
custom-exporter:
  build: "customexporter"
  container_name: customexporter
  restart: unless-stopped
  ports:
    - "5000:5000"
  networks:
    - "monitoring"
```

- Deploy your custom exporter using docker compose by run

```
cd ~/monitoring-lab
docker-compose up -d
```

 ## Configure prometheus to collect the metrics from your exporter

- Let's create a new targets file under the prometheus directory

```
nano ~/monitoring-lab/prometheus/custom-targets.yml
```

- Add the content below to the file

```
- targets: ['customexporter:5000']
  labels:
    name: 'My Exporter'
```

- Configure "prometheus.yml" to scrape the new target, your prometheus configuration should looks like below

```
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

  - job_name: 'My Exporter'
    file_sd_configs:
      - files:
         - custom-targets.yml
```

- Restart the prometheus container and apply the new configuration

```
docker-compose restart prometheus
```

 ## Inspect your exporter metrics

- Check the custom exporter metric by browse to the url below (refresh several times)

```
http://localhost:5000/metrics
```

- As you can note, a custom exporter is just a server that print key-value pairs of metrics

- In the Prometheus portal, run the following query under the "Graph" section and click "Execute"

```
custom_metric
```

<kbd>
  <img src="/images/customexporter-01.png" width="600">
</kbd><br/><br/>

- You can check the historical data by see "Graph" result

<kbd>
  <img src="/images/customexporter-02.png" width="600">
</kbd><br/><br/>
