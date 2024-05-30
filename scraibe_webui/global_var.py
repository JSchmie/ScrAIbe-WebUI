from os.path import dirname, realpath

ROOT_PATH = dirname(realpath(__file__)).split('scraibe_webui')[0]

# Variables for Live Interface
PIPE = None

# Variables for Mail Interface
MAX_CONCURRENT_MODELS: int = 1
NUMBER_OF_QUEUE: int = 0