
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
            
    if interface_type == "simple":
        from .simple.app import simple_app
        
        simple_app(config, **kwargs)
    
    elif interface_type == "simple_de":
        from .simple_de.app import simple_de_app
        
        simple_de_app(config, **kwargs)
        
    elif interface_type == "sync":
        from .sync.app import sync_app
        
        sync_app(config, **kwargs)
        
    elif interface_type == "async":
        from ._async.app import async_app
        
        async_app(config, **kwargs)
