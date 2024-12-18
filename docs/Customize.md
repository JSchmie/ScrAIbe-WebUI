# Customize your WebUI

Welcome to the comprehensive guide on customizing your ScrAIbe-WebUI! Whether you're just starting out or looking to fine-tune your setup, this guide will help you transform your WebUI to meet your specific needs. Let’s explore how to effectively use the config.yaml file and other configuration options to enhance your ScrAIbe-WebUI experience.

## How to Use Custom Settings

Let's use a simple example to demonstrate the process. Suppose we want to change the **port** to 8080 and set the **whisper model** to the latest `large-v3`.

### Step 1: Preparation

First, ensure you have successfully set up ScrAIbe-WebUI. If not, please follow our [Installation Guide](GETTING_STARTED.md).

### Step 2: Choose Your Method

You have two options: use our `command-line interface` (CLI) or the `Python` interface. Additionally, you can choose whether to use a structured dictionary, a YAML file, or keyword arguments as your input. If you're using `docker`, the CLI is a great choice. If you're using `docker-compose`, refer to our [Getting Started with Docker](./GETTING_STARTED_DOCKER.md).

### Using the CLI

Create a file called `custom.yaml` with the following content:

```yaml
launch:
    server_port: 8080
scraibe_params:
  whisper_model : 'large-v3'
```

Then, run the WebUI using the appropriate command to specify this configuration file:

```bash
scraibe-webui start -c custom.yaml
```

### Using the Python Interface

Import the `App` class from `scraibe_webui`, then launch the application using your custom YAML file:

```python
from scraibe_webui import App 

app = App.load_config("custom_config.yaml")

app.start()
```

### Quick Configuration Without YAML

Creating a YAML file makes sense when you need to change many parameters. But if you just want to try something quickly, you can skip the YAML file and use direct commands.

#### Quick CLI Version

Use the `scraibe-webui start` command with `--server-kwargs` to specify the desired settings directly in the command line:

```bash
scraibe-webui start server_port=8080 whisper_model=large-v3
```

#### Quick Python Version

Import the `App` class from `scraibe_webui`, then define the settings in a dictionary and launch the application with these settings:

```python
from scraibe_webui import App 

settings = {launch:{server_port: 8080},
            scraibe_params: { whisper_model : 'large-v3'}
            } 

App(**settings).start()
```

Alternatively, pass the settings directly as keyword arguments when launching the application:

```python
from scraibe_webui import App 

settings = {launch:{server_port: 8080},
            scraibe_params: { whisper_model : 'large-v3'}
            } 

App(server_port = 8080 ,whisper_model = 'large-v3').start()
```

By now, you should be able to run your custom WebUI. But you might ask: What are my options to customize my own instance?

Until now we’ve covered both the CLI and Python interfaces for configuring your WebUI, making it accessible even for beginners. For a more structured approach, we recommend using a YAML file, especially when changing multiple settings.

## Customizing Your `config.yaml`

The `config.yaml` file is the heart of your `ScrAIbe-WebUI` customization. This file allows you to define various settings that control how your WebUI behaves and appears. Below, we will dive into the key sections of the `config.yaml` file and explain how to customize each part. You can find the original `config.yaml` file in the repository under [`scraibe_webui/misc/config.yaml`](../scraibe_webui/misc/config.yaml)

### Key Sections

1. Interface Type
2. Gradio Launch Configuration
3. Gradio Queue Configuration
4. Layout Configuration
5. SCRAIBE Parameters
6. Setting Up the Email Backend for Async Interface
7. Advanced Configuration

### Interface Type

This is by far the most important setting for you. As we already know, there are two types of `ScrAIbe-WebUI` out there: the first one uses a synchronous (live and simple) approach, and the second one uses an asynchronous approach where you get your transcripts sent via email. You can select the type of the interface like so:

```yaml
interface_type: simple
```

- `interface_type`: Choose between `simple` or `async`.

The `simple` type doesn’t require email setup, while async handles transcriptions. The setup of the email configuration will be covered later in this tutorial.

### 2. Gradio Launch Configuration

This section shouldn't be discussed in too much detail here since it primarily acts as a wrapper for the underlying `gradio` functions that handle all the magic 🧙 for you. Check out our default [`config.yaml`](../scraibe_webui/misc/config.yaml) to see the default values.

