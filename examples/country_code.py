#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2ip API lookup example

Retrieve country code for the IP address 192.0.2.0
"""

from twoip import TwoIP

# If using API key, provide it here
twoip = TwoIP(key = None)

# Run the lookup
geo = twoip.geo(ip = '192.0.2.0')

# Print the retrieved country code
print(geo['country_code'])