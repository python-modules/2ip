# 2IP API - Provider Lookup

The Provider lookup is used to retrieve the ASN that announces an IP and the owner of the address block.

Results are returned as a `ProviderResults` object.

## ProviderResults Properties

The `ProviderResults` object is used to store the results of one or more provider lookups. It has the following properties:

| Name      | Type                   | Description                         |
| --------- | ---------------------- | ----------------------------------- |
| `results` | `list[ProviderResult]` | A list of `ProviderResult` objects. |

### ProviderResult Properties

The `ProviderResult` object stores the results for a single provider lookup. It has the following properties that are retrieved directly from the API:

| Name        | Type  | Default | Description                                       |
| ----------- | ----- | ------- | ------------------------------------------------- | ------------------------------------------------------------------------- |
| `ip`        | `str` |         | The IP address looked up represented as a string. |
| `route`     | `str  | None`   | `None`                                            | The base network address for the IP allocation containing the IP address. |
| `mask`      | `int  | None`   | `None`                                            | The prefix length for the IP allocation containing the IP address.        |
| `name_ripe` | `str  | None`   | `None`                                            | The English name of the provider the IP address is allocated to.          |
| `name_rus`  | `str  | None`   | `None`                                            | The Russian name of the provider the IP address is allocated to.          |
| `site`      | `str  | None`   | `None`                                            | The website for the provider the IP address is allocated to.              |

The following properties are generated from the API response:

| Name             | Type                      | Default      | Description |
| ---------------- | ------------------------- | ------------ | ----------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `ipaddress`      | `IPv4Address              | IPv6Address` |             | The IP address looked up represented as an IPv4 or IPv6 address object.        |
| `asn`            | `int                      | None`        | `None`      | The BGP autonomous system that announces the prefix containing the IP address. |
| `url`            | `urllib.parse.ParseResult | None`        | `None`      | The `site` parsed into a urllib object.                                        |
| `prefix`         | `IPv4Network              | IPv6Network  | None`       | `None`                                                                         | The prefix containing the IP address as an IPv4 or IPv6 network object. |
| `ip_range_start` | `IPv4Address              | IPv6Address  | None`       | `None`                                                                         | The start IP address of the IP allocation.                              |
| `ip_range_end`   | `IPv4Address              | IPv6Address  | None`       | `None`                                                                         | The end IP address of the IP allocation.                                |
