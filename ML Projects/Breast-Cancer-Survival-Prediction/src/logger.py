import logging
from typing import Optional

def get_console_logger(name:Optional[str]='project') -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger