from unittest import TestCase

from tests.test_integration import test_settings as settings
from yolapy.services import Yola


class YolaServiceTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.service = Yola(url=settings.url, auth=settings.auth)
