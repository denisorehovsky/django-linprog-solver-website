from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django_functest import FuncWebTestMixin, FuncSeleniumMixin


class WebTestBase(FuncWebTestMixin, TestCase):
    pass


class SeleniumTestBase(FuncSeleniumMixin, StaticLiveServerTestCase):
    driver_name = 'Chrome'
