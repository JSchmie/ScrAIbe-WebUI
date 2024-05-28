
from .utils.appconfigloader import AppConfigLoader
from .ui import gradio_Interface

class App:
    def __init__(self, config: str = None, **kwargs):
        """
        Initializes the App class.

        Args:
            config (str): Path to the YAML configuration file. Default settings are used 
                          if not provided.
            **kwargs: Keyword arguments corresponding to the configuration sections. Each 
                      argument should be a dictionary reflecting the structure of its 
                      respective section in `config.yaml`.
        """
        self.config = AppConfigLoader.load_config(config, **kwargs)

    def launch(self):
        """
        Launches the Gradio interface for audio transcription.

        Initializes the Gradio web interface with settings from a YAML configuration file
        and/or keyword arguments. The function manages AI models, handling their loading 
        into RAM and unloading after a session or specified timeout.

        Returns:
            None
        """
        print("Starting Gradio Web Interface")

        interface = gradio_Interface(self.config)
        interface.queue(**self.config.queue)
        interface.launch(**self.config.launch)