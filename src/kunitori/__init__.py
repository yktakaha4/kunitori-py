__version__ = "0.1.0"

import json
from logging import config, getLogger
from os.path import dirname, join

config_path = join(dirname(__file__), "config", "logging.json")
logger = getLogger(__name__)

with open(config_path) as f:
    logging_config = json.load(f)
    config.dictConfig(logging_config)

logger.info("init complete.")
