import logging
import os
from datetime import date, datetime

import requests
from requests.exceptions import RequestException, Timeout, TooManyRedirects


logger = logging.getLogger('api')


class NasapiError(Exception):
    pass


class Nasapi(object):

    base_url = 'api.nasa.gov'

    def __init__(self, resource):
        self.resource = resource

    def dt_to_string(self, dt):
        """
        Convert date and datetime to string
        """
        return datetime.strftime(dt, '%Y-%m-%d')

    def get_resource(self, *args, **kwargs):
        resource = self.resource if not args else self.resource.format(*args)

        url = 'https://{0}/{1}'.format(self.base_url, resource)

        # convert datetime or date in kwargs
        for k, v in kwargs.items():
            if isinstance(v, datetime) or isinstance(v, date):
                kwargs[k] = self.dt_to_string(v)

        kwargs['api_key'] = os.environ['NASA_API_KEY']

        try:
            response = requests.get(url, kwargs)
        except (RequestException, Timeout, TooManyRedirects) as exc:
            logger.critical(exc)
            raise NasapiError('Unable to fetch {0}'.format(url))

        if response.ok:
            try:
                json = response.json()
            except Exception as exc:
                logger.critical(exc)
                raise NasapiError('Invalid Json: {0}'.format(response.content))

            if 'error' in json:
                raise NasapiError(json)

        else:
            raise NasapiError('Not OK - {0} - {1} - {2}'.format(
                url, response.status_code, response.content))

        return json

    @staticmethod
    def string_to_date(s):
        """
        Helper static method to convert string to date instance.
        This is useful to convert datestrings from api calls to python.
        """
        return datetime.strptime(s, '%Y-%m-%d').date()

    @classmethod
    def get_apod(cls, date=None, hd=False):
        """
        Returns Astronomy Picture of the Day

        Args:
            date: date instance (default = today)

            hd: bool if high resolution should be included

        Returns:
            json
        """
        instance = cls('planetary/apod')
        filters = {
            'date': date,
            'hd': hd
        }

        return instance.get_resource(**filters)

    @classmethod
    def get_assets(cls, lat, lon, begin=None, end=None):
        """
        Returns date and ids of flyovers

        Args:
            lat: latitude float
            lon: longitude float
            begin: date instance
            end: date instance

        Returns:
            json
        """
        instance = cls('planetary/earth/assets')

        filters = {
            'lat': lat,
            'lon': lon,
            'begin': begin,
            'end': end,
        }

        return instance.get_resource(**filters)

    @classmethod
    def get_imagery(cls, lat, lon, date=None, dim=None, cloud_score=False):
        """
        Returns satellite image

        Args:
            lat: latitude float
            lon: longitude float
            date: date instance of available date from `get_assets`
            dim: width and height of image in degrees as float
            cloud_score: boolean to calculate the percentage of the image covered by clouds

        Returns:
            json
        """
        instance = cls('planetary/earth/imagery')

        filters = {
            'lat': lat,
            'lon': lon,
            'date': date,
            'dim': dim,
            'cloud_score': cloud_score
        }

        return instance.get_resource(**filters)
