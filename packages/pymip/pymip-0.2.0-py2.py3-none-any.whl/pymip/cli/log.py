# -*- coding: utf-8 -*-
import logging.handlers

LEVELS = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
TEMPLATE = "[%(asctime)s] %(name)-25s %(levelname)-8s %(message)s"
FORMATTER = logging.Formatter(TEMPLATE)


def file_logging(file_path, level='INFO'):
    """Setup logging using ``FileHandler`` based on current date."""
    handler = logging.handlers.RotatingFileHandler(file_path, backupCount=5)
    handler.setFormatter(FORMATTER)
    handler.setLevel(level)
    return handler


def stream_logging(level='ERROR'):
    """Setup logging to STDERR."""
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def setup_logging(file_path, file_level='INFO', stderr_level='ERROR',
                  root_level='DEBUG'):
    """Configure central logging for the package."""
    # get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(root_level)

    # setup stream logging to STDERR
    console = stream_logging(level=stderr_level)
    root_logger.addHandler(console)

    if file_path:
        file_handler = file_logging(file_path, level=file_level)
        root_logger.addHandler(file_handler)

    return root_logger
