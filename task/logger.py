import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel("INFO")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("\n%(asctime)s - %(levelname)s - %(message)s\n")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


LOGGER = setup_logger()
