import os
import warnings
from typing import Any, Dict
from .configloader import ConfigLoader
from ..global_var import ROOT_PATH
import scraibe_webui.global_var as gv
from .._version import __version__ as scraibe_webui_version
from scraibe.misc import SCRAIBE_TORCH_DEVICE, set_threads

class InterfaceTypeWarning(UserWarning):
    """Custom warning class for invalid interface type."""
    pass

class AppConfigLoader(ConfigLoader):
    """A class that extends ConfigLoader to manage application-specific configuration settings.

    This class provides methods for setting global variables, launch options, and layout options from the configuration.

    Attributes:
        config (dict): The current configuration settings.
        launch (dict): The launch configuration settings.
        models (dict): The models configuration settings.
        advanced (dict): The advanced configuration settings.
        queue (dict): The queue configuration settings.
        layout (dict): The layout configuration settings.
    """
    def __init__(self, config : Dict[str, Any]):
        """Initializes a new instance of the AppConfig class.

        Args:
            config (dict): The configuration dictionary.
        """
        
        super(AppConfigLoader, self).__init__(config)
        
        
        self.set_models_options()

        self.get_layout()
        
        self.interface_type = self.set_interface_type()
        self.launch = self.config.get("launch")
        self.scraibe_params = self.config.get("scraibe_params")
        self.advanced = self.config.get("advanced")
        self.queue = self.config.get("queue")
        self.layout = self.config.get("layout")
        self.mail = self.config.get("mail")
        self.load_mail_templates()
        self.set_advanced_options()
        
        
    def set_models_options(self) -> None:
        """Sets the model options from a configuration dictionary.	
            Here provides the option to set the device for the models.
        """ 
                
        device = self.config.get("scraibe_params").get('device')
        _num_threads = self.config.get("scraibe_params").pop('num_threads') # TODO: find a better approach here since this is hard to debug
        if device is None:
            device = SCRAIBE_TORCH_DEVICE
            
        if device == 'cpu' and _num_threads  is not None:
            set_threads(yaml_threads = _num_threads) # this is a global setting

        self.config['scraibe_params']['device'] = device
        
    def get_layout(self) -> Dict[str, str]:
        """Gets the layout options from a configuration dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the header and footer layout options.
        """
        
        def _check_potential_path(key: str, value: str) -> bool:
            """
            Check if the given key or value contains any potential path-related substring or file extension.

            Args:
                key (str): The key to check.
                value (str): The value to check.

            Returns:
                bool: True if the key contains path-related substrings or the value contains file extensions, otherwise False.
            """
            
            key_contains = ['src', 'file', 'path']
            value_ends_with = ['.html', '.css', '.png', '.jpg', '.jpeg', '.svg']
    
            if value is None:
                return False
            else:
                return (any(substring in key for substring in key_contains) or
                        any(value.endswith(suffix) for suffix in value_ends_with))

        _layout : dict = self.config.get("layout")
        
        self.check_and_set_path('header')
        
        _header = _layout.get("header")
        
        _header_format_options : dict = _layout.get("header_format_options")
        
        for key, value in _header_format_options.items():
            if _check_potential_path(key, value):
                self.check_and_set_path(key)
                self.add_to_allowed_paths(value)
            
            if 'scraibe_webui_version' in key and value is None:   
                _layout["header_format_options"][key] = scraibe_webui_version

        _header_format_options = _layout.get("header_format_options")
        
        self.check_and_set_path("footer")
        
        _footer = _layout.get("footer")
        _footer_format_options : dict = _layout.get("footer_format_options")
        
        for key, value in _footer_format_options.items():
            print(key, value)
            if _check_potential_path(key, value):
                self.check_and_set_path(key)
                self.add_to_allowed_paths(value)

            elif 'scraibe_webui_version' in key and value is None:    
                _layout["footer_format_options"][key] = scraibe_webui_version

        _footer_format_options = _layout.get("footer_format_options")
         
        if _header is not None: 
            
            with open(_header, "r", encoding= 'utf-8') as f:
                header = f.read()
                
            header = header.format(**_header_format_options)

            _layout['header'] = header
            
        if _footer is not None:
            
            with open(_footer, "r", encoding= 'utf-8') as f:
                footer = f.read()
            
            
            footer = footer.format(**_footer_format_options)
            
            
            _layout['footer'] = footer
        
        
        self.config['layout'] = _layout
        
    def add_to_allowed_paths(self, path: str) -> None:
        """Adds a path to the list of allowed paths.

        Args:
            path (str): The path to add.

        Returns:
            None
        """
        allowed_paths = self.config['launch']['allowed_paths']
            
        # If allowed_paths is None, create a new list 
        if allowed_paths is None:
            allowed_paths = []
        elif path in allowed_paths:
            return
    
        # Check if path exists otherwise try with ROOT_PATH
        
        if os.path.exists(path):
            
            if not os.path.isabs(path):
                
                path = os.path.join(ROOT_PATH, path)
                if path in allowed_paths:
                    return
                
        if not os.path.exists(path):
            
            path = os.path.join(ROOT_PATH, path)
            
            if not os.path.exists(path):
                warnings.simplefilter("always", InterfaceTypeWarning)
                warnings.warn(f"Path not found: {path}. Can not add {path} to allowed_paths.",
                              InterfaceTypeWarning, stacklevel=2)
                return
            if path in allowed_paths:
                return 
        
        if path not in allowed_paths:
            allowed_paths.append(path)
            self.config['launch']['allowed_paths'] = allowed_paths
        
    def remove_from_allowed_paths(self, path: str) -> None:
        """Removes a path from the list of allowed paths.

        Args:
            path (str): The path to remove.

        Returns:
            None
        """
        
        allowed_paths = self.config['launch']['allowed_paths']
        
        if allowed_paths is None:
            return
        
        if path in allowed_paths:
            allowed_paths.remove(path)
            self.config['launch']['allowed_paths'] = allowed_paths
    
    def load_mail_templates(self) -> Dict[str, str]:
        """Load the mail templates from the configuration file.
        
        Args:
            None
            
        Returns:
            None
        """
        
        self.check_and_set_path("error_template")
        self.check_and_set_path("upload_notification_template")
        self.check_and_set_path("success_template")
        self.check_and_set_path("mail_css_path")
        
        with open(self.mail.get("error_template"), "r", encoding= 'utf-8') as f:
            error_template = f.read()
        
        with open(self.mail.get("upload_notification_template"), "r", encoding= 'utf-8') as f:
            upload_template = f.read()
        
        with open(self.mail.get("success_template"), "r", encoding= 'utf-8') as f:
            success_template = f.read()
        
        self.mail['error_template'] = error_template
        self.mail['upload_notification_template'] = upload_template
        self.mail['success_template'] = success_template
        
    
    def check_and_set_path(self, key: list[str]) -> str:
        # TODO: I think this is Bullshit and should be removed or refactored
        """Check if the file exists at the given path. If not, try with ROOT_PATH.
        Raise FileNotFoundError if the file still doesn't exist.

        Args:
            config_item (dict): The configuration item.
            key (str): The key to check in the configuration item.

        Returns:
            str: The path to the file if it exists, None otherwise.
        """

        _path = self.get_nested_key(self.config, key)
        
        if _path is None:
            return self.restore_defaults_for_keys(key)
        
        if not os.path.exists(_path):
            # Check if the file exists in the ROOT_PATH
            new_path = os.path.join(ROOT_PATH, _path)
            
            if not os.path.exists(new_path):
                warnings.simplefilter("always", InterfaceTypeWarning)
                warnings.warn(f"{key.capitalize()} file not found: {_path} \n" \
                              "fall back to default.", InterfaceTypeWarning, stacklevel=2)
                self.restore_defaults_for_keys(key)
            else:
                self.update_nested_key(self.config, key, new_path)

    def set_advanced_options(self) -> None:
        """Sets the advanced options from a configuration dictionary.

        Args:
            None

        Returns:
            None
        """
        interface_type = self.interface_type
        
        advanced = self.advanced
        
        if interface_type == "async": 
            gv.MAX_CONCURRENT_MODELS = advanced.get("concurrent_workers_async")
            
            if advanced.get("keep_model_alive") is True:
                warnings.simplefilter("always", InterfaceTypeWarning)
                warnings.warn("The option 'keep_model_alive' is not supported in the async interface. Set to False.",
                              InterfaceTypeWarning, stacklevel=2)
                advanced["keep_model_alive"] = False
    
    def set_interface_type(self):
        """
        Sets or returns the interface type based on the 'interface_type' value from the configuration.

        Retrieves the interface type from the configuration dictionary. If the value is not 
        "simple" or "async", a warning is always raised, and the interface type defaults to "simple".
        The valid options are:
        - "simple": A basic, synchronous interface
        - "async": An asynchronous interface

        Args:
            inplace (bool): If True, sets the interface type as an attribute of the class. 
                            If False, returns the interface type without setting it.

        Returns:
            str: The interface type, if inplace=False.

        Raises:
            Warning: If an invalid interface type is provided.
        """
        
         # Add a custom filter to force this specific warning to always print
        warnings.simplefilter("always", InterfaceTypeWarning)
        
        # Get the value from the config dictionary
        _ui = self.config.get("interface_type", "simple")
        
        # Check if the value is valid
        if _ui not in ["simple", "async"]:
            # Raise the custom warning
            warnings.warn(f"IMPORTANT: Invalid interface type '{_ui}' provided. You can choose between 'simple' and 'async'. Falling back to 'simple'.", 
                          InterfaceTypeWarning, stacklevel=2)
            _ui = "simple"
        
        return _ui
                