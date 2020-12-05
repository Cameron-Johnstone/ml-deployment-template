import logging

from fastapi.logger import logger


handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d %(name)s - %(levelname)s : %(message)s',
    datefmt='%d-%b-%Y %H:%M:%S'
))
logger.addHandler(handler)


def get_logger(level=logging.DEBUG):    
    logger.setLevel(level)

    return logger
