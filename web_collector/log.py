import logging
import logging.handlers
from sys import stdout
from logging.config import dictConfig

formatter = logging.Formatter(
    "[%(asctime)s - %(name)s - %(levelname)s - %(filename)s] %(message)s"
)
#logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s - %(name)s - %(levelname)s - %(filename)s] %(message)s",
            }
        },
        "handlers": {
            "stdout": {"class": "logging.StreamHandler", "formatter": "default"},
            "file": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "default",
                "filename": "/var/log/web_collector/web_collector.log",
                "when": "midnight",
                "interval": 1,
                "backupCount": 5
            },
        },
        "root": {"level": "INFO", "handlers": ["stdout", "file"]},
    }
)

def setStreamHandler(stream=stdout):
    if stream:
        handler = logging.StreamHandler(stream)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def setLoggingFile(fileName):
    fileName = "web_scrapper"  # fixed for now
    handler = logging.handlers.TimedRotatingFileHandler(
        f"/var/log/web_collector/{fileName}.log", when="midnight", interval=1
    )
    handler.setFormatter(formatter)
    handler.suffix = "%Y%m%d"
    logger.addHandler(handler)


def setFlaskLogger(app):
    fileName = "web_scrapper"  # fixed for now
    handler = logging.handlers.TimedRotatingFileHandler(
        f"/var/log/web_collector/{fileName}.log", when="midnight", interval=1
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler.suffix = "%Y%m%d"
    app.logger.addHandler(handler)
