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
from .utils._path import ROOT_PATH

def cli():
    """
    Command-Line Interface (CLI) for the Scraibe WebUI Interface.
    """

    parser = ArgumentParser(formatter_class = ArgumentDefaultsHelpFormatter)

    group = parser.add_mutually_exclusive_group()
    
    parser.add_argument("-c","--config", type=str, default= None,
                        help="Path to the customized config.yaml file.")
    
    parser.add_argument('--server-kwargs', nargs='*', action=ParseKwargs, default={},
                    help='Keyword arguments for the Gradio app. If you do not provide a config file, you can use this to set the server configuration.')
    
    group.add_argument('--start-server', action='store_true',
                        help='Start the Gradio app.' \
                        'If set, all other arguments are ignored' \
                        'besides --server-config or --server-kwargs.')

    args = parser.parse_args()
    
    arg_dict = vars(args)
    
    execute_path = os.path.join(ROOT_PATH, "scraibe_webui/app_starter.py")
    
    config = arg_dict.pop("config")
    
    server_kwargs = arg_dict.pop("server_kwargs")
    
    if not config and not server_kwargs:
        subprocess.run([sys.executable, execute_path])
    if not config and server_kwargs:
        subprocess.run([sys.executable, execute_path, f"--server-kwargs={server_kwargs}"])
    elif not server_kwargs and config:
        subprocess.run([sys.executable, execute_path, f"--server-config={config}"])
    else:
        subprocess.run([sys.executable, execute_path, f"--server-config={config}", f"--server-kwargs={server_kwargs}"])

if __name__ == "__main__":
    cli()