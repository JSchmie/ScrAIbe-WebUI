"""
Command-Line Interface (CLI) for the Scraibe class,
allowing for user interaction to transcribe and diarize audio files. 
The function includes arguments for specifying the audio files, model paths,
output formats, and other options necessary for transcription.
"""
import os 
import sys
import subprocess
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from .utils._parsekwargs import ParseKwargs
from .global_var import ROOT_PATH
from .app import app

def cli():
    """
    Command-Line Interface (CLI) for the Scraibe WebUI Interface.
    """

    parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("-c","--config", type=str, default= None,
                        help="Path to the customized config.yaml file.")
    
    parser.add_argument('--server-kwargs', nargs='*', action=ParseKwargs, default={},
                    help='Keyword arguments for the Gradio app. If you do not provide a config file, you can use this to set the server configuration.')

    args = parser.parse_args()
    
    arg_dict = vars(args)
    
    config = arg_dict.pop("config")
    
    app(config, **arg_dict)
    
    
if __name__ == "__main__":
    cli()