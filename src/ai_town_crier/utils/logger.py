import os
import logging

def get_logger(name):
    level = os.getenv('LOGGING_LEVEL', 'WARNING').upper()

    level_mapping = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    level = level_mapping.get(level, logging.WARNING)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('file.log')

    c_handler.setLevel(level)
    f_handler.setLevel(level)

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
