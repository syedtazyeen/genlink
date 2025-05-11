import logging
import sys
from app.core.config import get_config

def set_logger():
    """Set up logger"""
    logger = logging.getLogger()
    log_level = get_config().LOG_LEVEL.upper()
    logger.setLevel(log_level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    formatter = logging.Formatter(
        "LOGGER[%(levelname)s]: %(filename)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

logger = set_logger()
