from os.path import dirname, realpath

ROOT_PATH = dirname(realpath(__file__)).split('scraibe_webui')[0]

PIPE = None
MAX_CONCURRENT_MODELS: int = 1