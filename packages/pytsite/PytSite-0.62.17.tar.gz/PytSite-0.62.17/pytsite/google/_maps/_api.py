"""Geo Functions.
"""
from urllib.parse import quote_plus as _urlquote
from . import _geocoding

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_map_link(lng: float=None, lat: float=None, query: str=None, zoom: int=15) -> str:
    """Get link to th Google map.
    """
    if lat and lng and query:
        return 'https://www.google.com/maps/search/{}/@{},{},{}z'.format(_urlquote(query), lat, lng, zoom)

    if lat and lng and not query:
        return 'https://www.google.com/maps?q={},{}'.format(lat, lng)

    if (not lat or not lng) and query:
        return 'https://www.google.com/maps/search/{}'.format(_urlquote(query), lat, lng)


def code(address: str, **kwargs):
    return _geocoding.GeoCoder().code(address, **kwargs)


def decode(lng: float, lat: float, **kwargs):
    return _geocoding.GeoCoder().decode(lng, lat, **kwargs)
