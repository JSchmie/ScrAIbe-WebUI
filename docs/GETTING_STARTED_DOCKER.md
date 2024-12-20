# Getting Started Using Docker with ScrAIbe-WebUI

Welcome to the Docker setup guide for ScrAIbe-WebUI! This guide will walk you through the steps to get started with setting up and running your WebUI using Docker. Follow these steps to quickly get up and running with a Dockerized environment.

## Prerequisites

Before setting up ScrAIbe-WebUI with Docker, ensure you have the following prerequisites:

- **Docker**: Installed and running on your machine. You can download Docker from the official [Docker website](https://www.docker.com/get-started).
- **Docker Compose**: Installed and running on your machine. You can download Docker Compose from the official [Docker Compose website](https://docs.docker.com/compose/install/).
- **Nvidia GPU Support (Optional)**: If you want to use GPU, ensure you have the Nvidia Container Toolkit installed and configured on your machine. You can find installation instructions on the [Nvidia Container Toolkit website](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

---

## Install ScrAIbe-WebUI Using Docker

### Step 1: Clone the Repository (Optional)

First, clone the ScrAIbe-WebUI repository from GitHub:

```bash
git clone https://github.com/JSchmie/ScrAIbe-WebUI.git
cd ScrAIbe-WebUI
```

---

### Step 2: Deployment Options

#### CPU Deployment

To run ScrAIbe-WebUI without GPU support, use the following `docker-compose.yml` file:

```yaml
services:
    scraibe:
      build: .
      container_name: scraibe-webui
      ports:
        - '7860:7860'
      volumes: 
        - ./data:/data
```

Deploy the container with:

```bash
docker compose up
```

This setup is ideal for environments without Nvidia GPUs or for basic transcription tasks that do not require GPU acceleration.

---

#### GPU Deployment

To enable GPU support, update your `docker-compose.yml` file to include GPU configuration:

```yaml
services:
    scraibe:
      build: .
      container_name: scraibe-webui
      ports:
        - '7860:7860'
      volumes: 
        - ./data:/data
      deploy:
        resources:
          reservations:
            devices:
              - driver: nvidia
                count: 1
                capabilities: [gpu]
```

Ensure you have installed the Nvidia Container Toolkit and configured it properly. Then deploy the container with:

```bash
docker compose up
```

This setup is optimized for faster transcription tasks using GPU acceleration.

---

### Step 3: Access the WebUI

Once the Docker container is running, access the WebUI in your web browser at:

```bash
http://localhost:7860
```

---

## Using the Pre-Built Image from Docker Hub

If you prefer not to build the image manually, you can use the pre-built image available on Docker Hub.

### Step 1: CPU Deployment

Run the container using the pre-built image:

```bash
docker run -d --name scraibe-webui -p 7860:7860 -v $(pwd)/data:/data hadr0n/scraibe-webui
```

### Step 2: GPU Deployment

For GPU support, include the `--gpus 'all'` flag:

```bash
docker run -d --name scraibe-webui -p 7860:7860 --gpus 'all' -v $(pwd)/data:/data hadr0n/scraibe-webui
```

Access the WebUI in your web browser at:

```bash
http://localhost:7860
```

---

## Custom Configuration

To use a custom configuration, you can place a `config.yaml` file in the `./data` folder of your mounted volume.

> **Note**: Currently, this file is created as the root user if Docker is run as root. We are working on resolving this issue.

---

## Summary

By following this guide, you should be able to install, run, and customize your ScrAIbe-WebUI effectively using Docker. Whether deploying on a CPU or GPU, this setup provides a robust and production-ready environment. For more details on customization options, refer to our [Customize your WebUI](Customize.md) guide.
