# pytorch Image
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

# Labels
LABEL maintainer="Jacob Schmieder"
LABEL email="Jacob.Schmieder@dbfz.de"
LABEL version="0.0.0"
LABEL description="ScrAIbe-WebUI is a tool for automatic speech recognition and speaker diarization. \
                    It supports a wide range of audio and video file types, integrates multiple transcription models, \
                    and provides advanced features like speaker diarization and custom configuration."
LABEL url="https://github.com/JSchmie/ScrAIbe-WebUI"

# Install dependencies
WORKDIR /app

ENV AUTOT_CACHE=/data/models/
ENV GRADIO_SERVER_NAME=0.0.0.0

# Copy all necessary files
COPY ../README.md /app/src/README.md
COPY ../scraibe_webui /app/src/scraibe_webui
COPY ../pyproject.toml /app/src/pyproject.toml
COPY ../LICENSE /app/src/LICENSE
COPY ../scraibe_webui/misc/config.yaml /app/scraibe_webui/misc/config.yaml

# Copy the entrypoint script
COPY ../docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy and modify config.yaml during build
RUN mkdir -p /data

# Installing all necessary Dependencies and Running the Application with a personalised Hugging-Face-Token
RUN apt update -y && apt upgrade -y && \
    apt install -y libsm6 libxrender1 libfontconfig1 git ffmpeg && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN conda update --all -y && conda install -y -c conda-forge libsndfile && \ 
    conda clean --all -y

RUN --mount=source=../.git,target=.git,type=bind \
    pip install --no-cache-dir ./src

# Expose port
EXPOSE 7860

# Set the entry point
ENTRYPOINT ["/app/entrypoint.sh"]

# Run the application
CMD ["python3", "-m", "scraibe_webui.cli", "start", "-c", "/data/config.yaml"]