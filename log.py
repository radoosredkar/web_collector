import logging
import logging.handlers
from sys import stdout

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def setStreamHandler(stream=stdout):
    if stream:
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def setLoggingFile(fileName):
    fileName = "web_scrapper"# fixed for now
    handler = logging.handlers.TimedRotatingFileHandler(
        f"{fileName}.log", when="midnight", interval=1
    )
    handler.setFormatter(formatter)
    handler.suffix = "%Y%m%d"
    logger.addHandler(handler)
