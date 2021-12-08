# -*- coding: utf-8 -*-

# pylint: disable=broad-except, invalid-name

"""
Click Parameter Type - URL

This parameter type will ensure the value provided is a valid URL.
"""

from urllib import parse
from click import ParamType

class URLParam(ParamType):
    """Validate the parameter is a valid URL

    Examples:
        'https://google.com' will pass validation
        'fsd4g,d' will fail validation
    """

    name = "URL"

    def convert(self, value: str, param, ctx) -> str:
        """The function which will perform validation or normalization

        Arguments:
            value (str): The URL to validate

        Returns:
            str: The validated URL
        """
        ## Attempt URL validation
        try:
            url = parse.urlparse(value)
        except Exception as e:
            ## Pass the exception to click
            self.fail(
                f'Exception validating "{value!r}" as a valid URL: {e}',
                param,
                ctx,
            )

        ## Make sure the URL is formed correctly
        if not all([url.scheme, url.netloc]):
            if url.path:
                formatted_url = f"{url.scheme}://{url.netloc}{url.path}"
            else:
                formatted_url = f"{url.scheme}://{url.netloc}"
        else:
            self.fail(
                f'URL "{value!r}" is not correctly formed',
                param,
                ctx,
            )

        ## Return formatted url
        return formatted_url
