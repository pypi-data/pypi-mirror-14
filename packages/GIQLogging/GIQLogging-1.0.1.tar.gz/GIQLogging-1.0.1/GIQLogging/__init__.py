"""
Lightweight logstash_formatter logging initializer.
We specifically use the logstash_formatter package to aide with consistency
in log formats across services and applications.

To use:
import logging
import GIQLogging

# For debugging and development you might want the output to go to stdout
GIQLogging.init()

# For production you might want level to be INFO and logs to go to a file
GIQLogging.init(level=logging.INFO, logpath='/path/to/file.log')

logging.info('hello world!')
"""

import logging
import sys

from logstash_formatter import LogstashFormatterV1


def init(level=logging.DEBUG, logpath=None):
    """
    Initializes logging based on optional level and logpath
    :param level: optional, defaulted to DEBUG
    :param logpath: optional, filepath that the log will be written to
        prints to stdout if logpath=None
    """
    if logpath:
        handler = logging.FileHandler(logpath)
    else:
        handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(LogstashFormatterV1())
    handler.setLevel(level)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)
