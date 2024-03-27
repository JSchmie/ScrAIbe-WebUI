from typing import Dict, Any
import scraibe_webui.sync.global_var as gv
from ..utils import AppConfigLoader


class SyncLoader(AppConfigLoader):
    """A class that extends AppConfigLoader to manage mail configuration settings.

    This class provides methods for setting mail configuration settings from the configuration.

    Attributes:
        config (dict): The current configuration settings.
        mail_options (dict): The mail configuration settings.
    """
    def __init__(self, config : Dict[str, Any]):
        """Initializes a new instance of the MailConfig class.

        Args:
            config (dict): The configuration dictionary.
        """
        super(SyncLoader, self).__init__(config)
        
    def set_global_vars_from_config(self) -> None:
        """Sets the global variables from a configuration dictionary.

        Args:
            config (dict): A dictionary containing the parameters for the models. Modify the default parameters in the config.yaml file.

        Returns:
            None
        """
    
        gv.MODELS_PARAMS = self.config.get('models')
        gv.TIMEOUT = self.config.get("advanced").get('timeout')