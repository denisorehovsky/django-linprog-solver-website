from test_plus.test import TestCase


class TestSimplexInitView(TestCase):

    def test_returns_correct_status_code(self):
        self.get_check_200('simplex:init')