For more detailed information, we recommend using the documentation that `gradio` provides about their `launch` function. You can find the documentation [here](https://www.gradio.app/docs/gradio/blocks#blocks-launch).

**Note:** Ensure you are referring to the documentation for the correct version of `gradio`. Also, make sure to check the [`requirements.txt`](../requirements.txt) file in the repository for the necessary dependencies.

**Example `config.yaml` for Launch Configuration:**

```yaml
launch: 
  server_port: 8080
  server_name: "0.0.0.0"
  auth: [my_username , my_passwd ]
```

### 3. Gradio Queue Configuration

Similar to the launch configuration, the queue configuration serves as a wrapper for the `gradio` functions that manage request queues. This section allows you to control how requests are queued and processed in your WebUI. Refer to our default [`config.yaml`](../scraibe_webui/misc/config.yaml) to see the default values.

For more detailed information on configuring the queue, we recommend consulting the `gradio` documentation on queue settings. You can find the documentation [here](https://www.gradio.app/docs/gradio/queue).

**Note:** Ensure you are referring to the documentation for the correct version of `gradio`. Also, make sure to check the [`requirements.txt`](../requirements.txt)  file in the repository for the necessary dependencies.

**Example `config.yaml`  for Queue Configuration:**

```yaml
queue:
  max_size: 10
```

### 4. Layout Configuration (Updated)

This section details how to configure and customize the layout of your WebUI. It covers specifying custom HTML files for the header and footer, using inline CSS for styling, and adjusting layout behavior for your project. Recent updates have introduced significant changes, including the deprecation of `header_css_path` and `footer_css_path`. Now, all CSS must be defined inline within the HTML file, and the API path has changed to `/gradio_api`.

---

Example `config.yaml` for Layout Configuration:

```yaml
layout:
  header: path/to/my/header.html
  header_format_options:
    header_logo_url: https://www.example.com/
    header_logo_src: path/to/my/logo/logo.png
  footer: path/to/my/footer.html
  footer_format_options: {}
  show_settings: true
```

---

### Configuration Options

- **header:**  
  Path to an HTML file for the header. Ensure the file is valid HTML and includes any required inline CSS.

- **header_format_options:**  
  Customization options for the header, such as logos or URLs, referenced using `{}` in the HTML.

  Example `header.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScrAIbe</title>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;700&display=swap" rel="stylesheet">
    <style>
        .header-container {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
        }
        .logo-container {
            position: absolute;
            top: 50%;
            right: 20px;
            transform: translateY(-50%);
            width: 150px;
        }
        .logo {
            width: 100%;
            height: auto;
        }
        .header-title {
            font-family: 'Cormorant Garamond', serif;
            font-size: 40px;
            font-weight: bold;
            color: #50AF31;
        }
    </style>
</head>
<body>
    <div class="header-container">
        <h1 class="header-title">ScrAIbe</h1>
        <div class="logo-container">
            <a href="{header_logo_url}">
                <img src="/gradio_api/file={header_logo_src}" alt="Logo" class="logo">
            </a>
        </div>
    </div>
</body>
</html>
```

- **footer:**  
  Path to an HTML file for the footer. Like the header, it should include inline CSS.

- **footer_format_options:**  
  Customization options for the footer, similar to `header_format_options`.

- **show_settings:**  
  Boolean to enable/disable the settings panel in the Gradio interface. This feature is experimental.

---

### Updated Important Notes

1. **File Imports**:  
   When importing files such as logos, CSS, or other assets, it is critical to prefix the file path with `/gradio_api/file=` in the HTML file. Otherwise, these imports will not work correctly in Gradio.

    Example:
    ```html
    <link rel="stylesheet" href="/gradio_api/file=path/to/your/style.css">
    ```

2. **File Detection**:  
   Gradio automatically detects file paths based on specific keywords or extensions. These include keys like `src`, `file`, or `path`, and values ending with `.html`, `.css`, `.png`, `.jpg`, `.jpeg`. Note that `.svg` is no longer supported as a file format.

    Example:
    ```yaml
    header_format_options:
      header_logo_src: /gradio_api/file=path/to/logo.png
    ```

    This path will be correctly detected and processed by Gradio.

3. **SVG File Format Deprecated**:  
   SVG files are no longer supported in Gradio. Use other common formats like `.png`, `.jpg`, or `.jpeg`. Ensure images are appropriately sized and optimized for the web to avoid performance issues.

---

#### Best Practices

- Ensure all HTML files are self-contained without reliance on external CSS files.  
- Use clear, descriptive variable names in `header_format_options` for better maintainability.  
- Validate your HTML to prevent layout issues in Gradio.  
- Test file imports thoroughly to ensure paths are recognized correctly by Gradio.

---

### 5. SCRAIBE Parameters

This section allows you to configure the specific parameters for the SCRAIBE application. These settings control the models and resources used by SCRAIBE, including the whisper model, device type, and more.

**Example `config.yaml` for SCRAIBE Parameters:**

```yaml
scraibe_params:
  whisper_model: medium
  whisper_type: whisper
  dia_model: null
  use_auth_token: null
  device: null
  num_threads: 0
```

- **whisper_model**: Specifies the whisper model to use. Available models include `tiny`, `base`, `small`, `medium`, and `large-v*`.
- **whisper_type**: Determines whether to use the original whisper or the faster-whisper backend. Options are `whisper` or `faster-whisper`.
- **dia_model**: Specifies the dialogue model to use.
- **use_auth_token**: Authentication token for accessing specific models or services.
- **device**: Set the device on which to run the models. Options include `cpu` or `cuda`.
- **num_threads**: Specifies the number of threads to use if running on CPU.

**Detailed Description:**

- **whisper_model**: This parameter sets the specific whisper model that SCRAIBE will use for processing. Available models are:
  - `tiny`
  - `base`
  - `small`
  - `medium`
  - `large`
  - `large-v2`
  - `large-v3`
  - `large-v3-turbo`

  Each model varies in terms of size and accuracy, with `tiny` being the smallest and fastest, and `large-v3` being the most accurate but requiring more resources.

- **whisper_type**: This setting allows you to choose between the original whisper backend and the faster-whisper backend. The original whisper backend is the standard processing method, while faster-whisper may offer different features or optimizations. Choose `whisper` for the standard whisper models method or `faster-whisper` for the alternative [faster-whisper](https://github.com/SYSTRAN/faster-whisper) backend.

- **dia_model**: This parameter allows you to specify the diarisation model that SCRAIBE will use. It is left as `null` by default, and you can set it to the specific [pyannote](https://github.com/pyannote/pyannote-audio) model you wish to use. The diarisation model we use is a wrapper for the pyannote audio model, which is renowned for its accurate speaker diarisation.

- **use_auth_token**: This parameter allows you to specify the Hugging Face authentication token needed for accessing certain models or services. Specifically, it is required if you wish to use one of the original pyannote models hosted on Hugging Face. By providing the Hugging Face authentication token here, you ensure access to these advanced and premium features, enabling SCRAIBE to utilize the full capabilities of the pyannote audio models.

- **device**: This parameter sets the device on which the models will run. You can choose `cpu` for standard processing or `cuda` if you have a compatible GPU and want to leverage its power for faster processing.

- **num_threads**: When using a CPU for processing, this parameter lets you define the number of threads that SCRAIBE can use. Setting this to a higher number can improve processing times by utilizing multiple CPU cores.

For more detailed information, refer to our default `config.yaml`.

You can also include other keyword arguments that the `ScrAIbe` class supports, like `verbose`.

### 6. Setting Up the Email Backend for Async Interface

To use the asynchronous interface type, where transcripts are sent via email, you need to configure the email backend properly. This involves setting up SMTP server details, email templates, and other related settings in the `config.yaml` file. **Note: These settings are only used when using the asynchronous backend.**

**Example `config.yaml` for Email Backend Configuration:**

```yaml
mail:
  sender_email: null
  smtp_server: null
  smtp_port: 0
  sender_password: null
  connection_type: TLS   # 'SSL', 'TLS', or 'PLAIN'
  context: default # Union[None, str, dict, ssl.SSLContext]
  default_subject: "SCRAIBE"
  error_template: scraibe_webui/misc/error_notification_template.html
  error_subject: An error occurred during processing.
  error_format_options:
    contact_email: support@mail.com 
  success_template: scraibe_webui/misc/success_template.html
  success_subject: "Your transcript is ready."
  success_format_options:
    contact_email: support@mail.com
  upload_notification_template: scraibe_webui/misc/upload_notification_template.html
  upload_subject: "Upload Successful"
  upload_notification_format_options:
    queue_position: null
    contact_email: support@mail.com
  mail_css_path: scraibe_webui/misc/mail_style.css
```

**Detailed Description:**

- **sender_email**: The email address that will be used to send out emails. This should be a valid email address from which you have permission to send emails.
- **smtp_server**: The SMTP server address that will handle the sending of emails. For example, `smtp.gmail.com` for Gmail.
- **smtp_port**: The port used by the SMTP server. Common ports are `587` for TLS and `465` for SSL.
- **sender_password**: The password or app-specific password for the sender email. Ensure this is kept secure and not exposed publicly.
- **connection_type**: Different SMTP servers use various encryption methods. The available options are:
  - `SSL`: Starts the connection to the SMTP client using SSL for all communication (e.g., Gmail).
  - `TLS`: Uses TLS for encryption and authentication.
  - `PLAIN`: Does not use any form of encryption or authentication.
- **context**: Sets the context information for Python's `smtplib.SMTP` or `smtplib.SMTP_SSL` connections. If set to `default`, `ssl.create_default_context()` will be used. If you provide a `dict`, you are passing keyword arguments for the default context. Alternatively, you can pass an `ssl.SSLContext` using the Python API.
- **default_subject**: The default subject line for emails sent by the application.
- **error_template**: Path to the HTML template used for error notification emails. Customize this template as needed.
- **error_subject**: Subject line for error notification emails.
- **error_format_options**: Format options for error emails. This typically includes the contact email or any other relevant information.
  - **contact_email**: Your contact email address. This can be customized or additional options can be added as necessary.
- **success_template**: Path to the HTML template used for success notification emails. Customize this template as needed.
- **success_subject**: Subject line for success notification emails.
- **success_format_options**: Format options for success emails. This typically includes the contact email or any other relevant information.
  - **contact_email**: Your contact email address. This can be customized or additional options can be added as necessary.
- **upload_notification_template**: Path to the HTML template used for upload notification emails. Customize this template as needed.
- **upload_subject**: Subject line for upload notification emails.
- **upload_notification_format_options**: Format options for upload notification emails. This typically includes queue position and contact email.
  - **queue_position**: Information about the queue position if relevant.
  - **contact_email**: Your contact email address. This can be customized or additional options can be added as necessary.
- **mail_css_path**: Path to the CSS file used for styling the emails.

The templates and the related CSS, as well as additional arguments (like the contact email), can be configured to your own needs. You can add additional formatting parameters as required.

**Demo Template Example with More Format Options:**

**success_template.html:**

```html
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" type="text/css" href="{{ mail_css_path }}">
</head>
<body>
  <h1>Transcript Ready</h1>
  <p>Dear User,</p>
  <p>Your transcript is now ready.</p>
  <p>Thank you for using our service!</p>
  <p>Best regards,</p>
  <p>{{ company_name }}</p>
  <footer>
    <p>Contact us at <a href="mailto:{{ contact_email }}">{{ contact_email }}</a></p>
  </footer>
</body>
</html>
```

In this example, additional format options such as `user_name`, `download_link`, and `company_name` are used to personalize the success notification email. he related part in your YAML file would look like:

```yaml
success_template: scraibe_webui/misc/success_template.html
success_format_options:
    company_name: company_name
    contact_email: support@mail.com
```

### 7. Advanced Configuration

The advanced settings allow for fine-tuning the performance and behavior of your ScrAIbe WebUI. These settings are particularly useful for optimizing resource usage and managing how jobs are processed.

**Example `config.yaml` for Advanced Settings:**

```yaml
advanced:
  keep_model_alive: false 
  concurrent_workers_async: 1 
```

**Detailed Description:**

- **keep_model_alive**: This setting is only available in the simple (synchronous) interface. When set to `true`, it keeps the model loaded while the WebUI is running. If set to `false`, the model is loaded each time a job is queued. This can save loading time for each job at the cost of increased memory usage while the WebUI is active.

- **concurrent_workers_async**: This setting is used only in the async interface, as the async interface does not rely on Gradio's queue but has its own built-in queue system. This parameter determines how many concurrent jobs can be run. Increasing this number can improve throughput but may also increase resource usage.

By configuring these parameters, you can better manage how resources are allocated and how efficiently jobs are processed in both the synchronous and asynchronous interfaces.

## Summary

In this tutorial, we have covered the various ways you can customize your ScrAIbe-WebUI using the `config.yaml` file. From setting up the interface type to configuring advanced settings, you now have the knowledge to tailor the WebUI to fit your specific needs. Whether you're using the CLI or the Python interface, creating a structured YAML file ensures a smooth and efficient configuration process.

Remember, the `config.yaml` file is a powerful tool that gives you control over how your WebUI operates and appears. Take advantage of the customization options to create a setup that works best for you.

Happy customizing! 🎉
