import logging

import requests


HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_412_PRECONDITION_FAILED = 412
HTTP_429_TOO_MANY_REQUESTS = 429


def make_request(method, url,
                 custom_exceptions=None,
                 expected_status_code=HTTP_200_OK,
                 **kwargs):
    response = requests.request(method, url, **kwargs)
    logging.debug('{method} {url} {code}'.format(method=method.upper(),
                                                 url=url,
                                                 code=response.status_code))

    if custom_exceptions is not None and response.status_code in custom_exceptions:
        raise custom_exceptions[response.status_code]

    if response.status_code == HTTP_401_UNAUTHORIZED:
        raise SerenyticsException('Unauthorized: please check your API key and retry')

    if response.status_code != expected_status_code:
        logging.debug('response: %s' % response.text)
        try:
            errors = response.json()['errors']
        except:
            raise SerenyticsException('Error while calling Serenytics API. Please retry or contact support.')
        else:
            raise SerenyticsException(errors[0])

    return response


class SerenyticsException(Exception):
    """Exception launched by Serenytics Client when an error occured."""
