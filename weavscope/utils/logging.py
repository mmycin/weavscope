"""
WeavScope logging — thin wrapper around the stdlib logging module.

Consumers can configure the root logger however they like. WeavScope
uses its own namespace ("weavscope.*") so log output can be filtered
independently from the rest of the application.

Usage
-----
from weavscope.utils.logging import get_logger
logger = get_logger(__name__)
logger.info("hello")
"""

import logging
import sys

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

_root = logging.getLogger("weavscope")
if not _root.handlers:
    _root.addHandler(_handler)
_root.setLevel(logging.DEBUG)
_root.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Returns a child logger under the 'weavscope' namespace.

    Args:
        name: Typically __name__ from the calling module.

    Returns:
        A configured logging.Logger.
    """
    return logging.getLogger(name)


def set_level(level: int) -> None:
    """
    Adjust the logging level for all WeavScope loggers.

    Args:
        level: A logging constant such as logging.DEBUG or logging.WARNING.
    """
    _root.setLevel(level)