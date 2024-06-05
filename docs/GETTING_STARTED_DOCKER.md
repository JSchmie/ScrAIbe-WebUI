# Getting Started Using Docker with ScrAIbe-WebUI

Welcome to the Docker setup guide for ScrAIbe-WebUI! This guide will walk you through the steps to get started with setting up and running your WebUI using Docker. Follow these steps to quickly get up and running with a Dockerized environment.

## Prerequisites

Before setting up ScrAIbe-WebUI with Docker, ensure you have the following prerequisites:

- **Docker**: Installed and running on your machine. You can download Docker from the official [Docker website](https://www.docker.com/get-started).
- **Docker Compose**: Installed and running on your machine. You can download Docker Compose from the official [Docker Compose website](https://docs.docker.com/compose/install/).
- **Nvidia GPU Support (Optional)**: If you want to use GPU, ensure you have the Nvidia Container Toolkit installed and configured on your machine. You can find installation instructions on the [Nvidia Container Toolkit website](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

## Install ScrAIbe-WebUI Using Docker

### Step 1: Clone the Repository

First, clone the ScrAIbe-WebUI repository from GitHub.

```bash
git clone https://github.com/JSchmie/ScrAIbe-WebUI.git
cd ScrAIbe-WebUI
```

### Step 2: Build and Run the Docker Container

To build and run the Docker container, use the following commands:

```bash
docker compose up
```

This command will build the Docker image and start the container using the configuration specified in the `docker-compose.yml` file.

### Step 3: Access the WebUI

Once the Docker container is running, you can access the WebUI in your web browser at:

```bash
http://localhost:7860
```

## Example `docker-compose.yml`

Here is an example of what your docker-compose.yml file might look like:

```yaml
services:
  scraibe:
    # you can set a UID/GID in an .env file
    user: "${UID}:${GID}"
    entrypoint: ./run_docker.sh
    build: .
    environment: 
      - AUTOT_CACHE=/data/models/
    container_name: scraibe_large
    ports:
      - '7860:7860'
    volumes: 
      - type: bind
        source: data/
        target: /data/
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Using the Pre-built Image from Docker Hub

If you prefer to use the pre-built image available on Docker Hub, you can pull and run it with a single command.

### Step 1: Run the Container

Run the Docker container using the pre-built image:

```bash
docker run -d --name scraibe-webui -p 7860:7860 --gpus 'all' -v $(pwd)/data:/data hadr0n/scraibe-webui:latest_webui
```

Docker will automatically pull the image from Docker Hub if it is not already present on your system.

### Step 2: Access the WebUI

Once the Docker container is running, you can access the WebUI in your web browser at:

```bash
http://localhost:7860
```

## Custom Configuration

To use a custom configuration, you can use the `config.yaml` file in the `./data` folder of your mounted volume.  
(Currently, this file is created as root user of dckre is run as root. We are working on solving this.)

## Summary

By following this guide, you should be able to install, run, and customize your ScrAIbe-WebUI effectively using Docker. This setup provides a robust and production-ready environment, ensuring a consistent and easy-to-manage installation. For more details on customization options, refer to our [Customize your WebUI](Customize.md) guide.
