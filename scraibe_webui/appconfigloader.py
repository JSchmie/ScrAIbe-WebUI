import os
import warnings
from typing import Any, Dict, Optional

import global_var as gv
from configloader import ConfigLoader, CURRENT_PATH
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
        self.config = config
        
        self.set_models_options()
        
        self.set_layout_options()
        
        self.set_global_vars_from_config()
        
        self.launch = self.config.get("launch")
        self.models = self.config.get("models")
        self.advanced = self.config.get("advanced")
        self.queue = self.config.get("queue")
        self.layout = self.config.get("layout")
        
        self.mail_options = self.get_mail_options()
        
    
    def set_global_vars_from_config(self) -> None:
        """Sets the global variables from a configuration dictionary.

        Args:
            config (dict): A dictionary containing the parameters for the models. Modify the default parameters in the config.yaml file.

        Returns:
            None
        """
    
        gv.MODELS_PARAMS = self.config.get('models')
        gv.TIMEOUT = self.config.get("advanced").get('timeout')
        gv.LAYOUT_TYPE = self.config.get("layout").get('type')
            
    
    def set_launch_options(self) -> None:
        """DEPRECATED:  Sets the launch options from a configuration dictionary.

        Args:
            None

        Returns:
            None
        """
        launch_options = self.config.get("launch")
        
        if launch_options.get('auth').pop('auth_enabled'):
            self.config['launch']['auth'] = (launch_options.get('auth').pop('auth_username'),
                                             launch_options.get('auth').pop('auth_password'))
        else:
            self.config['launch']['auth'] = None
    
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
        self.config['layout']['header'] = self.check_and_set_path(self.config['layout'], 'header')
        self.config['layout']['footer'] = self.check_and_set_path(self.config['layout'], 'footer')
        self.config['layout']['logo'] = self.check_and_set_path(self.config['layout'], 'logo')
        
        self.add_to_allowed_paths(self.config['layout']['logo'])
    
    def get_layout(self) -> Dict[str, str]:
        """Gets the layout options from a configuration dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the header and footer layout options.
        """
        if not os.path.exists(self.config['layout']['header']) and \
            self.config['layout']['header'] == "scraibe/app/header.html": 
            
            hname = os.path.join(CURRENT_PATH, "header.html")
            
            header = open(hname).read()
            
        elif not os.path.exists(self.config['layout']['header']) and self.config['layout']['header'] != "scraibe/app/header.html":
            warnings.warn(f"Header file not found: {self.config['layout']['header']} \n" \
                              "fall back to default.")
            
            hname = os.path.join(CURRENT_PATH, "header.html")
            
            header = open(hname).read()
        elif os.path.exists(self.config['layout']['header']):
            header = open(self.config['layout']['header']).read()    
        else:
            warnings.warn(f"Header file not found: {self.config['layout']['header']}")
            header = None
            
              
        if header is not None: 
            if self.config['layout']['logo'] == "scraibe/app/logo.svg":
                header = header.replace("/file=logo.svg", f"/file={os.path.join(CURRENT_PATH, 'logo.svg')}")
            elif self.config['layout']['logo'] != "scraibe/app/logo.svg":
                header = header.replace("/file=logo.svg", f"/file={self.config['layout']['logo']}")
            else:
                warnings.warn(f"Logo file not found: {self.config['layout']['logo']}")
            
        
        if self.config['layout']['footer'] is not None:
            if os.path.exists(self.config['layout']['footer']):
                footer = open(self.config['layout']['footer']).read()
            elif self.config['layout']['footer'] is None:
                footer = None
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
            path = os.path.join(CURRENT_PATH, filename)
            
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
    
    def get_mail_options(self) -> Optional[Dict[str, Any]]:
        """Sets the mail options from a configuration dictionary.

        Args:
            None

        Returns:
            None
        """
        if self.config['layout']['type'] == 'asynchronous':
            Warning("Asynchronous is a Beta feature. Expect some bugs.")
            return self.config['advanced']['mail']
        else:
            return None

    @staticmethod
    def check_and_set_path(config_item: dict, key: str) -> Optional[str]:
        """Check if the file exists at the given path. If not, try with CURRENT_PATH.
        Raise FileNotFoundError if the file still doesn't exist.

        Args:
            config_item (dict): The configuration item.
            key (str): The key to check in the configuration item.

        Returns:
            str: The path to the file if it exists, None otherwise.
        """

        file_path = config_item.get(key)
        if file_path is None:
            return None
        if not os.path.exists(file_path):
            new_path = os.path.join(CURRENT_PATH, file_path)
            if not os.path.exists(new_path):
                warnings.warn(f"{key.capitalize()} file not found: {config_item[key]} \n" \
                              "fall back to default.")
            else:
                config_item[key] = new_path
            
        return config_item[key]
