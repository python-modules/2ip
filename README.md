# Python 2ip Module

**2ip** allows you to make requests to the 2ip.me API to retrieve provider/geographic information for IP addresses. Requests are (optionally, on by default) cached to prevent unnecessary API lookups when possible.

## Installation

Install the module from PyPI:

```bash
python3 -m pip install 2ip
```

## Methods

The following methods are available.
### TwoIP (Initialisation)

When initialising the 2ip module the following parameters may be specified:

* *Optional* `key`: The API key to use for lookups. If no API key defined the API lookups will use the rate limited free API.

### geo

The geographic lookup method accepts the following parameters:

* *Required* `ip`: The IP address to lookup.
* *Optional* `format` {**json**,xml}: The output format for the request. `json` will return a dict and `xml` will return a string.
* *Optional* `force` {True,**False**}: Force an API lookup even if there is a cache entry.
* *Optional* `cache` {**True**,False}: Allow the lookup result to be cached.

### provider

The provider lookup method accepts the following parameters:

* *Required* `ip`: The IP address to lookup.
* *Optional* `format` {**json**,xml}: The output format for the request. `json` will return a dict and `xml` will return a string.
* *Optional* `force` {True,**False**}: Force an API lookup even if there is a cache entry.
* *Optional* `cache` {**True**,False}: Allow the lookup result to be cached.

## Examples

Some example scripts are included in the [examples](https://github.com/python-modules/2ip/tree/main/examples) directory.

### Provider API

Retrieve provider information for the IP address `192.0.2.0` as a `dict`:

```python
>>> from twoip import TwoIP
>>> twoip = TwoIP(key = None)
>>> twoip.provider(ip = '192.0.2.0')
{'ip': '192.0.2.0',
 'ip_range_end': '3221226239',
 'ip_range_start': '3221225984',
 'mask': '24',
 'name_ripe': 'Reserved AS',
 'name_rus': '',
 'route': '192.0.2.0'}
```

Retrieve provider information for the IP address `192.0.2.0` as a XML string:

```python
>>> from twoip import TwoIP
>>> twoip = TwoIP(key = None)
>>> twoip.provider(ip = '192.0.2.0', format = 'xml')
'<?xml version="1.0" encoding="UTF-8"?>\n<provider_api><ip>192.0.2.0</ip><name_ripe>Reserved AS</name_ripe><name_rus></name_rus><ip_range_start>3221225984</ip_range_start><ip_range_end>3221226239</ip_range_end><route>192.0.2.0</route><mask>24</mask></provider_api>'
```

### Geographic API

Retrieve geographic information for the IP address `8.8.8.8` as a `dict`:

```python
>>> from twoip import TwoIP
>>> twoip = TwoIP(key = None)
>>> twoip.geo(ip = '8.8.8.8')
{'city': 'Mountain view',
 'country': 'United states of america',
 'country_code': 'US',
 'country_rus': 'США',
 'country_ua': 'США',
 'ip': '8.8.8.8',
 'latitude': '37.405992',
 'longitude': '-122.078515',
 'region': 'California',
 'region_rus': 'Калифорния',
 'region_ua': 'Каліфорнія',
 'time_zone': '-08:00',
 'zip_code': '94043'}
```

Retrieve geographic information for the IP address `8.8.8.8` as a XML string:

```python
>>> from twoip import TwoIP
>>> twoip = TwoIP(key = None)
>>> twoip.geo(ip = '8.8.8.8', format = 'xml')
'<?xml version="1.0" encoding="UTF-8"?>\n<geo_api><ip>8.8.8.8</ip><country_code>US</country_code><country>United states of america</country><country_rus>США</country_rus><country_ua>США</country_ua><region>California</region><region_rus>Калифорния</region_rus><region_ua>Каліфорнія</region_ua><city>Mountain view</city><latitude>37.405992</latitude><longitude>-122.078515</longitude><zip_code>94043</zip_code><time_zone>-08:00</time_zone></geo_api>'
```

## Roadmap/Todo

- [ ] Support for email API
- [ ] Support for MAC address API
- [ ] Support for hosting API
- [x] Option to retrieve data as XML
- [ ] Unit tests
- [x] Deduplicate handler to retrieve information from API
