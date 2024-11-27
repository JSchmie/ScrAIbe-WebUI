<a id="v0.2.0"></a>
# [v0.2.0](https://github.com/JSchmie/ScrAIbe-WebUI/releases/tag/v0.2.0) - 2024-11-27

<!-- Release notes generated using configuration in .github/release.yml at v0.2.0 -->

## What's Changed
### New Features 🎉
* Added a Feature that the submit Button in both interfaces is only available when a file is available by [@Tryndaron](https://github.com/Tryndaron) in [#51](https://github.com/JSchmie/ScrAIbe-WebUI/pull/51)
* Add ForestOceanTheme: A Light, Vibrant Green Theme Inspired by Nature 🌲 by [@JSchmie](https://github.com/JSchmie) in [#60](https://github.com/JSchmie/ScrAIbe-WebUI/pull/60)
* Update MailService Class with Enhanced Context Handling and Warnings by [@JSchmie](https://github.com/JSchmie) in [#52](https://github.com/JSchmie/ScrAIbe-WebUI/pull/52)
### Bug Fixes 🐛
* Set `server_port` and `server_name` to `null` to enable auto-resolve open ports from Gradio and added latest function variables to Gradio `launch` function.  by [@JSchmie](https://github.com/JSchmie) in [#38](https://github.com/JSchmie/ScrAIbe-WebUI/pull/38)
* changed the logo file format to .png  in order to work with latest gradio version by [@JSchmie](https://github.com/JSchmie) in [#43](https://github.com/JSchmie/ScrAIbe-WebUI/pull/43)
* The Model Configuration now displays the currently selected model as the default. by [@JSchmie](https://github.com/JSchmie) in [#56](https://github.com/JSchmie/ScrAIbe-WebUI/pull/56)
### Dependency Updates 📦
* Update dependencies of `gradio` to `4.43.0`. Removed `numpy` dependencie and updated patch versions of `pandas` and ``tqdm` by [@JSchmie](https://github.com/JSchmie) in [#37](https://github.com/JSchmie/ScrAIbe-WebUI/pull/37)
* Updated Scribe to Version 0.3.0 and Fixed Language Dropdown Bug for FasterWhisper Models by [@JSchmie](https://github.com/JSchmie) in [#39](https://github.com/JSchmie/ScrAIbe-WebUI/pull/39)
### Other Changes 🔧
* fix missing libiomp5.so by upgrading torch base image on dockerfile by [@neohunter](https://github.com/neohunter) in [#30](https://github.com/JSchmie/ScrAIbe-WebUI/pull/30)
* fixed typo in Settings section of UI. Thanks [@friki67](https://github.com/friki67) by [@JSchmie](https://github.com/JSchmie) in [#48](https://github.com/JSchmie/ScrAIbe-WebUI/pull/48)
* Normalize File Paths for SMTP Compatibility by [@JSchmie](https://github.com/JSchmie) in [#49](https://github.com/JSchmie/ScrAIbe-WebUI/pull/49)
* Handle bug where `App()` does not load default config. by [@JSchmie](https://github.com/JSchmie) in [#50](https://github.com/JSchmie/ScrAIbe-WebUI/pull/50)
* fixed gradio Warnings due to value errors. by [@JSchmie](https://github.com/JSchmie) in [#53](https://github.com/JSchmie/ScrAIbe-WebUI/pull/53)
* Add Custom Warnings for Interface Type and Path Handling by [@JSchmie](https://github.com/JSchmie) in [#54](https://github.com/JSchmie/ScrAIbe-WebUI/pull/54)
* Changed default task to transcribe to work with faster-whisper by [@mahenning](https://github.com/mahenning) in [#57](https://github.com/JSchmie/ScrAIbe-WebUI/pull/57)
* Enhance WebUI compatibility by allowing PyTorch device configuration via SCRAIBE_TORCH_DEVICE environment variable by [@JSchmie](https://github.com/JSchmie) in [#59](https://github.com/JSchmie/ScrAIbe-WebUI/pull/59)
* Fix set scraibe webui version config yaml by [@JSchmie](https://github.com/JSchmie) in [#62](https://github.com/JSchmie/ScrAIbe-WebUI/pull/62)
* Use set_threads  from scraibe instead of torch set_num_threads to ensure threads will be set across all models by [@JSchmie](https://github.com/JSchmie) in [#63](https://github.com/JSchmie/ScrAIbe-WebUI/pull/63)
* Fix progress bar incompatibility with Faster-Whisper models in run_scraibe by [@JSchmie](https://github.com/JSchmie) in [#65](https://github.com/JSchmie/ScrAIbe-WebUI/pull/65)

## New Contributors
* [@neohunter](https://github.com/neohunter) made their first contribution in [#30](https://github.com/JSchmie/ScrAIbe-WebUI/pull/30)

**Full Changelog**: https://github.com/JSchmie/ScrAIbe-WebUI/compare/v0.1.1...v0.2.0

[Changes][v0.2.0]


<a id="v0.1.1"></a>
# [Release v0.1.1](https://github.com/JSchmie/ScrAIbe-WebUI/releases/tag/v0.1.1) - 2024-08-30



[Changes][v0.1.1]


<a id="v0.1.0"></a>
# [Release v0.1.0](https://github.com/JSchmie/ScrAIbe-WebUI/releases/tag/v0.1.0) - 2024-05-31

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

[Changes][v0.1.0]


[v0.2.0]: https://github.com/JSchmie/ScrAIbe-WebUI/compare/v0.1.1...v0.2.0
[v0.1.1]: https://github.com/JSchmie/ScrAIbe-WebUI/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/JSchmie/ScrAIbe-WebUI/tree/v0.1.0

<!-- Generated by https://github.com/rhysd/changelog-from-release v3.8.0 -->
