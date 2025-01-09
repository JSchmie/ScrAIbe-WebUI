# Getting Started with ScrAIbe-WebUI

Welcome to the ScrAIbe-WebUI! This guide will walk you through the steps to get started with setting up and running your WebUI. Follow these steps to quickly get up and running.

## Prerequisites

Before installing ScrAIbe-WebUI, ensure you have the following prerequisites:

- **Python**: Version 3.11 or later.
- **PyTorch**: Version 2.0 or later.
- **CUDA**: A compatible version with your PyTorch version if you want to use GPU acceleration.

**Note:** PyTorch should be automatically installed with the pip installer. However, if you encounter any issues, you should consider installing it manually by following the instructions on the [PyTorch website](https://pytorch.org/get-started/locally/).

---

## Install ScrAIbe-WebUI

Install ScrAIbe-WebUI on your local machine with ease using PyPI.

```bash
pip install scraibe-webui
```

If you encounter problems with your installation or you want to have an even easier setup for a production environment, consider using our Docker image. For a complete walkthrough on how to set up and use Docker, check out our [Docker Getting Started](GETTING_STARTED_DOCKER.md) guide.

---

## Install Pre-Release or Development Version

To install the latest development version from GitHub, use the following command:

```bash
pip install git+https://github.com/JSchmie/ScrAIbe-WebUI.git@develop
```

Alternatively, you can install the latest pre-release from PyPI:

```bash
pip install --pre scraibe-webui
```

---

## Setting Up from Scratch

For a more hands-on approach, you can set up ScrAIbe-WebUI from scratch by cloning the repository and installing it in editable mode.

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/JSchmie/ScrAIbe-WebUI.git
```

Navigate to the cloned directory:

```bash
cd ScrAIbe-WebUI
```

### Step 2: Install Dependencies

Install the required dependencies in editable mode:

```bash
pip install -e .
```

This command ensures that any changes made to the local source code will be immediately reflected without reinstalling the package.

### Step 3: Verify Installation

After installation, verify that ScrAIbe-WebUI is set up correctly by running the following command:

```bash
scraibe-webui --help
```

If the installation was successful, this will display a list of available commands and options.

---

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

---

## Explore Customization Options

Did you know there is a wide variety of customization options available? Customize the appearance, functionality, and performance of your WebUI to better suit your needs. To explore these options, check out our [Customize your WebUI](Customize.md) guide.

---

Happy transcribing! 🎉
`
