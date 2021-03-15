# -*- coding: utf-8 -*-

# Import core modules
import logging
from pprint import pformat
from typing import Optional, Union, Literal, List

# Import data types to store results
from .datatypes.geo import Geo
from .datatypes.georesult import GeoResult
from .datatypes.provider import Provider
from .datatypes.providerresult import ProviderResult

# Import version info to add to HTTP headers
from .__version__ import __version__

# Get logger
log = logging.getLogger('twoip')

class Parser(object):
    """
    Parse 2ip API responses
    """

    def __parse_results(self, results: List[dict], lookup_type: str) -> Union[Geo, Provider]:

        ## Logging
        log.debug('Parsing list of results')

        ## Create empty list of parsed results
        parsed = []

        ## Check lookup type
        if lookup_type == 'geo':

            ## Loop over each result
            for result in results:

                ## Logging
                log.debug(f'Parsing geo result for IP address "{result["ip"]}"')

                ## Parse the result and add to parsed list
                parsed.append(self.__parse_geo_result(result = result))

            ## Generate the parent dataclass from results
            parent = Geo(results = parsed)

        elif lookup_type == 'provider':

            ## Loop over each result
            for result in results:

                ## Logging
                log.debug(f'Parsing provider result for IP address "{result["ip"]}"')

                ## Parse the result and add to parsed list
                parsed.append(self.__parse_provider_result(result = result))

            ## Generate the parent dataclass from results
            parent = Provider(results = parsed)

        else:
            raise ValueError(f'Lookup parser for lookup type {lookup_type} does not exist')

        ## Return the parent object
        return parent

    @staticmethod
    def __parse_geo_result(result: dict) -> GeoResult:
        ## Logging
        log.trace(f'Geo result to parse:\n{pformat(result)}')

        ## Check if the response resulted in an error; if so shortcut processing
        if 'error' in result:
            log.trace(f'Geo result for IP address "{result["ip"]}" cannot be parsed due to error: {result["error"]}')
            return GeoResult(ipaddress = result["ip"], error = result['error'])

        ## Get response
        response = result['response']

        ## Make sure there is a response body
        try:
            response_text = response.text
        except Exception:
            log.error(f'Geo result for IP address "{result["ip"]}" cannot be parsed due to missing response body')
            return GeoResult(ipaddress = result["ip"], error = 'No response body in API response')

        ## Make sure there is a status code
        try:
            status_code = response.status_code
        except Exception:
            log.error(f'Geo result for IP address "{result["ip"]}" cannot be parsed due to missing status code')
            return GeoResult(ipaddress = result['ip'], error = 'No HTTP response code', api_response_raw = response_text)

        ## Check the status code of response
        if status_code != 200:
            ## If the API was rate limited, format error nicely
            if status_code == 429:
                log.error(f'Geo result for IP address "{result["ip"]}" hit API rate limit; try again later')
                return GeoResult(ipaddress = result['ip'], error = 'Rate limit exceeded',
                    api_response_raw = response_text, http_code = 429)
            ### Otherwise provide raw data
            else:
                log.error(f'Geo result for IP address "{result["ip"]}" resulted in unexpected HTTP response code {status_code}')
                return GeoResult(ipaddress = result['ip'], error = 'Unexpected HTTP response code',
                    api_response_raw = response_text, http_code = status_code)

        ## Parse response as JSON
        try:
            json = response.json()
        except Exception as e:
            log.error(f'Could not parse API response as JSON:\n{e}')
            return GeoResult(ipaddress = result['ip'], error = 'Could not parse API response as JSON',
                    api_response_raw = response_text, http_code = status_code)
        else:
            log.trace(f'Parsed API response as JSON:\n{pformat(json)}')

        ## Set dict values that we want to extract from JSON response
        field_filter: List[str] = ['country_code', 'country', 'country_rus', 'country_ua',
                                'region', 'region_rus', 'region_ua', 'city', 'city_rus',
                                'latitude', 'longitude', 'zip_code', 'time_zone']

        ## Get the values that we want from the JSON response
        log.trace(f'Retrieving the following fields from API data:\n{pformat(field_filter)}')
        extracted = {k: json.get(k, None) for k in field_filter}

        ## Set list of dict values that are equivilent in API response to None
        empty = ['-', 'Неизвестно', 'Невідомо']

        ## Set any fields that cannot be retrieved to None
        log.trace(f'Removing any API fields that match filter:\n{pformat(empty)}')
        filtered = dict(filter(lambda d: d[1] not in empty, extracted.items()))

        ## Create the GeoResult object
        log.trace(f'Creating GeoResult object from data:\n{pformat(filtered)}')
        try:
            georesult = GeoResult(ipaddress = result['ip'], api_response_raw = response_text,
                            http_code = status_code, **filtered)
        except Exception as e:
            log.error(f'Exception creating GeoResult object from API response:\n{e}')
            return GeoResult(ipaddress = result['ip'], error = e,
                    api_response_raw = response_text, http_code = status_code)

        ## Finally return the object
        return georesult

    @staticmethod
    def __parse_provider_result(result: dict) -> GeoResult:
        ## Logging
        log.trace(f'Provider result to parse:\n{pformat(result)}')

        ## Check if the response resulted in an error; if so shortcut processing
        if 'error' in result:
            log.trace(f'Provider result for IP address "{result["ip"]}" cannot be parsed due to error: {result["error"]}')
            return ProviderResult(ipaddress = result["ip"], error = result['error'])

        ## Get response
        response = result['response']

        ## Make sure there is a response body
        try:
            response_text = response.text
        except Exception:
            log.error(f'Provider result for IP address "{result["ip"]}" cannot be parsed due to missing response body')
            return ProviderResult(ipaddress = result["ip"], error = 'No response body in API response')

        ## Make sure there is a status code
        try:
            status_code = response.status_code
        except Exception:
            log.error(f'Provider result for IP address "{result["ip"]}" cannot be parsed due to missing status code')
            return ProviderResult(ipaddress = result['ip'], error = 'No HTTP response code', api_response_raw = response_text)

        ## Check the status code of response
        if status_code != 200:
            ## If the API was rate limited, format error nicely
            if status_code == 429:
                log.error(f'Provider result for IP address "{result["ip"]}" hit API rate limit; try again later')
                return ProviderResult(ipaddress = result['ip'], error = 'Rate limit exceeded',
                    api_response_raw = response_text, http_code = 429)
            ### Otherwise provide raw data
            else:
                log.error(f'Provider result for IP address "{result["ip"]}" resulted in unexpected HTTP response code {status_code}')
                return ProviderResult(ipaddress = result['ip'], error = 'Unexpected HTTP response code',
                    api_response_raw = response_text, http_code = status_code)

        ## Parse response as JSON
        try:
            json = response.json()
        except Exception as e:
            log.error(f'Could not parse API response as JSON:\n{e}')
            return ProviderResult(ipaddress = result['ip'], error = 'Could not parse API response as JSON',
                    api_response_raw = response_text, http_code = status_code)
        else:
            log.trace(f'Parsed API response as JSON:\n{pformat(json)}')

        ## Set dict values that we want to extract from JSON response
        field_filter: List[str] = ['name_ripe', 'name_rus', 'site', 'as', 'ip_range_start',
                        'ip_range_end', 'route', 'mask']

        ## Get the values that we want from the JSON response
        log.trace(f'Retrieving the following fields from API data:\n{pformat(field_filter)}')
        extracted = {k: json.get(k, None) for k in field_filter}

        ## Set list of dict values that are equivilent in API response to None
        empty = ['-']

        ## Set any fields that cannot be retrieved to None
        log.trace(f'Removing any API fields that match filter:\n{pformat(empty)}')
        filtered = dict(filter(lambda d: d[1] not in empty, extracted.items()))

