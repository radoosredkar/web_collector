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
#            "file": {
#                "class": "logging.handlers.TimedRotatingFileHandler",
#                "formatter": "default",
#                "filename": "/var/log/web_collector/web_collector.log",
#                "when": "midnight",
#                "interval": 1,
#                "backupCount": 5
#            },
        },
        "root": {"level": "INFO", "handlers": ["stdout",]},
    }
)

