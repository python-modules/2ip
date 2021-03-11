# Changelog

2ip Python module changelog.

## [1.0.0] - Unreleased

This release is a complete rewrite. Major changes include:

- HTTP requests now handled by `httpx` instead of `requests`
- HTTP2 support added
- Asynchronous HTTP requests
- CLI lookups added with `2ip` command
- XML output support removed
- Results are now returned as an object using dataclasses
- More validation for failure cases
- Examples rewritten
- Table and tab output of results

## [0.0.2] - 2020-01-23

- Use HTTP response code to check if the API has been rate limited
- Update setup.py for packaging and testing purposes
- Correct license
- Deduplicate handler for geo/provider API
- Add ability to retrieve data as a dict (default) or as a XML string

## [0.0.1] - 2020-01-20

- Initial release
