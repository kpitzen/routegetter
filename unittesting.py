'''We will test all routegetter methods in this test suite'''

from os.path import join, abspath, sep
import unittest
import logging
import routesparser
from faker import Faker

LOG_FILE = join(sep.join(sep.split(abspath(__file__))[:-1]), 'log', 'testing', 'testing.log')

class RoutesGetterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger('RouteGetterTests')
        cls.log.setLevel(logging.DEBUG)
        cls.routegetter = routesparser.RouteGetter(url='http://www.cyride.com/index.aspx'
                                                   , payload={'page':1212})
        cls.data_generator = Faker()

    def setUp(self):
        self.bad_url = self.data_generator.url()

    def test_cyride_request(self):
        '''we want to test that our request succeeds at cyride'''
        log = self.log.getChild('test_cyride_request')
        request = self.routegetter.request
        self.assertNotEqual(request.status_code, 404)
        log.debug('%s, %s', request.url, request)

    @unittest.expectedFailure
    def test_bad_url(self):
        log = self.log.getChild('test_bad_url')
        request = routesparser.get_request(self.bad_url)
        self.assertEqual(request.status_code, 404)
        log.debug(request.url, request)


class RoutesParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger('RouteParserTests')
        cls.log.setLevel(logging.DEBUG)
        cls.routeparser = routesparser.RouteParser()

    def test_souped_data(self):
        log = self.log.getChild('test_souped_data')
        pretty_html = self.routeparser.pretty_html
        self.assertIsNotNone(self.routeparser.pretty_html)
        log.info(pretty_html.title.string)

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, filemode='w')
    unittest.main()
