# Customize Your WebUI

Welcome to this comprehensive guide on customizing your ScrAIbe-WebUI! Whether you’re just getting started or looking to refine an existing setup, this guide will show you how to tailor your WebUI to meet your unique requirements. We’ll explore how to effectively use the `config.yaml` file, command-line arguments, and Python-based configurations to enhance your ScrAIbe-WebUI experience.

## Table of Contents

- [Customize Your WebUI](#customize-your-webui)
  - [Table of Contents](#table-of-contents)
  - [How to Use Custom Settings](#how-to-use-custom-settings)
    - [Step 1: Preparation](#step-1-preparation)
    - [Step 2: Choose Your Configuration Method](#step-2-choose-your-configuration-method)
    - [Using the CLI](#using-the-cli)
    - [Using the Python Interface](#using-the-python-interface)
    - [Quick Configuration Without YAML](#quick-configuration-without-yaml)
    - [Summary of Configuration Approaches](#summary-of-configuration-approaches)
  - [Customizing Your `config.yaml`](#customizing-your-configyaml)
    - [1. Interface Type](#1-interface-type)
      - [Detailed Explanation](#detailed-explanation)
        - [**Simple Interface**](#simple-interface)
        - [**Async Interface**](#async-interface)
      - [Choosing the Right Interface Type](#choosing-the-right-interface-type)
    - [2. Gradio Launch Configuration](#2-gradio-launch-configuration)
    - [3. Gradio Queue Configuration (Simple Interface Only)](#3-gradio-queue-configuration-simple-interface-only)
    - [4. Layout Configuration](#4-layout-configuration)
    - [Configuration Options in Detail](#configuration-options-in-detail)
    - [Updated Important Notes](#updated-important-notes)
      - [Best Practices](#best-practices)
    - [5. SCRAIBE Parameters](#5-scraibe-parameters)
    - [Parameter Details](#parameter-details)
    - [6. Setting Up the Email Backend for Async Interface](#6-setting-up-the-email-backend-for-async-interface)
    - [Parameter Details](#parameter-details-1)
    - [Best Practices for Email Configuration](#best-practices-for-email-configuration)
    - [7. Advanced Configuration](#7-advanced-configuration)
    - [Summary](#summary)
    - [Need Help or Have Questions?](#need-help-or-have-questions)


## How to Use Custom Settings

To illustrate how customization works, let’s start with a simple example: changing the **server port** to `8080` and setting the **whisper model** to `large-v3`.

### Step 1: Preparation

Before making any changes, ensure that ScrAIbe-WebUI is correctly installed and running. If it’s not set up yet, follow our [Installation Guide](GETTING_STARTED.md).

### Step 2: Choose Your Configuration Method

You can configure ScrAIbe-WebUI using several approaches:

1. **Command-Line Interface (CLI)**  
2. **Python Interface**

Within these approaches, you can provide configuration values in various formats:

- **YAML File**: Ideal for multiple or frequently changing parameters.
- **Structured Dictionaries**: Useful for Python-based configuration in code.
- **Direct Keyword Arguments**: Perfect for quick tests or small tweaks.

**Tip:**  
- If you’re using `docker`, the CLI approach is typically more convenient.  
- If you’re using `docker-compose`, or prefer a more programmatic setup, consider using the Python interface. For more details on Docker-specific usage, see our [Getting Started with Docker](./GETTING_STARTED_DOCKER.md) guide.

### Using the CLI

1. **Create a `custom.yaml` File:**
   ```yaml
   launch:
     server_port: 8080
   scraibe_params:
     whisper_model: 'large-v3'
   ```

2. **Run the WebUI Using Your Custom Configuration:**
   ```bash
   scraibe-webui start -c custom.yaml
   ```

This approach cleanly separates your configuration into a YAML file, making it easier to maintain and share.

### Using the Python Interface

If you prefer a more programmatic approach or want to integrate ScrAIbe-WebUI into a larger Python application, you can load configurations directly from Python:

```python
from scraibe_webui import App

app = App.load_config("custom_config.yaml")
app.start()
```

### Quick Configuration Without YAML

Sometimes, you might just want to test a setting quickly without creating or editing a YAML file. In that case, you can pass parameters directly via the CLI or Python interface.

**CLI Example Without YAML:**
```bash
scraibe-webui start server_port=8080 whisper_model=large-v3
```

**Python Example Without YAML:**
```python
from scraibe_webui import App

# Using a dictionary:
settings = {
    "launch": {"server_port": 8080},
    "scraibe_params": {"whisper_model": "large-v3"}
}

App(**settings).start()

# Or directly as keyword arguments:
App(server_port=8080, whisper_model="large-v3").start()
```

### Summary of Configuration Approaches

- **YAML File (CLI or Python)**: Best for organized, long-term configurations.
- **Direct CLI Arguments**: Good for quick tests, especially in containerized environments.
- **Python Keyword Arguments or Dictionaries**: Ideal for programmatic integration or when automating tasks.

With these methods, you have flexibility and control over how you configure your WebUI. So far, we’ve covered basic changes to the port and whisper model through both CLI and Python interfaces, ensuring even beginners can get started with customization.

---

At this point, you’ve learned the fundamentals of customizing your ScrAIbe-WebUI using different configuration methods. Next, we’ll explore how to dive deeper into customizing your `config.yaml` file for a more structured and comprehensive setup.

## Customizing Your `config.yaml`

The `config.yaml` file is the heart of your `ScrAIbe-WebUI` customization. This file allows you to define various settings that control how your WebUI behaves and appears. Below, we will dive into the key sections of the `config.yaml` file and explain how to customize each part. You can find the original `config.yaml` file in the repository under [`scraibe_webui/misc/config.yaml`](../scraibe_webui/misc/config.yaml)

### 1. Interface Type

The interface type determines how ScrAIbe-WebUI processes your transcription tasks. There are two interface types available: `simple` and `async`. Each serves different use cases depending on your needs, resources, and preferences. You can configure the interface type in your `config.yaml` like this:

```yaml
interface_type: simple
```

- **`interface_type`**: Choose between `simple` or `async`.

---

#### Detailed Explanation

##### **Simple Interface**
The `simple` interface is ideal for real-time transcription or smaller tasks. This option allows you to upload your file, process it on the page, and get the results with a short waiting time.

- **Best For**:
  - Live transcriptions.
  - Users with a GPU setup to speed up processing.
  - Smaller audio/video files.

- **Advantages**:
  - Quick and straightforward.
  - Doesn’t require additional configurations like email setup.
  - More robust for immediate use cases.

- **Example UI**:
  Below is a screenshot of the simple interface layout:  
  ![Simple Interface](/img/simple_ui.png)

---

##### **Async Interface**
The `async` interface is designed for scenarios where you do not want to keep the browser open while the transcription is being processed. Files are added to a queue and processed asynchronously, with the results delivered to your email once ready.

- **Best For**:
  - Saving resources like CPU usage.
  - Transcribing larger or longer files.
  - Users who prefer not to wait actively for the transcription to complete.

- **How It Works**:
  - You upload your files to the system.
  - The files are queued for processing.
  - Once processing is complete, the transcript is sent to your email.

- **Requirements**:
  - You must configure the email settings in the `config.yaml` file to enable this feature. (Covered in the Email Backend section.)

- **Advantages**:
  - Allows background processing without requiring the browser to remain open.
  - Ideal for larger tasks where immediate results are not necessary.

- **Example UI**:
  Below is a screenshot of the async interface layout:  
  ![Async Interface](/img/async_ui.png)

---

#### Choosing the Right Interface Type

| **Feature**              | **Simple**                   | **Async**                    |
|---------------------------|------------------------------|------------------------------|
| **Setup Complexity**      | Minimal                     | Requires email configuration |
| **Use Case**              | Live transcription, small files | Asynchronous processing, large files |
| **Speed**                 | Faster results              | Background processing        |
| **Resource Efficiency**   | More demanding (CPU/GPU)    | Saves resources              |
| **Robustness**            | More reliable               | Depends on email setup       |

By understanding your specific use case, you can select the interface type that best suits your needs. For example, if you’re working on smaller files with GPU acceleration, the `simple` type is the way to go. On the other hand, if you have longer recordings or prefer to process files without waiting actively, the `async` type is more appropriate.

### 2. Gradio Launch Configuration

The `launch` configuration section in `config.yaml` determines how your ScrAIbe-WebUI instance is served by Gradio. By providing parameters to Gradio’s `launch` function, you influence where and how the interface is hosted, accessed, and secured.

**What You Can Control:**
- **Server Port (`server_port`)**: Choose a specific port to ensure predictable access points, such as `http://localhost:8080`.
- **Server Name (`server_name`)**: Define the network interface that your WebUI binds to, allowing external access (e.g., `"0.0.0.0"`) or restricting it to the local machine only.
- **Authentication (`auth`)**: Set credentials to protect the interface from unauthorized access, making it suitable for private or internal deployments.
- **Additional Parameters**: Options like `inbrowser`, `share`, or SSL configurations can be passed along to Gradio, tailoring the user’s initial experience when the WebUI launches.

**Where to Learn More:**
- Consult the default [`config.yaml`](../scraibe_webui/misc/config.yaml) for examples.
- Detailed parameter explanations are available in the [Gradio Launch Documentation](https://www.gradio.app/docs/gradio/blocks#blocks-launch).
- Always verify that the Gradio documentation matches the version you’ve installed.
- Check the [`requirements.txt`](../requirements.txt) to ensure all necessary dependencies are met.

**Example `config.yaml` Snippet:**
```yaml
launch:
  server_port: 8080
  server_name: "0.0.0.0"
  auth: [my_username, my_passwd]
```

In this example:
- The WebUI is accessible at `http://<your_machine_ip>:8080/`.
- It listens on all network interfaces, allowing LAN-based users to connect.
- Users must log in with the specified credentials.

---

### 3. Gradio Queue Configuration (Simple Interface Only)

The `queue` section configures how incoming requests are queued and processed. **Note that this queueing system is only relevant for the simple (synchronous) interface**. In the simple interface, requests are handled directly through Gradio’s built-in queue functionality, allowing you to manage how many tasks are processed at once and how they line up when the system is busy.

**What You Can Control:**
- **Maximum Queue Size (`max_size`)**: Set how many requests can wait in line. Once the queue is full, new requests might be delayed or turned away, depending on your logic.
- **Ensuring Responsiveness**: By tuning the queue size, you can balance resource usage and user experience. A larger queue can handle more users but may slow down processing; a smaller queue maintains responsiveness but might turn some requests away.

**Important Note:**
- The queue configuration does not apply to the async interface, as the async interface handles job scheduling and parallelization differently.
- For additional details on configuring the queue and other Gradio functionalities, refer to the [Gradio Queue Documentation](https://www.gradio.app/docs/gradio/queue).
- Always ensure that your Gradio documentation version matches the version you have installed.

**Example `config.yaml` Snippet:**
```yaml
queue:
  max_size: 10
```

In this example:
- Up to 10 requests can wait to be processed in the simple interface.
- Adjusting this value allows you to scale the WebUI’s capacity based on your hardware resources and expected user load.

---

When tuning the `launch` and `queue` configurations, remember that these settings primarily pass directly to Gradio. For any advanced configurations or deeper dives into parameters, consult the [Gradio Documentation](hhttps://www.gradio.app/docs/gradio/blocks) to ensure proper implementation and compatibility.  

---

### 4. Layout Configuration

The `layout` section in `config.yaml` focuses on customizing your ScrAIbe-WebUI’s appearance. It allows you to define separate HTML files for the header and footer and inject dynamic content into those templates using `header_format_options` and `footer_format_options`. Importantly, Gradio no longer supports importing external CSS or SVG files, so all styling must be fully contained within the HTML files themselves, and images must be in supported formats like `.png`, `.jpg`, or `.jpeg`.

**What You Can Control:**
- **Header and Footer HTML Files:**  
  Specify your own HTML files for these sections. Each file can include its own inline CSS styles.
- **Dynamic Variables:**  
  Use placeholders in the HTML (e.g., `{header_logo_url}`) that Gradio replaces at runtime with values from `header_format_options` or `footer_format_options`.
- **No External CSS Files or SVGs:**  
  All styling must be inline in the HTML. CSS files cannot be imported, and `.svg` images are no longer supported. Choose standard image formats like `.png`, `.jpg`, or `.jpeg` for your logos and icons.

**Where to Learn More:**
- Check our default [`config.yaml`](../scraibe_webui/misc/config.yaml) for baseline examples.
- If you have advanced layout questions, refer to the [Gradio Documentation](https://www.gradio.app/docs/). However, note that support for external CSS and `.svg` files is no longer provided by Gradio, so you must rely on inline HTML styling and compatible image formats.

**Example `config.yaml` Snippet:**
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

In this example:
- `header.html` and `footer.html` define your layout, with inline styling applied directly in the HTML.
- `header_logo_url` and `header_logo_src` are dynamically inserted into the HTML.
- The `show_settings` option displays a settings panel in the interface if set to `true` (experimental).

---

### Configuration Options in Detail

- **header**:  
  Points to an HTML file that defines your header’s structure. All CSS must be inline.

- **header_format_options**:  
  A dictionary that maps placeholders in the header HTML to their actual values. For example, `{header_logo_url}` in `header.html` could be replaced by `https://www.example.com/`.

  **Example HTML:**
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

  Here:
  - The logo and styles are fully defined inline.
  - The placeholder `{header_logo_url}` is replaced by the URL defined in `header_format_options`.
  - The image path is specified with `/gradio_api/file=`, which Gradio uses to serve the image. Only images can be referenced this way; external CSS files are not supported.

- **footer**:  
  Similarly to the header, points to an HTML file for the footer, which must also contain all of its styling inline.

- **footer_format_options**:  
  Works the same way as `header_format_options`, allowing dynamic insertion of values into the footer template.

- **show_settings**:  
  A Boolean to toggle the settings panel in the interface. This feature remains experimental and may not be suitable for all scenarios.

---

### Updated Important Notes

1. **No External CSS Files**:  
   Gradio no longer supports importing external CSS files. All CSS must be defined inline within your HTML files. This ensures that the entire layout configuration is self-contained.

2. **Only Image Files Are Served**:  
   Images can be referenced with `/gradio_api/file=`. No other file types, including `.css` or `.svg`, are supported. Use common image formats like `.png`, `.jpg`, or `.jpeg`.

3. **SVG Files Not Supported**:  
   If you previously relied on SVGs for icons or logos, switch to `.png`, `.jpg`, or `.jpeg`. Ensure images are appropriately sized and optimized for performance.

---

#### Best Practices

- **Inline All Styles**: Place all necessary CSS in `<style>` tags within the HTML. Since external CSS files are not supported, this keeps your interface portable and predictable.
- **Use Common Image Formats**: Stick to `.png`, `.jpg`, or `.jpeg` for logos and icons.
- **Descriptive Variable Names**: Choose clear keys in `header_format_options` and `footer_format_options` for easier maintenance.
- **Validate Your HTML**: Well-formed HTML helps prevent layout issues.
- **Test Your Layout**: Check the final appearance in different browsers and devices. If issues arise, consult the [Gradio Documentation](https://www.gradio.app/docs/) or community forums for guidance.

---

By adhering to these guidelines and limitations, you can create a visually appealing and fully functional layout. Inline styles and compatible image formats help ensure that your ScrAIbe-WebUI loads smoothly and consistently across various environments.

---

### 5. SCRAIBE Parameters

The `scraibe_params` section defines the core transcription and processing characteristics of ScrAIbe-WebUI. Here, you specify which Whisper model to use, how to handle diarization, which hardware to run on, and other performance-related settings. Adjusting these parameters allows you to optimize for speed, accuracy, or resource constraints.

**Key Considerations:**
- **Model Selection:** Choose a Whisper model that matches your accuracy and latency needs. Smaller models (like `tiny` or `base`) run faster on limited hardware, while larger models (`large-v3`, `large-v3-turbo`) offer better accuracy but require more compute.
- **Backend and Device Management:** Decide whether to use the standard Whisper backend or the faster-whisper alternative, and choose between CPU or GPU (`cuda`) processing depending on your hardware capabilities.
- **Diarization and Authentication:** Enable speaker diarization with pyannote models if needed, and supply authentication tokens for protected model access.

**Example `config.yaml` Snippet:**
```yaml
scraibe_params:
  whisper_model: medium
  whisper_type: whisper
  dia_model: null
  use_auth_token: null
  device: null
  num_threads: 0
```

In this example:
- The `medium` Whisper model is selected, striking a balance between speed and accuracy.
- The standard `whisper` backend is chosen.
- No diarization model is set (`dia_model: null`).
- `use_auth_token: null` means no special authentication is currently required.
- `device: null` and `num_threads: 0` let ScrAIbe-WebUI auto-select the best available resources.

---

### Parameter Details

- **whisper_model**:  
  Defines the exact Whisper model used. Options include:
  - `tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`, `large-v3-turbo`
  
  **Trade-Offs:**  
  - Smaller models (`tiny`, `base`) process audio more quickly but may yield less accurate results.
  - Larger models (`large-v3`, `large-v3-turbo`) achieve higher accuracy, especially for complex or noisy audio, but require more memory and GPU/CPU resources.

- **whisper_type**:  
  Choose `whisper` for the original backend or `faster-whisper` for a potentially more efficient implementation. The `faster-whisper` backend, found at [faster-whisper](https://github.com/SYSTRAN/faster-whisper), may offer speed or optimization benefits, but always test to ensure it meets your quality and performance needs.

- **dia_model**:  
  When set, this parameter enables speaker diarization using a pyannote-based model. By default, it’s `null`, meaning no diarization is performed. If you require identifying and separating different speakers within an audio track, specify a pyannote model path or name. This is a powerful feature for transcribing interviews, meetings, or multi-speaker podcasts.

- **use_auth_token**:  
  Some advanced models, particularly those hosted on Hugging Face, require authentication. If you need access to original pyannote models or other restricted resources, provide your Hugging Face token here. Doing so unlocks the full potential of premium features and ensures compliance with model usage policies.

- **device**:  
  - `cpu`: Ideal for systems without GPUs or when GPU resources are limited.
  - `cuda`: Utilize your GPU for faster processing, assuming you have CUDA-compatible hardware. GPU acceleration can significantly speed up transcription times for larger models or longer audio files.

- **num_threads**:  
  This parameter controls how many CPU threads are allocated to transcription when running on `cpu`. Increasing the number of threads can improve performance on multi-core systems. However, avoid setting it too high, as excessive parallelization can lead to diminishing returns or increased contention for system resources.

**Additional Options:**
- **verbose** or other supported keyword arguments can be passed to the underlying `ScrAIbe` class to provide more detailed logging, debugging information, or fine-grained control over processing behavior.

**Where to Learn More:**
- Refer to the default [`config.yaml`](../scraibe_webui/misc/config.yaml) for baseline settings and additional parameters.
- For details on Whisper models and performance characteristics, consult the official Whisper documentation and community resources.
- The [pyannote documentation](https://github.com/pyannote/pyannote-audio) can provide guidance on selecting and using diarization models.
- For questions on Hugging Face authentication tokens or model access, visit the Hugging Face documentation and platform guidelines.

---

By fine-tuning the `scraibe_params` settings, you can customize the transcription experience to suit your workflow. Whether you need lightning-fast results for simple tasks or highly accurate, speaker-differentiated transcripts for complex projects, these parameters give you the flexibility and control to meet your goals.

### 6. Setting Up the Email Backend for Async Interface

When using the asynchronous (`async`) interface, completed transcripts are not directly displayed in your browser. Instead, they’re processed in the background and delivered to you via email once ready. Configuring the email backend ensures that transcripts, error notifications, and upload confirmations reach you or your users reliably.

**Key Considerations:**
- **SMTP Credentials & Security:**  
  Provide your email service’s SMTP details, including the server address, port, and authentication credentials. Ensure that these credentials are kept secure and private.
- **Encryption & Authentication Methods:**  
  Choose between `SSL`, `TLS`, or `PLAIN` depending on your email provider’s requirements. TLS or SSL is typically recommended for secure email transmission.
- **Templating & Customization:**  
  Customize HTML templates for various notification types: success messages, error reports, and upload confirmations. Insert dynamic fields (like `contact_email` or `exception`) to make messages more informative.
- **Layout & Styling:**  
  While Gradio supports a `mail_css_path` for styling your emails, ensure your CSS is compatible and properly referenced so that recipients see a well-formatted message.

**Note:**  
These settings are only applicable if you’re using the async interface. The simple interface processes requests immediately and does not send emails.

**Example `config.yaml` Snippet:**
```yaml
mail:
  sender_email: null
  smtp_server: null
  smtp_port: 0
  sender_password: null
  connection_type: TLS
  context: default
  default_subject: "SCRAIBE"
  error_template: scraibe_webui/misc/error_notification_template.html
  error_subject: "An error occurred during processing."
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

---

### Parameter Details

- **sender_email**:  
  The email address from which all notifications are sent. Use an address you control and ensure it’s correctly authenticated with your email provider.

- **smtp_server & smtp_port**:  
  Provide your email provider’s SMTP details. Common servers include `smtp.gmail.com` for Gmail, and ports often are `587` (TLS) or `465` (SSL).

- **sender_password**:  
  The account’s password or app-specific password. Handle this securely—avoid committing sensitive credentials to public repositories.

- **connection_type** (`SSL`, `TLS`, or `PLAIN`):  
  Select the encryption/authentication method your SMTP server requires. Most providers recommend TLS or SSL for secure connections.

- **context**:  
  Controls the SSL context for secure email transmission. When set to `default`, it uses `ssl.create_default_context()`. If needed, you can supply a custom `ssl.SSLContext` or pass a dictionary of arguments to configure security further.

- **default_subject**:  
  The fallback subject line used if no other specific subject is provided.

- **error_template & error_subject**:  
  Define an HTML template and subject line for error notifications. The `exception` placeholder is automatically populated with the error details, making it easier to debug issues.

- **error_format_options**:  
  Insert dynamic content like `contact_email` or other fields into the error notification template, allowing you to provide support information or troubleshooting steps.

- **success_template & success_subject**:  
  Specify the HTML template and subject for success notifications, sent when transcripts are ready. Dynamic placeholders (e.g., `company_name`, `contact_email`) personalize these messages.

- **success_format_options**:  
  Similar to error notifications, these key-value pairs populate placeholders in the success template.

- **upload_notification_template & upload_subject**:  
  Configure a template and subject line for upload confirmations, optionally including a `queue_position` to indicate the user’s place in the processing line.

- **upload_notification_format_options**:  
  Customize placeholders for upload notifications. For instance, `queue_position` can reassure users their request is queued and not lost.

- **mail_css_path**:  
  Points to a CSS file for styling email templates. Ensure the CSS is inline-friendly and that your email provider/client supports the styles used.

---

**Demo Template Example:**

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

**YAML Integration:**
```yaml
success_template: scraibe_webui/misc/success_template.html
success_format_options:
  company_name: "My Awesome Company"
  contact_email: support@mail.com
```

In this example:
- The template uses `{{ company_name }}` and `{{ contact_email }}` placeholders.
- The `success_format_options` in YAML provides the values inserted at runtime.

---

### Best Practices for Email Configuration

- **Use Secure Credentials**: Consider using app-specific passwords or OAuth methods supported by your email provider.
- **Test Templates Thoroughly**: Send test emails to ensure formatting, placeholders, and styling appear as intended in common email clients.
- **Monitor Deliverability**: Some SMTP servers or email providers may require additional authentication steps (like `App Passwords` or `2FA`) to ensure emails are delivered reliably and not marked as spam.
- **Consult Documentation**: For advanced customization or troubleshooting, refer to the [Gradio Documentation](https://www.gradio.app/docs/) and your email provider’s SMTP configuration guides.

---

By correctly setting up the email backend, the async interface can notify you (or your users) automatically when transcripts are ready, when uploads are completed, or if errors occur. This streamlined communication ensures a smoother, more efficient workflow without requiring the browser to remain open or the user to wait actively for processing to finish.

---

### 7. Advanced Configuration

The `advanced` section in your `config.yaml` gives you direct control over resource usage and performance tuning for ScrAIbe-WebUI. Adjusting these parameters can help you strike the right balance between responsiveness, throughput, and memory consumption.

**Example `config.yaml` Snippet:**
```yaml
advanced:
  keep_model_alive: false
  concurrent_workers_async: 1
```

**Key Parameters:**

- **keep_model_alive** (Applies to the Simple Interface Only):  
  - **When `true`**: The Whisper model remains in memory continuously.  
    - **What This Means:** Faster subsequent transcriptions since you don’t have to reload the model each time.  
    - **Trade-Off:** Higher ongoing memory usage.  
    - **Concrete Guidance:** Start with `false`. If you find the initial loading delay bothersome, set it to `true` and monitor memory usage. If memory usage becomes an issue, revert to `false`.
  
  - **When `false`**: The model unloads after each transcription.  
    - **Result:** Lower memory consumption, but a short model loading delay before each task.  
    - **Concrete Guidance:** This is the safest default. Only switch to `true` if you frequently run many short tasks and need to eliminate loading delays.

- **concurrent_workers_async** (Applies to the Async Interface Only):  
  - **What It Does:** Determines how many transcription tasks the async interface can process at once.  
  - **Trade-Off:** More concurrent workers can boost throughput, but also increase CPU/GPU usage.  
  - **Concrete Guidance:**  
    - Start with `concurrent_workers_async = 1`.  
    - If you find that tasks are backing up and you have sufficient hardware resources, increment this by 1 and test again.  
    - Continue increasing gradually until you reach an acceptable balance between speed and resource usage. If system performance degrades or resources become strained, dial the number back down.

---

### Summary

With these advanced parameters, you have precise control over ScrAIbe-WebUI’s performance characteristics. By starting with conservative values and incrementally adjusting based on observed behavior, you can tailor the WebUI to your environment without guesswork. Over time, fine-tuning these settings ensures that your transcription tasks run efficiently and meet your productivity goals.

### Need Help or Have Questions?

If you run into issues, have suggestions, or need further assistance, we’re here to help! Don’t hesitate to [open an issue on our GitHub repository](https://github.com/JSchmie/ScrAIbe-WebUI/issues/new/choose). Your input helps us continually improve ScrAIbe-WebUI for everyone.

Happy customizing! 🎉