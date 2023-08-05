# import regex

from unittest import TestCase

try:
    from helpers import StaxHelper
except:
    from staxing.helpers import StaxHelper


class TestHelper(TestCase):
    ''''''
    def setUp(self):
        self.helper = StaxHelper()

    def tearDown(self):
        self.helper.driver = None

    def test_run_on(self):
        ''''''  # driver = self.helper
