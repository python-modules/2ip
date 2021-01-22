#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2ip API lookup example

Retrieve geographic information for the IP address 192.0.2.0
"""

import pprint
from twoip import TwoIP

# If using API key, provide it here
twoip = TwoIP(key = None)

# Run the lookup
geo = twoip.geo(ip = '192.0.2.0')

# Print the retrieved country code
pprint.pprint(geo)

# {'city': '-',
#  'city_rus': 'Неизвестно',
#  'city_ua': 'Невідомо',
#  'country': '-',
#  'country_code': '-',
#  'country_rus': 'Неизвестно',
#  'country_ua': 'Невідомо',
#  'ip': '192.0.2.0',
#  'region': '-',
#  'region_rus': 'Неизвестно',
#  'region_ua': 'Невідомо',
#  'time_zone': '-',
#  'zip_code': '-'}