import collections
import requests
from .exceptions import *


exception_cls_map = {
    401: NotAuthorisedException,
    403: ForbiddenException,
    404: NotFoundException,
    500: InternalServerError
}

CODES_ACCEPTED = (requests.codes.ok, requests.codes.accepted,
                  requests.codes.created)


class APIClient(object):

    def __init__(self, **kwargs):
        """
        acceptable arguments are listed below
        @param base_url: string: required
        @param api_key: string
        @param auth_header: string: name of header for authentication
        """
        self._base_url = kwargs.get('base_url', None)
        assert self._base_url, "Must pass the base_url"

        self._api_key = kwargs.get('api_key', None)
        self._auth_header_name = kwargs.get('auth_header', None)

        self.headers = self.get_headers(kwargs.get('headers', {}))

    def call(self, resource_path, method='get', data=None,
             params=None):

        url = '/'.join([self._base_url, resource_path])

        method = getattr(requests, method)
        headers = self.headers

        response = method(url, data=data, params=params, headers=headers)
        return self._parse_response(response)

    def get_headers(self, additional_headers):
        """
        returns the headers to be sent along with the request
        override for adding your own list of headers
        """
        headers = {
            'Accept': additional_headers.get('Accept', 'application/json'),
            'Content-Type': 'application/json'
        }

        if self._api_key and self._auth_header_name:
            headers[self._auth_header_name] = self._api_key

        headers.update(additional_headers)

        return headers

    @staticmethod
    def _parse_response(response):
        status_code = response.status_code
        if status_code in CODES_ACCEPTED:

            if APIClient.is_json(response):
                return response.json(object_pairs_hook=collections.OrderedDict)
            else:
                return response.text

        else:
            #Log error message
            if status_code in exception_cls_map:
                execption_cls = exception_cls_map[status_code]
                raise execption_cls(response.json())
            else:
                raise Exception(response.json())

    @staticmethod
    def is_json(response):
        return response.headers['content-type'] == 'application/json'