import logging
from unittest import TestCase


class TestBaseCase(TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.maxDiff = None

    def tearDown(self):
        logging.disable(logging.NOTSET)
