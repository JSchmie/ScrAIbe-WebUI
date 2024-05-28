"""
Command-Line Interface (CLI) for the Scraibe class,
allowing for user interaction to transcribe and diarize audio files. 
The function includes arguments for specifying the audio files, model paths,
output formats, and other options necessary for transcription.
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from .utils._parsekwargs import ParseKwargs
from .app import app
from ._version import __version__

def start_command(args):
    """
    Function to start the Gradio Web Interface with the given configuration and server arguments.
    """
    config = args.config
    server_kwargs = args.server_kwargs
    app(config, **server_kwargs)

def version_command(args):
    """
    Function to display the version of the CLI.
    """
    print(f"Scraibe WebUI CLI version {__version__}")

def create_parser():
    """
    Create the top-level parser and subparsers.
    """
    parser = ArgumentParser(
        description='Command-Line Interface (CLI) for the Scraibe class, allowing for user interaction to transcribe and diarize audio files.',
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Sub-commands')
    
    # Parser for the "start" command
    parser_start = subparsers.add_parser('start', help='Start the Gradio Web Interface')
    parser_start.add_argument("-c", "--config", type=str, default=None,
                              help="Path to the customized config.yaml file.")
    parser_start.add_argument('--server-kwargs', nargs='*', action=ParseKwargs, default={},
                              help='Keyword arguments for the Gradio app. If you do not provide a config file, you can use this to set the server configuration.')
    parser_start.set_defaults(func=start_command)
    
    # Parser for the "version" command
    parser_version = subparsers.add_parser('version', help='Show the version of the CLI')
    parser_version.set_defaults(func=version_command)
    
    return parser

def cli():
    """
    Main entry point for the CLI.
    """
    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
