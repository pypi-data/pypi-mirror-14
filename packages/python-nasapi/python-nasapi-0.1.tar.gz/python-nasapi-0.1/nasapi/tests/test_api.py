import os
from datetime import date, datetime

import mock
import pytest
import requests
from requests.exceptions import RequestException

from nasapi import Nasapi, NasapiError


os.environ['NASA_API_KEY'] = 'testkey'


class TestNasapi(object):

    def setup(self):
        self.api = Nasapi('foo')

        self.response_mock = requests.models.Response()
        self.response_mock.status_code = 200
        self.response_mock._content = b'{"data": []}'

    @mock.patch('requests.get')
    def test_get_resource_requests_exception(self, get_mock):
        get_mock.side_effect = RequestException('Something went wrong')

        with pytest.raises(NasapiError) as exc:
            self.api.get_resource()

        assert 'Unable to fetch' in str(exc)

    @mock.patch('requests.get')
    def test_get_resource_json_exception(self, get_mock):
        response = requests.models.Response()
        response.status_code = 200
        response._content = '{"foo": "bar"}'
        get_mock.return_value = response

        with pytest.raises(NasapiError) as exc:
            self.api.get_resource()

        assert 'Invalid Json' in str(exc)

    @mock.patch('requests.get')
    def test_get_resource_response_not_ok(self, get_mock):
        response = requests.models.Response()
        response.status_code = 404
        response._content = 'Not Found'
        get_mock.return_value = response

        with pytest.raises(NasapiError) as exc:
            self.api.get_resource()

        assert '404 - Not Found' in str(exc)

    @mock.patch('requests.get')
    def test_get_resource_error_msg(self, get_mock):
        response = requests.models.Response()
        response.status_code = 200
        response._content = b'{"error": "test", "message": "test"}'
        get_mock.return_value = response

        with pytest.raises(NasapiError) as exc:
            self.api.get_resource()

        assert "'error': 'test'" in str(exc)
        assert "'message': 'test'" in str(exc)

    @mock.patch('requests.get')
    def test_success_call(self, get_mock):
        get_mock.return_value = self.response_mock

        # no args or kwargs
        api = Nasapi('foo')
        api.get_resource()
        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/foo'
        assert get_mock.call_args[0][1] == {'api_key': 'testkey'}

        # args
        api = Nasapi('foo/{0}')
        api.get_resource(1)
        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/foo/1'
        assert get_mock.call_args[0][1] == {'api_key': 'testkey'}

        # kwargs
        api = Nasapi('foo')
        api.get_resource(key='test')

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/foo'
        assert get_mock.call_args[0][1] == {'key': 'test', 'api_key': 'testkey'}

        # both
        api = Nasapi('foo/{0}')
        api.get_resource(1, key='test')

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/foo/1'
        assert get_mock.call_args[0][1] == {'key': 'test', 'api_key': 'testkey'}

    @mock.patch('requests.get')
    def test_get_apod_default_today(self, get_mock):
        get_mock.return_value = self.response_mock

        Nasapi.get_apod()

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/apod'
        assert get_mock.call_args[0][1] == {'date': None, 'api_key': 'testkey', 'hd': False}

    @mock.patch('requests.get')
    def test_get_apod_specified(self, get_mock):
        get_mock.return_value = self.response_mock

        dt = date(2015, 10, 22)
        Nasapi.get_apod(date=dt, hd=True)

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/apod'
        assert get_mock.call_args[0][1] == {'date': '2015-10-22', 'api_key': 'testkey', 'hd': True}

    @mock.patch('requests.get')
    def test_get_assets_default_today(self, get_mock):
        get_mock.return_value = self.response_mock

        Nasapi.get_assets(52.3, 5.1)

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/earth/assets'
        assert get_mock.call_args[0][1] == {
            'lat': 52.3,
            'lon': 5.1,
            'begin': None,
            'end': None,
            'api_key': 'testkey'
        }

    @mock.patch('requests.get')
    def test_get_assets_specified(self, get_mock):
        get_mock.return_value = self.response_mock

        begin = date(2015, 10, 22)
        end = date(2015, 11, 22)
        Nasapi.get_assets(52.3, 5.1, begin=begin, end=end)

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/earth/assets'
        assert get_mock.call_args[0][1] == {
            'lat': 52.3,
            'lon': 5.1,
            'begin': '2015-10-22',
            'end': '2015-11-22',
            'api_key': 'testkey'
        }

    @mock.patch('requests.get')
    def test_get_imagery_default_today(self, get_mock):
        get_mock.return_value = self.response_mock

        Nasapi.get_imagery(52.3, 5.1)

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/earth/imagery'
        assert get_mock.call_args[0][1] == {
            'lat': 52.3,
            'lon': 5.1,
            'date': None,
            'dim': None,
            'cloud_score': False,
            'api_key': 'testkey'
        }

    @mock.patch('requests.get')
    def test_get_imagery_specified(self, get_mock):
        get_mock.return_value = self.response_mock

        dt = date(2015, 10, 22)
        Nasapi.get_imagery(52.3, 5.1, date=dt, dim=0.05, cloud_score=True)

        assert get_mock.call_args[0][0] == 'https://api.nasa.gov/planetary/earth/imagery'
        assert get_mock.call_args[0][1] == {
            'lat': 52.3,
            'lon': 5.1,
            'date': '2015-10-22',
            'dim': 0.05,
            'cloud_score': True,
            'api_key': 'testkey'
        }

    def test_string_to_date(self):
        assert Nasapi.string_to_date('2012-10-08') == date(2012, 10, 8)

    def test_dt_to_string_date(self):
        instance = Nasapi('foo')
        assert instance.dt_to_string(date(2013, 4, 15)) == '2013-04-15'

    def test_dt_to_string_datetime(self):
        instance = Nasapi('bar')
        assert instance.dt_to_string(datetime(2013, 4, 15, 0, 0, 0)) == '2013-04-15'
