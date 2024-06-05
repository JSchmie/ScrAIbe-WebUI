# Changelog

## [0.1.0] - 2024-05-31

We are finally here launching our new ScrAIbe-WebUI! 🎉

### Features 🌟

- **User-Friendly Interface**: Leveraging Gradio, ScrAIbe-WebUI provides an intuitive web interface that makes it easy for users to interact with the transcription services without any coding requirement.
- **Synchronous Transcription** 🕒: Perfect for live applications, this mode allows users to perform real-time transcriptions, enabling instant text output as audio is being spoken.
- **Asynchronous Transcription** 📨: Designed for asynchronous processing, allowing users to upload audio or video files using the WebUI, which are automatically transcribed, with results sent back via email including file attachment.
- **Broad File Format Compatibility** 🎥🎙: Supports a wide range of audio and video file types compatible with [FFmpeg](https://ffmpeg.org/), ensuring flexibility in handling media from various sources.
- **Direct Input Options** 📹: Users can directly utilize their webcam or microphone to record audio or video for transcription.
- **Multiple Transcription Models** 🌍: Users can select from all available [Whisper](https://github.com/openai/whisper) models, accommodating multiple languages to suit global needs. Includes support for [WhisperX](https://github.com/m-bain/whisperX), providing quantized models for faster performance on CPU.
- **Speaker Diarization** 🗣: Integrates with [Pyannote](https://github.com/pyannote/pyannote-audio), an advanced tool for speaker diarization, ensuring accurate and clear attribution of speech to individual speakers.
- **Custom Configuration** ⚙️: Users can fine-tune settings and preferences via a `config.yaml` file, allowing detailed customization of the application's behavior, including custom headers, footers, and other UI elements.
- **CLI Support** 🖥: Includes a powerful command line interface, enabling scripting and automation of transcription tasks.
- **Docker Compatibility** 🐳: Easy and consistent deployment using Docker. ScrAIbe-WebUI can run in a containerized environment, ensuring smooth operation across different systems.
- **Docker Compose Support** 📦: Manage multi-container Docker applications with ease using Docker Compose.
- **GPL-3.0 License** 📜: ScrAIbe-WebUI is open source and licensed under the GPL-3.0 license, promoting collaboration and development within the community.

### Getting Started 🚀

- **Installation Methods**:
  - **Docker** 🐳: The simplest and most efficient way to deploy ScrAIbe-WebUI. [Get Started with Docker](./docs/GETTING_STARTED_DOCKER.md)
  - **PyPI Package** 📦: Install ScrAIbe-WebUI via pip for seamless integration with your Python environment. [Learn How to Install via PyPI](./docs/GETTING_STARTED.md#pypi-package)
  - **Build from Scratch** 🔧: For those who like to get their hands dirty, build ScrAIbe-WebUI from the ground up. [See the Step-by-Step Guide](./docs/GETTING_STARTED.md#build-from-scratch)

- **Detailed Guides**: For step-by-step instructions on each installation method, refer to our comprehensive [Getting Started Guide](./docs/GETTING_STARTED.md).
- **Recommended Method**: For the easiest and quickest setup, we highly recommend using Docker. [Check out our Docker Guide](./docs/GETTING_STARTED_DOCKER.md)

### Advanced Setup 🛠

For customization and extending the functionality of ScrAIbe-WebUI, our [Advanced Setup Tutorial](./docs/Customize.md) provides all the details you need.

### Contributions 🤝

We warmly welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for more information.

### License 📜

ScrAIbe-WebUI is proudly open source and licensed under the GPL-3.0 license. For more details, see the [LICENSE](./LICENSE) file in this repository.

---

Join us in making ScrAIbe-WebUI even better! 🚀
