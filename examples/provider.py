#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2ip API lookup example

Retrieve provider information for the IP 192.0.2.0
"""

import pprint
from twoip import TwoIP

# If using API key, provide it here
twoip = TwoIP(key = None)

# Run the lookup
provider = twoip.provider(ip = '192.0.2.0')

# Print the retrieved country code
pprint.pprint(provider)

# {'ip': '192.0.2.0',
#  'ip_range_end': '3221226239',
#  'ip_range_start': '3221225984',
#  'mask': '24',
#  'name_ripe': 'Reserved AS',
#  'name_rus': '',
#  'route': '192.0.2.0'}