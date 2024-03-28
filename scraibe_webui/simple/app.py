"""
Gradio App
----------

This module provides an interface to transcribe audio files using the 
Scraibe model. Users can either upload an audio file or record their speech 
live for transcription. The application supports multiple languages and provides 
options to specify the number of speakers and the language of the audio. It also 
enables efficient management of resources by loading and unloading AI models 
based on usage.

The configuration is managed via a 'config.yaml' file, which allows customization
of various aspects of the application, including the Gradio interface, queue
management, and model parameters.

Configuration Sections in 'config.yaml':
- launch: Settings for launching the interface, such as server port, authentication, SSL configuration.
- queue: Configuration for managing request handling and concurrency.
- layout: Customization options for the interface layout, like headers, footers, and logos.
- model: Specifications for different AI models used in transcription.
- advanced: Advanced settings, including session timeout duration.

Note: 
    The .queue function of the Gradio interface is currently experiencing issues 
    and might not work as expected. 

Usage:
    Run this script to start the Gradio web interface for audio transcription.
"""



####
# Gradio Interface
####
from .loader import SimpleLoader
from .interface import gradio_Interface
from ..utils.stg import GradioTranscriptionInterface
import scraibe_webui.simple.global_var as gv


def simple_app(config : str = None, **kwargs):
    """
    Launches the Gradio interface for audio transcription.

    Initializes the Gradio web interface with settings from a YAML configuration file
    and/or keyword arguments. The function manages AI models, handling their loading 
    into RAM and unloading after a session or specified timeout.

    The `kwargs` are used to override or supplement values from the `config.yaml` file.
    They should follow the structure of `config.yaml`, which includes sections like 
    'launch', 'queue', 'layout', 'model', and 'advanced'.

    Args:
        config (str): Path to the YAML configuration file. Default settings are used 
                      if not provided.
        **kwargs: Keyword arguments corresponding to the configuration sections. Each 
                  argument should be a dictionary reflecting the structure of its 
                  respective section in `config.yaml`.

    Returns:
        None
    """

    # Load and override configuration from the YAML file with kwargs
    
    config = SimpleLoader.load_config(config, **kwargs)

    # Set the layout for the Gradio interface
    layout = config.get_layout()

    print("Starting Gradio Web Interface")
    
    # Stup PIPE:
    gv.PIPE = GradioTranscriptionInterface.load_from_dict(config.models)
    
    # Launch the Gradio interface
    
    interface = gradio_Interface(layout)
    interface.queue(**config.queue)
    interface.launch(**config.launch)
  
    
    # # Set the layout for the Gradio interface
    # layout = config.get_layout()
    
    # # start the timer thread
    # timer.start()
    
    # print("Starting Gradio Web Interface")
    
    # # Launch the Gradio interface
    
    # interface = gradio_Interface(layout)
    # interface.queue(**config.queue)
    # interface.launch(**config.launch)

    # # Wait for the timer thread to finish
    # timer.join()
    # gv.MODELS_PROCESS.join()

