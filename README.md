# ScrAIbe-WebUI


The Gradio App is a user-friendly interface for ScrAIbe. It enables you to run the model without any coding knowledge. Therefore, you can run the app in your browser and upload your audio file, or you can make the Framework avail on your network and run it on your local machine.

## Prequesits: 

## Install Docker: 

For more informations go to: https://docs.docker.com/engine/install/ubuntu/

### Add Docker's official GPG key:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```
# Add the repository to Apt sources:

```bash
echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

### Install the Docker packages.

To install the latest version, run:

```bash
 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

**Verify** that the Docker Engine installation is successful by running the hello-world image.

```bash
sudo docker run hello-world
```

## Install Nvidia Container Toolkit

For more informations go to: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

Configure the production repository:
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Optionally, configure the repository to use experimental packages:
```bash
sed -i -e '/experimental/ s/^#//g' /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Update the packages list from the repository:
```bash
sudo apt-get update
```
Install the NVIDIA Container Toolkit packages:

```bash
sudo apt-get install -y nvidia-container-toolkit
```


## Configure Docker to use Nvidia Container Toolkit 

Ensure:
- You installed a supported container engine (Docker, Containerd, CRI-O, Podman).
- You installed the NVIDIA Container Toolkit.

1. Configure the container runtime by using the nvidia-ctk command:
```bash
sudo nvidia-ctk runtime configure --runtime=docker
```

The nvidia-ctk command modifies the /etc/docker/daemon.json file on the host. The file is updated so that Docker can use the NVIDIA Container Runtime.

2. Restart the Docker daemon:

```bash
sudo systemctl restart docker
```

## Start Gradio with Docker

To start the application, just us the `easy_start.sh` script in this repository.  
Navigate to the path of the cloned repository and make it executable and run it with: 
```bash
chmod +x easy_start.sh
sudo ./easy_start.sh
```
The script will search for already created and/or started Gradio applications and run them, or create a new one.  
As the script is working with docker inside, it has to be started as sudo.

If you want to start the container without the script, use 
```bash
sudo docker run -d -p 7860:7860 --name scraibe_de --gpus 'all' hadr0n/scraibe:0.1.1.dev-base-de --server-kwargs inbrowser=True
```

## Alernative install it via CONDA

For more informations go to: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

1. Download Anaconda installer : https://www.anaconda.com/download/

'''bash

wet https://repo.anaconda.com/archive/Anaconda3-2024.02-1-Linux-x86_64.sh
'''

