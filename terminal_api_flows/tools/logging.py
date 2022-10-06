import logging


def get_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger()
