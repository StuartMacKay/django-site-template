import logging

from django.conf import settings

import structlog
from celery.signals import setup_logging  # type: ignore


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # noqa
    logging.config.dictConfig(settings.LOGGING)  # type: ignore

    # noinspection DuplicatedCode
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,  # type: ignore
        cache_logger_on_first_use=True,
    )
