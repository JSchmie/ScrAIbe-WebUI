#pytorch Image
FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

# Labels

LABEL maintainer="Jacob Schmieder"
LABEL email="Jacob.Schmieder@dbfz.de"
LABEL version="0.1.1.dev"
# todo text anpassen
LABEL description="Scraibe is a tool for automatic speech recognition and speaker diarization. \
                    It is based on the Hugging Face Transformers library and the Pyannote library. \
                    It is designed to be used with the Whisper model, a lightweight model for automatic \
                    speech recognition and speaker diarization."
LABEL url="https://github.com/JSchmie/ScrAIbe-WebUI"

# Install dependencies
WORKDIR /app
#Copy all necessary files 
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md
COPY scraibe_webui /app/scraibe_webui
COPY setup.py /app/setup.py
# header, footer mount in data
COPY run_docker.sh /app/run_docker.sh
RUN chmod +x /app/run_docker.sh
RUN mkdir /data

#Installing all necessary Dependencies and Running the Application with a personalised Hugging-Face-Token
RUN apt update && apt-get install -y libsm6 libxrender1 libfontconfig1 git
RUN conda update --all

RUN conda install pip
RUN pip install /app/
RUN conda install -y ffmpeg 
RUN conda install -c conda-forge libsndfile
RUN pip install -r requirements.txt
RUN pip install markupsafe==2.0.1 --force-reinstall

# RUN python3 -m 'scraibe_webui.cli'
# Expose port
EXPOSE 7860
# Run the application

ENTRYPOINT ["python3", "-m",  "scraibe_webui.cli"]