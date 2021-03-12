# Python 2ip Module

**2ip** allows you to make requests to the 2ip.me API to retrieve provider/geographic information for IP addresses. Requests are cached to prevent unnecessary API lookups when possible.

A command line interface, `2ip`, is included. The CLI allows lookups for one or more IP's with the output being returned in a table or CSV.

## Requirements

For an up to date list of requirements, check the [requirements.txt](requirements.txt) file.

* `httpx`: Used to send the requests to the API. The `h2` module will be installed as a dependency to provide HTTP2 support.
* `click`: To provide the command line interface argument parsing, validation, help menu and tab completion.
* `tabulate`: For formatting results into a table.
* `colorlog` (optional, recommended): To provide colored log output.

## Installation

Install the module from PyPI:

```bash
python3 -m pip install 2ip
```

## CLI

For available arguments/options, run the command line interface with the `--help` flag. Example:

```bash
$ 2ip --help
Usage: 2ip [OPTIONS] IP...

  Perform 2ip.me lookups for one or more IP addresses

Options:
  -k, --key TEXT                  The optional API key for 2ip.me
  -kf, --keyfile FILENAME         The optional API key file for 2ip.me
  -t, --type [geo|provider]       The lookup provider/type (geo for geographic
                                  information or provider for provider
                                  information)  [default: geo]

  -o, --output [table|csv]        The output format  [default: table]
  -s, --strict                    Strict mode - any errors will return an
                                  exception  [default: False]

  -h2, --http2                    Enable HTTP2 support for querying API
                                  [default: True]

  -c, --connections INTEGER RANGE
                                  Maximum number of HTTP connections to open
                                  to API  [default: 10]

  -v, --verbose                   Set output verbosity level - specify
                                  multiple times for further debugging

  --help                          Show this message and exit.
```

Basic examples:

* Geo lookup:

```bash
$ 2ip 1.1.1.1
+------------+-------------+--------------------------+
| IP Address |    City     |         Country          |
+------------+-------------+--------------------------+
|  1.1.1.1   | Los angeles | United states of america |
+------------+-------------+--------------------------+
```

* Provider lookup:

```bash
TODO
```

### Auto complete

The shell auto completion file can be generated like this:

```bash
## For bash
_2IP_COMPLETE=source_bash 2ip

## For ZSH
_2IP_COMPLETE=source_zsh 2ip

## For fish
_2IP_COMPLETE=source_fish 2ip
```

To get auto complete for the current shell you can eval the code directly:

```bash
## For bash
eval "$(_2IP_COMPLETE=source_bash 2ip)"
```

## Methods

The following methods are available.

### TwoIP (Initialization)

Initialize the TwoIP module.

**Parameters**:

The following parameters are all optional.

* *str* `key`: The API key to use for lookups. If no API key defined the API lookups will use the rate limited free API. Defaults to `None`.
* *str* `api`: Override the base API url. Defaults to `https://api.2ip.ua`.
* *int* `connections`: The maximum number of concurrent API HTTP connections allowed. Defaults to `10`.
* *bool* `http2`: Enable HTTP2 support.
* *bool* `strict`: If set to `True`, raise an Exception if an invalid IP address is looked up. If set to `False`, the invalid IP's will be skipped. Defaults to `False`.

**Returns**:

An initialized TwoIP object.

**Examples**:

```python
## Import module
>>> from twoip import TwoIP
## Initialize without any parameters accepting all defaults
>>> twoip = TwoIP()
## Initialize with an API key
>>> twoip = TwoIP(key = 'my-api-key-here')
```

### geo

Perform a geographic lookup for one or more IP addresses. For more examples check the [Geo Examples](examples/geo.md) page.

**Parameters**:

*Union[IPv4Address, IPv6Address, str, List[IPv4Address, IPv6Address, str]]* `ip`: One or more IP addresses to lookup.

**Returns**:

A `Geo` object. The `Geo.results` attribute contains a list of all results as `GeoResult` objects.

**Example**:

```python
## Import module
>>> from twoip import TwoIP
## Initialize without any parameters accepting all defaults
>>> twoip = TwoIP()
## Perform geo lookup for IP address 192.0.2.0
>>> twoip.geo('192.0.2.0')
Geo(
    results = [
        GeoResult(
            ip='192.0.2.0', ipaddress=IPv4Address('192.0.2.0'),
            http_code=200, api_response_raw=..., error=None,
            city=None, city_rus=None, region=None, region_rus=None, region_ua=None,
            country_code=None, country=None, country_rus=None, country_ua=None,
            latitude=None, longitude=None, time_zone=None, zip_code=None
        )
    ]
)
## Perform geo lookup for IP addresses 1.1.1.1 and 8.8.8.8
>>> twoip.geo(['1.1.1.1','8.8.8.8'])
Geo(
    results = [
        GeoResult(
            ip='1.1.1.1', ipaddress=IPv4Address('1.1.1.1'),
            http_code=200, api_response_raw=..., error=None,
            city='Los angeles', city_rus='Лос-Анджелес', region='California', region_rus='Калифорния', region_ua='Каліфорнія',
            country_code='US', country='United states of america', country_rus='США', country_ua='США',
            latitude='34.05223', longitude='-118.24368', time_zone='-08:00', zip_code='90001'
        ),
        GeoResult(
            ip='8.8.8.8', ipaddress=IPv4Address('8.8.8.8'),
            http_code=None, api_response_raw=..., error=None,
            city='Mountain view', city_rus=None, region='California', region_rus='Калифорния', region_ua='Каліфорнія',
            country_code='US', country='United states of america', country_rus='США', country_ua='США',
            latitude='37.405992', longitude='-122.078515', time_zone='-08:00', zip_code='94043'
        )
    ]
)
```

## Return Objects

### GeoResult

The `GeoResult` object stores a single lookup result for a Geo request.

For a list of fields/attributes the `describe` method may be called:

```bash
>>> from twoip.datatypes.georesult import GeoResult
>>> from ipaddress import ip_address
>>> print(GeoResult(ipaddress = ip_address('192.0.2.0')).describe())
Field list:
- Field: ip
        - Title: IP Address
        - Description: The IP address that was looked up represented as a string
- Field: ipaddress
        - Description: The IP address that was looked up represented as an ipaddress object
- Field: http_code
        - Title: HTTP Code
        - Description: The HTTP response code from the API
...
```

The following methods can be called on a `GeoResult` object:

* `describe`: Describe a list of all fields
* `distance_to`: Get the difference in kilometers or miles between two IP addresses
* `is_global`: Check if the IP address is globally routable
* `is_private`: Check if the IP address is private

## Examples

For full [examples](https://github.com/python-modules/2ip/tree/main/examples) directory.

## Roadmap/Todo

- [ ] General cleanup of `TwoIP` to remove code duplication
- [ ] Unit testing