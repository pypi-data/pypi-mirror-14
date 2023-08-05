"""
Lightweight logstash_formatter logging initializer.
We specifically use the logstash_formatter package to aide with consistency
in log formats across services and applications.

To use:
import GIQLogging

# For debugging and development you might want the output to go to stdout
logging = GIQLogging.init()

# For production you might want level to be INFO and logs to go to a file
logging = GIQLogging.init(level=logging.INFO, logpath='/path/to/file.log')

logging.info('hello world!')
"""

import json
import logging
import sys

from logstash_formatter import LogstashFormatterV1


def init(level=logging.DEBUG, logpath=None, extra_fields=None, logger_name=None):
    """
    Initializes and returns configured LogstashFormatter logger

    :param level: defaulted to DEBUG
    :type level: int
    :param logpath: optional, filepath that the log will be written to, prints to stdout if logpath=None
    :type logpath: str
    :param extra_fields: provide extra fields to be always present in logs
    :type extra_fields: dict
    :param logger_name: name of logger to be configured
    :type logger_name: str
    """
    if logpath:
        handler = logging.FileHandler(logpath)
    else:
        handler = logging.StreamHandler(sys.stdout)

    if extra_fields is None:
        fmt = None
    else:
        if not isinstance(extra_fields, dict):
            raise Exception('extra_fields must be of type dict')
        fmt = json.dumps({'extra': extra_fields})

    handler.setFormatter(LogstashFormatterV1(fmt=fmt))
    handler.setLevel(level)

    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
