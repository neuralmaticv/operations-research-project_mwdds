import logging
from logging.handlers import TimedRotatingFileHandler
import os

LOG_OUTPUT = "../data/log/"

def setup_logging(log_dir: str, log_file_name: str) -> logging.Logger:
    path = os.path.join(LOG_OUTPUT, log_dir)
    os.makedirs(path, exist_ok=True)

    log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    log_handler = TimedRotatingFileHandler(
        filename=os.path.join(path, f"{log_file_name}.log"),
        when="midnight",
        interval=1,
        backupCount=5,
    )
    log_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    return logger
