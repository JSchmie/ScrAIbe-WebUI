from typing import Any, Dict
import scraibe_webui._async.global_var as gv
from ..utils.appconfigloader import AppConfigLoader

class AsyncLoader(AppConfigLoader):
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
        
        super(AsyncLoader, self).__init__(config)
        
        
    def set_global_vars_from_config(self) -> None:
        """Sets the global variables from a configuration dictionary.

        Args:
            config (dict): A dictionary containing the parameters for the models. Modify the default parameters in the config.yaml file.

        Returns:
            None
        """
    
        gv.MODELS_PARAMS = self.config.get('models')
        gv.TIMEOUT = self.config.get("advanced").get('timeout')
        gv.MAIL_SETTINGS = self.get_mail_options()
    
    def get_mail_options(self) -> Dict[str, Any]:
        """Sets the mail options from a configuration dictionary.

        Args:
            None

        Returns:
            None
        """
        
        if self.config['advanced']['mail']['context_kwargs'] is None:
            self.config['advanced']['mail']['context_kwargs'] = {}
            return self.config['advanced']['mail']
        return self.config['advanced']['mail']
