# Getting Started with ScrAIbe-WebUI

Welcome to the ScrAIbe-WebUI! This guide will walk you through the steps to get started with setting up and running your WebUI. Follow these steps to quickly get up and running.

## Prerequisites

Before installing ScrAIbe-WebUI, ensure you have the following prerequisites:

- **Python**: Version 3.11 or later.
- **PyTorch**: Version 2.0 or later.
- **CUDA**: A compatible version with your PyTorch Version if you want to use GPU acceleration.

**Note:** PyTorch should be automatically installed with the pip installer. However, if you encounter any issues, you should consider installing it manually by following the instructions on the [PyTorch website](https://pytorch.org/get-started/locally/).

## Install ScrAIbe WebUI

Install ScrAIbe-WebUI on your local machine with ease using PyPI.

```bash
pip install scraibe-webui
```

If you want to install the development version, you can do so by installing it from GitHub:

```bash
pip install git+https://github.com/JSchmie/ScrAIbe-WebUI.git@develop
```

or from PyPI using our latest pre-release:

```bash
pip install --pre scraibe-webui
```

If you encounter problems with your installation or you want to have an even easier setup for a production environment, consider using our Docker image instead. For a complete walkthrough on how to set up and use Docker, check out our [Docker Getting Started](GETTING_STARTED_DOCKER.md) guide.

## Start the WebUI

Starting the WebUI with the default settings is straightforward. You can use either the command line interface or a short Python script.

### Using the Command Line Interface

To start the WebUI using the command line interface, simply run:

```bash
scraibe-webui start
```

### Using Python

Alternatively, you can start the WebUI using a Python script:

```python
from scraibe_webui import App 

App().launch()
```

### Explore Customization Options

Did you know there is a wide variety of customization options available? Customize the appearance, functionality, and performance of your WebUI to better suit your needs. To explore these options, check out our [Customize your WebUI](Customize.md) guide.
