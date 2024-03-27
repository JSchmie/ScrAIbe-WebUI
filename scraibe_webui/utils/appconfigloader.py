import os
import warnings
from typing import Any, Dict, Optional
from abc import abstractmethod

from .configloader import ConfigLoader
from ._path import ROOT_PATH
from torch import set_num_threads
from torch import device as torch_device
from torch.cuda import is_available

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
        
        self.set_layout_options()
        
        self.set_global_vars_from_config()
        
        self.launch = self.config.get("launch")
        self.models = self.config.get("models")
        self.advanced = self.config.get("advanced")
        self.queue = self.config.get("queue")
        self.layout = self.config.get("layout")
    
    @abstractmethod
    def set_global_vars_from_config(self) -> None:
        """Sets the global variables from a configuration dictionary.

        Args:
            config (dict): A dictionary containing the parameters for the models. Modify the default parameters in the config.yaml file.

        Returns:
            None
        """
        ...
    
    def set_models_options(self) -> None:
        """Sets the model options from a configuration dictionary.	
            Here provides the option to set the device for the models.
        """ 
                
        device = self.config.get("models").get('device')
        if device is None:
            device = torch_device('cuda' if is_available() else 'cpu')
        elif device is not None:
            device  = torch_device(device)
            
        if device == 'cpu' and self.config.get("models").get('num_threads') is not None:
            set_num_threads(self.config.get("models").get('num_threads')) # this is a global setting

        self.config['models']['device'] = device
    
    def set_layout_options(self) -> None:
        """Sets the layout options from a configuration dictionary.

        Args:
            None

        Returns:
            None
        """
        
        self.check_and_set_path('header')
        self.check_and_set_path('footer')
        self.check_and_set_path('logo')
        
        self.add_to_allowed_paths(self.config['layout']['logo'])
    
    def get_layout(self) -> Dict[str, str]:
        """Gets the layout options from a configuration dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the header and footer layout options.
        """
        _header = self.config['layout']['header']
        
        if _header == "misc/header.html":
            _header = os.path.join(ROOT_PATH, _header)
            
            if os.path.exists(_header):
                
                header = open(_header).read()
            else:
                raise FileNotFoundError(f"Header file not found: {_header}")     
            
        elif os.path.exists(_header):
            header = open(_header).read()    
        else:
            warnings.warn(f"Header file not found: {self.config['layout']['header']}")
            header = None
            
              
        if header is not None: 
            _logo = self.config['layout']['logo']
            
            if _logo == "scraibe_webui/misc/logo.svg":
                _logo = os.path.join(ROOT_PATH, _logo)
                
                if os.path.exists(_logo):
                    header = header.replace("/file=logo.svg", f"/file={_logo}")
                else:
                    warnings.warn(f"Logo file not found: {_logo}")
            elif os.path.exists(_logo):
                header = header.replace("/file=logo.svg", f"/file={_logo}")
            else:
                warnings.warn(f"Logo file not found: {self.config['layout']['logo']}")
            
        _footer = self.config['layout']['footer']
        
        if _footer is not None:
            if os.path.exists(_footer):
                footer = open(_footer).read()
            else:    
                warnings.warn(f"Footer file not found: {self.config['layout']['footer']}")
        else:
            footer = None
       
        return {'header' : header ,
                'footer' : footer} 
        
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
    
         # Check if path exists otherwise try with CURRENT_PATH
         
        if not os.path.exists(path):
            filename = os.path.basename(path)
            path = os.path.join(ROOT_PATH, filename)
            
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
    
    def check_and_set_path(self, key: list[str]) -> Optional[str]:
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
                warnings.warn(f"{key.capitalize()} file not found: {_path} \n" \
                              "fall back to default.")
                self.restore_defaults_for_keys(key)
            else:
                self.update_nested_key(self.config, key, new_path)
