from task.logger import LOGGER
from unittest import TestCase
from unittest.mock import patch


class TestBaseCase(TestCase):
    def setUp(self):
        LOGGER.disabled = True
        self.maxDiff = None

    def tearDown(self):
        LOGGER.disabled = False
