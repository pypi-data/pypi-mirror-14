import json

from .helpers import SerenyticsException, make_request
from . import settings


class UnknownDataSource(SerenyticsException):
    def __init__(self, uuid_or_name):
        super(UnknownDataSource, self).__init__(u'Source with uuid or name "{}" does not exist'.format(uuid_or_name))


class DataSource(object):
    """
    Serenytics data source
    """

    def __init__(self, config, headers):
        self._config = config
        self._headers = headers

    def _check_is_push_source(self):
        if self._config['type'] != 'Push':
            raise SerenyticsException('Error: You can only reload the data of a push data source.')

    @property
    def name(self):
        return self._config['name']

    @property
    def uuid(self):
        return self._config['uuid']

    def reload_data(self, new_data):
        """
        Reset data of a Push data source.

        It erases old data and loads new data instead.

        Notes:
            - current data source must be a Push data source
            - new data doesn't have to have the same structure as old data.
        """
        self._check_is_push_source()

        push_url = self._config['jsonContent']['url']
        reload_url = push_url.replace('/push/', '/reload/')
        make_request('post', reload_url, data=json.dumps(new_data), headers={'Content-type': 'application/json'})

    def batch_push_data(self, rows):
        """
        Append several rows of data to current push data source.

        :param rows: list of dict, each dict being a single row of data

        Notes:
            - current data source must be a Push data source
            - new data has to have the same structure as old data.
        """
        self._check_is_push_source()

        push_url = self._config['jsonContent']['url']
        reload_url = push_url.replace('/push/', '/batch_push/')
        make_request('post', reload_url, data=json.dumps(rows), headers={'Content-type': 'application/json'})

    def push_data(self, data):
        """
        Append `data` to current push data source.

        Warning: this call is not blocking and doesn't wait for the data to be imported into serenytics datawarehouse.
        Then you won't have any guarantee that the data has really been imported. If you need a guarantee, at the
        expense of a longer function call, please use method `batch_push_data` and regroup all your rows of data
        in a list.
        """
        self._check_is_push_source()
        push_url = self._config['jsonContent']['url']
        make_request('post', push_url, data=json.dumps(data), headers={'Content-type': 'application/json'})

    def get_data(self, options=None):
        """
        Extract data from the data source
        """
        no_options = options is None

        if no_options:
            options = {
                'format': 'simple_array',
                'only_headers': True
            }

        response = make_request('post', settings.SERENYTICS_API_DOMAIN + '/api/formatted_data/' + self.uuid,
                                data=json.dumps(options),
                                headers=self._headers)

        if not no_options:
            return Data(response.json())

        # make second API call to retrieve actual data
        headers = response.json()['columns_titles']
        new_options = {
            'format': 'simple_array',
            'order': 'row_by_row',
            'data_processing_pipeline': [{
                'select': [header['name'] for header in headers]
            }]
        }
        response = make_request('post', settings.SERENYTICS_API_DOMAIN + '/api/formatted_data/' + self.uuid,
                                data=json.dumps(new_options),
                                headers=self._headers)

        return Data(response.json())


class Data(object):
    """
    Handles data extracted from a data source
    """

    def __init__(self, raw_data):
        self._raw_data = raw_data

    @property
    def headers(self):
        return self._raw_data.get('columns_titles', [])

    @property
    def columns(self):
        return [header['name'] for header in self.headers]

    @property
    def rows(self):
        return self._raw_data.get('data', [])
