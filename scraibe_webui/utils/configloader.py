"""
configloader.py

This module contains two classes, ConfigLoader and AppConfig, which are used to manage application-specific configuration settings.

The ConfigLoader class provides methods for loading a configuration file, applying overrides, and restoring default values for specified keys. It also includes methods for recursively updating nested keys and getting the default configuration.

The AppConfig class extends ConfigLoader and provides additional methods for setting global variables, launch options, and layout options from the configuration. It also includes methods for checking and setting file paths, and getting layout options.

Classes:
    ConfigLoader: Manages application-specific configuration settings.
    AppConfig: Extends ConfigLoader to provide additional methods for managing application-specific configuration settings.
"""
import os
import yaml
from abc import ABCMeta
from typing import Any, Dict, Optional
from ..global_var import ROOT_PATH

class ConfigLoader(metaclass = ABCMeta):
    """A class that extends ConfigLoader to manage application-specific configuration settings.

    This class provides methods for setting global variables, launch options, and layout options from the configuration.

    Attributes:
        config (Dict[str, Any]): The current configuration settings.
        launch (Dict[str, Any]): The launch configuration settings.
        models (Dict[str, Any]): The models configuration settings.
        advanced (Dict[str, Any]): The advanced configuration settings.
        queue (Dict[str, Any]): The queue configuration settings.
        layout (Dict[str, Any]): The layout configuration settings.
    """
    def __init__(self, config: Dict[str, Any]):
        """Initializes a new instance of the ConfigLoader class.

        Args:
            config (dict): The configuration dictionary.
        """
        self.config = config 
        
        self.default_config = self.get_default_config()

        
        
    def restore_defaults_for_keys(self, *args: str):
        """Restores specified keys to their default values, including nested keys.

        Args:
            *args (str): A list of keys or paths to keys (for nested dictionaries) to restore to default values.
                         Each key or path should be a list of keys leading to the desired key.
        """
        
        for key in args:
            self.apply_overrides(self.config, self.default_config, key)
    
    def get(self, key: str):
        """Gets the value of the specified key from the configuration.

        Args:
            key (str): The key to retrieve the value for.

        Returns:
            Any: The value of the specified key, or None if the key is not found.
        """
        return self.get_nested_key(self.config, key)
    
    def set(self, key: str, value: Any):
        """Sets the value of the specified key in the configuration.

        Args:
            key (str): The key to set the value for.
            value (Any): The value to set for the key.
        """
        self.apply_overrides(self.config, {key: value})
        
    @classmethod
    def load_config(cls, yaml_path: Optional[str] = None, **kwargs: Any):
        """Load the configuration file and apply overrides.

        Args:
            yaml_path (str, optional): Path to the YAML file containing overrides.
            **kwargs: Additional overrides as keyword arguments.

        Returns:
            ConfigLoader: A ConfigLoader object with the loaded configuration.
        """
        
        # Load the original configuration    
        config = cls.get_default_config()
    
        # Override with another YAML file if provided
        
        if yaml_path:
            with open(yaml_path, 'r') as file:
                override_config = yaml.safe_load(file)
                if override_config is None:
                    override_config = {}
                cls.apply_overrides(config, override_config)

        # Apply overrides from kwargs
        cls.apply_overrides(config, kwargs)
        return cls(config)
    
    @staticmethod
    def apply_overrides(orig_dict: Dict[str, Any], override_dict: Dict[str, Any], specific: Optional[str] = None):
        """Recursively apply overrides to the configuration, only for specific keys.
        TODO: Maybe think about adding checking for key existence in the original dictionary.
        Args:
            orig_dict (Dict[str, Any]): The original dictionary.
            override_dict (Dict[str, Any]): The override dictionary.
            specific (str, optional): The specific key to override.
        """
        for key, value in override_dict.items():
            if isinstance(value, dict):
                # If the value is a dict, apply recursively
                sub_dict = orig_dict.get(key, {})
                ConfigLoader.apply_overrides(sub_dict, value, specific)
                orig_dict[key] = sub_dict
            else:
                # Apply override for this key
                if specific is None:
                    # If no specific keys are provided, update the key  
                    # If the value is not a dict, search for the key and update
                    if ConfigLoader.update_nested_key(orig_dict, key, value):
                        continue  # Key was found and updated
                    orig_dict[key] = value  # Key not found, update at this level
                
                elif key in specific:
                    # If specific keys are provided, only update if the key is in the list
                    if ConfigLoader.update_nested_key(orig_dict, specific, value):
                        continue  # Key was found and updated
                    orig_dict[specific] = value

    @staticmethod
    def update_nested_key(d, key, value):
        """Recursively search and update the key in nested dictionary.

        Args:
            d (Dict[str, Any]): The dictionary.
            key (str): The key to update.
            value (Any): The new value.

        Returns:
            bool: True if the key was found and updated, False otherwise.
        """
        if key in d:
            d[key] = value
            return True
        for _ , v in d.items():
            if isinstance(v, dict) and ConfigLoader.update_nested_key(v, key, value):
                return True
        return False
    
    @staticmethod
    def get_nested_key(d, key):
        """Recursively search and get the key in nested dictionary.

        Args:
            d (Dict[str, Any]): The dictionary.
            key (str): The key to get.

        Returns:
            Any: The value of the key if found, None otherwise.
        """
        
        if key in d:
            return d[key]
        
        for _ , v in d.items():
            if isinstance(v, dict):
                result = ConfigLoader.get_nested_key(v, key)
                if result is not None:
                    return result
        return None
    
    @staticmethod
    def check_key_in_dict(d, key):
        """Recursively search for the key in the dictionary.

        Args:
            d (Dict[str, Any]): The dictionary.
            key (str): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if key in d:
            return True
        for _ , v in d.items():
            if isinstance(v, dict) and ConfigLoader.check_key_in_dict(v, key):
                return True
        return False
    
    @staticmethod
    def get_default_config():
        """Return the default configuration.

        Returns:
            Dict[str, Any]: The default configuration.
        """
        with open(os.path.join(ROOT_PATH, "scraibe_webui/misc/config.yaml") , 'r') as file:
            config = yaml.safe_load(file)
        return config
