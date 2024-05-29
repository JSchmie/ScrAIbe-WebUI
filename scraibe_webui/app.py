
from .utils.appconfigloader import AppConfigLoader
from .ui import gradio_Interface

class App(AppConfigLoader):
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
        super(App, self).__init__(config, **kwargs)

    def start(self):
        """
        Launches the Gradio interface for audio transcription.

        Initializes the Gradio web interface with settings from a YAML configuration file
        and/or keyword arguments. The function manages AI models, handling their loading 
        into RAM and unloading after a session or specified timeout.

        Returns:
            None
        """
        print("Starting Gradio Web Interface")

        interface = gradio_Interface(self)
        interface.queue(**self.queue)
        interface.launch(**self.launch)
    
    