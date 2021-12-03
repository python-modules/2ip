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
