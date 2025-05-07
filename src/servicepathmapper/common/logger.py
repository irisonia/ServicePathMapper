import logging
from abc import ABC
from typing import Type


class Logger(ABC):
    _logger = logging.getLogger()
    _logger.setLevel(logging.INFO)

    @classmethod
    def log(cls, message: str, level: int = logging.INFO) -> None:
        cls._logger.log(level, message)

    @classmethod
    def create_console_logger(cls) -> None:
        cls._setup_logging_handler(logging.StreamHandler, logging.ERROR)

    @classmethod
    def create_file_logger(cls, log_file_path: str) -> None:
        cls._setup_logging_handler(
            handler_type=logging.FileHandler,
            level=logging.INFO,
            log_file_path=log_file_path)

    @classmethod
    def _setup_logging_handler(cls,
                               handler_type: Type[logging.Handler],
                               level: int = logging.INFO,
                               log_file_path: str = None) -> None:
        """Sets up a logging handler for the package logger, unless that handler type already exists."""

        if not any(isinstance(h, handler_type) for h in cls._logger.handlers):
            handler = handler_type(log_file_path) if log_file_path is not None else handler_type()
            handler.setLevel(level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            cls._logger.addHandler(handler)
