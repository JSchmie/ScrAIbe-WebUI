# Getting Started Using Docker with ScrAIbe-WebUI

Welcome to the Docker setup guide for ScrAIbe-WebUI! This guide will walk you through the steps to get started with setting up and running your WebUI using Docker. Follow these steps to quickly get up and running with a Dockerized environment.

## Prerequisites

Before setting up ScrAIbe-WebUI with Docker, ensure you have the following prerequisites:

- **Docker**: Installed and running on your machine. You can download Docker from the official [Docker website](https://www.docker.com/get-started).
- **Docker Compose**: Installed and running on your machine. You can download Docker Compose from the official [Docker Compose website](https://docs.docker.com/compose/install/).
- **Nvidia GPU Support (Optional)**: If you want to use GPU, ensure you have the Nvidia Container Toolkit installed and configured on your machine. You can find installation instructions on the [Nvidia Container Toolkit website](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

---

## Using the Pre-Built Image from Docker Hub

If you prefer not to build the image manually, you can use the pre-built image available on Docker Hub.

### Step 1: Deployment

#### a) CPU Deployment

Run the container using the pre-built image:

```bash
docker run -d --name scraibe-webui -p 7860:7860 -v $(pwd)/data:/data hadr0n/scraibe-webui
```

#### b) GPU Deployment

For GPU support, include the `--gpus 'all'` flag:

```bash
docker run -d --name scraibe-webui -p 7860:7860 --gpus 'all' -v $(pwd)/data:/data hadr0n/scraibe-webui
```

### Step 2: Access the UI

After deploying the container, you can access the web UI by navigating to `http://localhost:7860` in your web browser.

---

## Building the Docker Image Manually

To build the Docker image manually, follow these steps:

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/hadr0n/scraibe-webui.git
cd scraibe-webui
```

### Step 2: Build the Docker Image

Build the Docker image using the provided Dockerfile:

```bash
docker build -t scraibe-webui .
```

### Step 3: Run the Docker Container

Run the container using the built image:

#### a) CPU Deployment

```bash
docker run -d --name scraibe-webui -p 7860:7860 -v $(pwd)/data:/data scraibe-webui
```

#### b) GPU Deployment

For GPU support, include the `--gpus 'all'` flag:

```bash
docker run -d --name scraibe-webui -p 7860:7860 --gpus 'all' -v $(pwd)/data:/data scraibe-webui
```

### Step 4: Access the UI

After deploying the container, you can access the web UI by navigating to `http://localhost:7860` in your web browser.

---

## Building and Running with Docker Compose

For a more advanced setup, you can use Docker Compose.

### Step 1: Create a `docker-compose.yml` File

Create a `docker-compose.yml` file with the following content:

#### a) CPU Deployment

```yaml
version: '3.8'

services:
  scraibe-webui:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/data
```

#### b) GPU Deployment

For GPU support, include the GPU configuration:

```yaml
version: '3.8'

services:
  scraibe-webui:
    build: .
    ports:
      - "7860:7860"
    volumes:
      - ./data:/data
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
```

### Step 2: Deploy with Docker Compose

Deploy the stack using Docker Compose:

```bash
docker compose up
```

This setup is optimized for faster transcription tasks using GPU acceleration.

### Step 3: Access the WebUI

Once the Docker container is running, access the WebUI in your web browser at:

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
