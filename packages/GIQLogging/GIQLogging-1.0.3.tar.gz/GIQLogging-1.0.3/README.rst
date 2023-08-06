GIQLogging
==========

.. image:: https://travis-ci.org/graphiq-data/GIQLogging.svg?branch=master
    :target: https://travis-ci.org/graphiq-data/GIQLogging

.. image:: https://badge.fury.io/py/giqlogging.svg
    :target: https://badge.fury.io/py/giqlogging

GIQLogging is a lightweight logging initializer to promote standardized log formats across services. It wraps the functionality of ``logging`` with formatting provided by `Exoscale's <https://github.com/exoscale>`_ `python-logstash-formatter <https://github.com/exoscale/python-logstash-formatter>`_.

.. code-block:: python

  import GIQLogging
  logging = GIQLogging.init(logstash_type='servicename',
                            level=GIQLogging.INFO,
                            logpath='/path/to/log/output',
                            logger_name='servicename',
                            extra_fields={'foo': 'bar', 'hello': 'world'})
  logging.info('log message')

Installation
------------

To install GIQLogging, simply:

.. code-block:: bash

  pip install GIQLogging

Assumptions
-----------

- In Graphiq's case, GIQLogging is specifically intended for services to log JSON output to be picked up and visualized using an ELK (Elasticsearch, Logstash & Kibana) stack. As such, we require the ``logstash_type`` value to be set upon initialization. This value is placed as an ``extra_field`` and output to each log entry for later use by Logstash.
- The default ``level`` if one is not provided is ``logging.DEBUG``
- If a ``logpath`` is not provided the log will be directed to ``sys.stdout`
- ``logger_name`` is optional, only necessary if initializing multiple loggers
- ``extra_fields`` are optional

Issues
------

Please submit issues `here <https://github.com/graphiq-data/GIQLogging/issues>`_.
