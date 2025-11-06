"""Simple logging helper.

Provides a get_logger(...) function that returns a configured logger with
console output and an optional rotating file handler.

Usage:
    from logger import get_logger
    log = get_logger(__name__, level="INFO", log_file="app.log")
    log.info("hello")
"""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


DEFAULT_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"


def get_logger(name: str = __name__, level: str | int = "INFO", log_file: Optional[str] = None, *, max_bytes: int = 10 * 1024 * 1024, backup_count: int = 5, reconfigure: bool = False) -> logging.Logger:
    """Return a configured logger.

    Args:
        name: Logger name (typically __name__).
        level: Logging level (str or int) — e.g. 'DEBUG' or logging.INFO.
        log_file: Optional path to a file to write logs to (rotating).
        max_bytes: Max bytes per file for rotation.
        backup_count: Number of rotated files to keep.
        reconfigure: If True, remove existing handlers and reconfigure.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Normalize level
    if isinstance(level, str):
        level = logging.getLevelName(level.upper())

    logger.setLevel(level)

    if reconfigure:
        for h in list(logger.handlers):
            logger.removeHandler(h)

    # If there are no handlers, or reconfigure requested, add defaults
    if not logger.handlers:
        fmt = logging.Formatter(DEFAULT_FORMAT)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(fmt)
        logger.addHandler(ch)

        # Optional rotating file handler
        if log_file:
            fh = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
            fh.setLevel(level)
            fh.setFormatter(fmt)
            logger.addHandler(fh)

    return logger


logger = get_logger()