from django.test import TestCase
from django_functest import FuncWebTestMixin


class WebTestBase(FuncWebTestMixin, TestCase):
    pass
