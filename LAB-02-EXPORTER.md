# Lab 02: Configuring Node Exporter

## Note

In this section we will do basically two things: learn how to install node_exporter (in a ubuntu container) and deploy a node_exporter container using our docker compose file to monitor our server (note that it will be deployed using the host driver so it will be accessible only from other containers, you don't will be able to access it directly)


## Summary

 - Learn how to install node_exporter
 - Deploy node_exporter using Docker Compose
 - Test that node_exporter is working as expected


## Learn how to install node_exporter

- To learn how to run node_exporter let's run an ubuntu container interactively

```
docker run --rm -it --name node-exporter-test -p 9100:9100 ubuntu:18.04 /bin/bash
```

- Now, that we are attached to the container let's install wget and download the node_exporter binary

```
apt update && apt install -y wget
wget "https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz"
```

- Unpack the tarball

```
tar -xvf node_exporter-1.1.2.linux-amd64.tar.gz
```

- Move the node export binary to /usr/local/bin

```
mv node_exporter-1.1.2.linux-amd64/node_exporter /usr/local/bin/
```

- Run node_exporter manually

```
node_exporter
```

- Check current metrics exposed by node_exporter from your browser

```
http://localhost:9100/metrics
```

- That's it, as you saw node_exporter is just a binary that expose all the server metrics. However, in the "real world" you will probably want to configure it using a service

- Stop the node_export process by click Control+C and exit from the container to delete it

```
exit
```


## Deploy node_exporter using Docker Compose

- Let's add a node_exporter container to our docker compose file to monitor our server

```
nano ~/monitoring-lab/docker-compose.yml
```

- Add the following service:

```
  node-exporter:
    image: prom/node-exporter:v1.1.2
    container_name: nodeexporter
    user: root
    privileged: true
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'
    restart: unless-stopped
    expose:
      - 9100
    networks:
     - "monitoring"
```

- Deploy node_exporter using docker compose by run

```
cd ~/monitoring-lab
docker-compose up -d
```

- Note the following:
  - node_exporter will be deployed using the host driver so it will be accessible only from other containers, you don't will be able to access it directly
  - The container will run in privileged mode (administrator access)
  - Several system paths are pased to the container as docker volumes
  - The container will be attached to the "monitoring" network so will be accessible only for container attached to that network


## Test that node_exporter is working as expected

- Let's create a ubuntu container attached to the "monitoring" network to ensure that our node_exporter container is working as expected

```
docker run --rm -it --name node-exporter-check --network monitoring-lab_monitoring ubuntu:18.04 /bin/bash
```

- Now, that we are attached to the container let's install curl and check the current metrics

```
apt update && apt install -y curl
curl nodeexporter:9100/metrics
```

- Note that if your docker-compose file is under a different folder (other than ~/monitoring-lab) the newtork name may change, use the following command to see your current docker networks

```
docker network ls
```

- Exit from the container to delete it

```
exit
```