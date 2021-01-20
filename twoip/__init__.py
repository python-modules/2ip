#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python API client for 2ip.me

This API client will send requests for various information to 2ip.me and provide a response in either XML or JSON.
"""

# Import logging
import logging
from logging import NullHandler

# Import TwoIP class
from .twoip import TwoIP

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

# Set default logging format
logging.basicConfig(
    format='%(asctime)s,%(msecs)03d %(levelname)-7s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.WARN,
)

" Do nothing if running module directly "
if __name__ == '__main__':
  raise RuntimeError('This module contains functions for use in other modules; do not use it directly.')