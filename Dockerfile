#pytorch Image
FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# Labels
LABEL maintainer="Jacob Schmieder"
LABEL email="Jacob.Schmieder@dbfz.de"
LABEL version="0.0.0"
# todo text anpassen
LABEL description="Scraibe is a tool for automatic speech recognition and speaker diarization. \
                    It is based on the Hugging Face Transformers library and the Pyannote library. \
                    It is designed to be used with the Whisper model, a lightweight model for automatic \
                    speech recognition and speaker diarization."
LABEL url="https://github.com/JSchmie/ScrAIbe-WebUI"

# Install dependencies
WORKDIR /app
ENV AUTOT_CACHE=/data/models/
ENV GRADIO_SERVER_NAME=0.0.0.0
#Copy all necessary files
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md
COPY scraibe_webui /app/scraibe_webui
COPY pyproject.toml /app/pyproject.toml
COPY LICENSE /app/LICENSE
# header, footer mount in data
COPY run_docker.sh /app/run_docker.sh
RUN chmod +x /app/run_docker.sh
RUN mkdir /data

#Installing all necessary Dependencies and Running the Application with a personalised Hugging-Face-Token
RUN apt update -y && apt upgrade -y && \
    apt install -y libsm6 libxrender1 libfontconfig1 git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN conda update --all && conda install -c conda-forge libsndfile && \ 
    conda clean --all -y

# RUN pip install /app/
RUN pip install --no-cache-dir -r requirements.txt

# RUN python3 -m 'scraibe_webui.cli'
# Expose port
EXPOSE 7860
# Run the application

ENTRYPOINT ["./run_docker.sh"]
