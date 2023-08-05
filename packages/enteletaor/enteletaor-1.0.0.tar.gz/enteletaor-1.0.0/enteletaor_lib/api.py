# -*- coding: utf-8 -*-

"""
This file contains API calls and Data
"""

import six
import logging

from .data import *

__all__ = ["run_console", "run", "GlobalParameters"]

log = logging.getLogger()


# --------------------------------------------------------------------------
#
# Command line options
#
# --------------------------------------------------------------------------
def run_console(config):
    """
    :param config: GlobalParameters option instance
    :type config: `GlobalParameters`

    :raises: TypeError
    """
    if not isinstance(config, GlobalExecutionParameters):
        raise TypeError("Expected GlobalParameters, got '%s' instead" % type(config))

    logging.error("Starting Enteletaor execution")
    run(config)
    logging.error("Done!")


# ----------------------------------------------------------------------
#
# API call
#
# ----------------------------------------------------------------------
def run(config):
    """
    :param config: GlobalParameters option instance
    :type config: `GlobalParameters`

    :raises: TypeError
    """
    if not isinstance(config, GlobalExecutionParameters):
        raise TypeError("Expected GlobalParameters, got '%s' instead" % type(config))

    from .libs.core.structs import AppSettings

    # Run modules
    AppSettings.modules[config.action]().run(config)
