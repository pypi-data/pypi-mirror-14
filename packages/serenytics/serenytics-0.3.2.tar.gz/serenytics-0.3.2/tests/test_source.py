import pytest


class TestDataSource(object):

    @pytest.fixture(autouse=True)
    def set_test_client(self, serenytics_client, push_data_source):
        self._client = serenytics_client
        self._data_source = push_data_source

    def test_reload_data(self):
        self._data_source.reload_data([
            {'year': 2015, 'quarter': 'Q1', 'sales': 120},
            {'year': 2015, 'quarter': 'Q2', 'sales': 80},
            {'year': 2015, 'quarter': 'Q4', 'sales': 25},
            {'year': 2014, 'quarter': 'Q2', 'sales': 85},
        ])

        data = self._data_source.get_data()
        assert sorted(data.columns) == ['quarter', 'sales', 'year']
        assert sorted(data.rows) == [[u'Q1', 120, 2015],
                                     [u'Q2', 80, 2015],
                                     [u'Q2', 85, 2014],
                                     [u'Q4', 25, 2015]]

    def test_batch_push_data(self):
        # clear the data source by reloading empty data
        self._data_source.reload_data([])

        self._data_source.batch_push_data([
            {'year': 2015, 'quarter': 'Q2', 'sales': 80},
            {'year': 2015, 'quarter': 'Q4', 'sales': 25},
        ])

        data = self._data_source.get_data()
        assert sorted(data.rows) == [[u'Q2', 80, 2015],
                                     [u'Q4', 25, 2015]]
