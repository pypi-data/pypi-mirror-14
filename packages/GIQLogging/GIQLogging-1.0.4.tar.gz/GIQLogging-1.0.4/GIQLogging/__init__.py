"""
Lightweight logstash_formatter logging initializer.
We specifically use the logstash_formatter package to aide with consistency
in log formats across services and applications.

To use:
import GIQLogging

# For debugging and development you might want the output to go to stdout
logging = GIQLogging.init(logstash_type='servicename')

# For production you might want level to be INFO and logs to go to a file
logging = GIQLogging.init(logstash_type='servicename', level=GIQLogging.INFO, logpath='/path/to/file.log')

logging.info('hello world!')
"""

import json
import logging
import sys

from logstash_formatter import LogstashFormatterV1


# Log level constants imported from logging
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET


def init(logstash_type, level=logging.DEBUG, logpath=None, logger_name=None, extra_fields=None):
    """
    Initializes and returns configured LogstashFormatter logger

    :param logstash_type: required extra field used for logstash configuration to Kafka topic output
    :type logstash_type: str
    :param level: defaulted to DEBUG
    :type level: int
    :param logpath: optional, filepath that the log will be written to, prints to stdout if logpath=None
    :type logpath: str
    :param logger_name: name of logger to be configured
    :type logger_name: str
    :param extra_fields: provide extra fields to be always present in logs
    :type extra_fields: dict
    """
    if logpath:
        handler = logging.FileHandler(logpath)
    else:
        handler = logging.StreamHandler(sys.stdout)

    # since we require that type is declared, it is always defined as an extra field
    fmt = {'extra': {'type': logstash_type}}

    # if additional extra fields are defined they are appended
    if extra_fields:
        if not isinstance(extra_fields, dict):
            raise Exception('extra_fields must be of type dict')
        fmt['extra'].update(extra_fields)

    handler.setFormatter(LogstashFormatterV1(fmt=json.dumps(fmt)))
    handler.setLevel(level)

    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
