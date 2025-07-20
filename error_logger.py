import logging

def setup_error_logger():
    logger = logging.getLogger('error_logger')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('error_log.txt')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

error_logger = setup_error_logger()