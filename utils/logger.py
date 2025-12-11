import json
import logging

def get_logger(name: str):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '{"level":"%(levelname)s","message":"%(message)s","name":"%(name)s"}'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
