from typing import Dict, Any
from .utils import AppConfigLoader


class SimpleLoader(AppConfigLoader):
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
        super(SimpleLoader, self).__init__(config)
    
    def set_global_vars_from_config(self) -> None:
        pass