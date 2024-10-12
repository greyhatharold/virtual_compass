import logging
import sys
from typing import Optional, Any, Dict

import structlog
from structlog.types import Processor, WrappedLogger

class CustomLogger:
    def __init__(
        self,
        name: str,
        log_level: str = "INFO",
        log_file: Optional[str] = None,
        json_format: bool = False
    ):
        self.name = name
        self.log_level = self._get_log_level(log_level)
        self.log_file = log_file
        self.json_format = json_format

        self._configure_structlog()
        self.logger = self._get_logger()

    @staticmethod
    def _get_log_level(level: str) -> int:
        return getattr(logging, level.upper(), logging.INFO)

    def _configure_structlog(self):
        shared_processors: list[Processor] = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.contextvars.merge_contextvars,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        if self.json_format:
            shared_processors.append(structlog.processors.JSONRenderer())
        else:
            shared_processors.append(
                structlog.dev.ConsoleRenderer(colors=True, exception_formatter=structlog.dev.plain_traceback)
            )

        structlog.configure(
            processors=shared_processors,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )

    def _get_logger(self) -> WrappedLogger:
        logger = structlog.get_logger(self.name)
        logger = logger.bind(logger_name=self.name)

        # Configure handlers
        handlers = [logging.StreamHandler(sys.stdout)]
        if self.log_file:
            handlers.append(logging.FileHandler(self.log_file))

        logging.basicConfig(
            format="%(message)s",
            level=self.log_level,
            handlers=handlers,
        )

        return logger

    def log(self, level: str, event: str, **kwargs: Any):
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(event, **kwargs)

    def debug(self, event: str, **kwargs: Any):
        self.logger.debug(event, **kwargs)

    def info(self, event: str, **kwargs: Any):
        self.logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: Any):
        self.logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs: Any):
        self.logger.error(event, **kwargs)

    def critical(self, event: str, **kwargs: Any):
        self.logger.critical(event, **kwargs)

def get_logger(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    json_format: bool = False
) -> CustomLogger:
    return CustomLogger(name, log_level, log_file, json_format)

# Make sure to export the get_logger function
__all__ = ['get_logger']
