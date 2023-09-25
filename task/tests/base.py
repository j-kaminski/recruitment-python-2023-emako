from unittest import TestCase
from unittest.mock import patch

from task.logger import LOGGER


class TestBaseCase(TestCase):
    def setUp(self):
        LOGGER.disabled = True
        self.maxDiff = None

    def tearDown(self):
        LOGGER.disabled = False
