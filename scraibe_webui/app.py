
from .utils.configloader import ConfigLoader


def app(config : str = None, **kwargs):
       # Load and override configuration from the YAML file with kwargs
    
    interface_type = kwargs.get('interface_type', None)

    if not interface_type:
        _config = ConfigLoader.load_config(config, **kwargs)
        
        interface_type = _config.get('interface_type')
        
        if not interface_type:
            raise ValueError("interface_type is not defined in the configuration file."\
                " Please enshure default config.yaml is present or provide a valid configuration file.")


def new_app(config : str = None, **kwargs):
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