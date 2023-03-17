# -*- coding: utf-8 -*-

"""
Validate the supplied URL is of an expected scheme (HTTP or HTTPS)
"""

from urllib.parse import urlparse, ParseResult

from click import ParamType


class URL(ParamType):
    """
    Validate the supplied data is a URL
    """

    name = "url"

    def convert(self, value, param, ctx) -> str:
        if not isinstance(value, tuple):
            parsed_url: ParseResult = urlparse(value)
            if parsed_url.scheme not in ("http", "https"):
                self.fail(
                    f"invalid URL scheme ({parsed_url.scheme}). Only HTTP(S) URLs are allowed.",
                    param,
                    ctx,
                )
        return value
