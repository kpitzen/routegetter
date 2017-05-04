"""RoutesParser

This module will use the requests package to find daily route information
in html form from the cyride website, and use beautifulsoup4 to parse that information
into a usable form.
"""
from os.path import join, abspath, sep
import io

import requests
from bs4 import BeautifulSoup

DATA_DIR = join(sep.join(sep.split(abspath(__file__))[:-1]), 'data', 'html')

def get_request(url: str, payload: dict=None, request_type: str='get') -> requests.get:
    '''this function takes a url and a dictionary payload and
    returns a get request'''
    if request_type == 'put':
        output_request = requests.put(url, params=payload)
    else:
        output_request = requests.get(url, params=payload)
    try:
        assert output_request.status_code != 404
    except AssertionError:
        print('ERROR: request has failed')
        raise
    return output_request

def prettify_html_file(html_file: io.TextIOBase) -> BeautifulSoup:
    '''uses beautifulsoup to access structure of HTML data'''
    soup = BeautifulSoup(html_file, 'html.parser')
    return soup


class RouteGetter():
    '''This class will download the cyride route information into a textfile for
    beautifulsoup to consume'''

    def __init__(self, url: str, payload: dict, request_type: str='get'):
        self.payload = payload
        self.url = url
        self.request = get_request(url=self.url, payload=self.payload, request_type=request_type)

    def export_route_data(self):
        '''write all data from request to an html file'''
        data_filename = join(DATA_DIR, 'route_index.html')
        with open(data_filename, 'w') as data_file:
            print(self.request.text, file=data_file, flush=True)


class RouteParser():
    '''this class will consume the exported html file from RouteGetter,
    and parse it into a usable form, writing out a python .bin file'''

    def __init__(self):
        self.data_file = join(DATA_DIR, 'route_index.html')
        with open(self.data_file, 'r') as html_file:
            self.pretty_html = prettify_html_file(html_file)

