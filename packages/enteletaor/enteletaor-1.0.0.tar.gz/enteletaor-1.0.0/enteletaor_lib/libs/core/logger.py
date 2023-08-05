# -*- coding: utf-8 -*-

import logging
import logging.handlers

from colorlog import ColoredFormatter


# ----------------------------------------------------------------------
def setup_logging():
    """
	Setup initial logging configuration
	"""
    from ...config import __tool_name__, DEBUG_LEVEL

    # Init logger
    logger = logging.getLogger()

    # Set log level
    logger.setLevel(abs(50 - (DEBUG_LEVEL if DEBUG_LEVEL < 5 else 5) * 10))

    # Set file log format
    file_format = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    log_file = logging.FileHandler(filename="%s.log" % __tool_name__)
    log_file.setFormatter(file_format)

    # Handler: console
    formatter = ColoredFormatter(
        "[ %(log_color)s*%(reset)s ] %(blue)s%(message)s",
        # "[ %(log_color)s%(levelname)-8s%(reset)s] %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    log_console = logging.StreamHandler()
    log_console.setFormatter(formatter)

    # --------------------------------------------------------------------------
    # Add all of handlers to logger config
    # --------------------------------------------------------------------------
    logger.addHandler(log_console)
    logger.addHandler(log_file)
