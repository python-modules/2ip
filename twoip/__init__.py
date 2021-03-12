# -*- coding: utf-8 -*-

"""
Python API client for 2ip.me

This API client will send requests for various information to 2ip.me and provide a response in either XML or JSON.
"""

# Import logging and set null handler
import logging

# Set default logging handler to avoid "No handler found" warnings.
from logging import NullHandler
logging.getLogger(__name__).addHandler(NullHandler())

# Import version info
from .__version__ import __version__

# Load main TwoIP module
from .twoip import TwoIP
