import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_OUTPUT = os.environ.get("..data/log")

def setup_logging(log_dir):
    path = os.path.join(LOG_OUTPUT, log_dir)
    os.makedirs(path, exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    log_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, "main.log"),
        when="midnight",
        interval=1,
        backupCount=5,
    )
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
