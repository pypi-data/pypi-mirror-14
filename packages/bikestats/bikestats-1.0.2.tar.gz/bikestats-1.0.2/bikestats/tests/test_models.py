import os
import unittest
from bs4 import BeautifulSoup
from django.test import TestCase

from bikestats.models import Make, Model, Stat, parse_all
from bikestats.scraper import Scraper


TEST_DIR = os.path.join(os.path.dirname(__file__), '../../www.motorcyclespecs.co.za')


class TestScraper(TestCase):
    """ Test our scraped data. Note: you must have scraped the entire website before this test! """
    def test_scrape_root(self):
        parse_all(TEST_DIR)
        # TODO some sort of functional test, not just a count of makes
        self.assertEqual(132, Make.objects.count())
        self.assertEqual(4290, Model.objects.count())
        self.assertEqual(26482, Stat.objects.count())


if __name__ == '__main':
    unittest.main()
