"""_parsekwargs.py
Custom action for argparse to parse keyword arguments for Gradio app configuration.
"""
from argparse import Action

class ParseKwargs(Action):
    """Custom action for argparse to parse keyword arguments for Gradio app configuration.

    This action parses a series of keyword arguments and converts them into a 
    dictionary, which is then used to configure the Gradio application. It 
    supports dynamic types by attempting to evaluate the argument values.

    Attributes:
        dest (str): The name of the attribute to be added to the object returned by parse_args().
    """
    def __call__(self, parser, namespace, values, option_string=None):
        """Parses keyword arguments and updates the namespace with these arguments as a dictionary.

        For each value provided, this method splits the string on the '=' character 
        to separate keys and values, attempting to evaluate the values for Python 
        literals. If evaluation fails, the raw string is used as the value.

        Args:
            parser (ArgumentParser): The ArgumentParser object that called this method.
            namespace (Namespace): An argparse.Namespace object that will be returned by parse_args().
            values (list of str): List of strings, each representing a key-value pair in 'key=value' format.
            option_string (Optional[str]): The option string that was used to invoke this action.

        Raises:
            ValueError: If any string in values does not contain the '=' character, indicating an invalid format.
        """
        
        setattr(namespace, self.dest, dict())
        for value in values:
            if '=' in value:
                key, value = value.split('=')
            try:
                value = eval(value)
            except:
                pass
            if isinstance(value, dict):
                key, value = value.popitem()
                try: 
                    value = eval(value)
                except:
                    pass
            getattr(namespace, self.dest)[key] = value    
  
