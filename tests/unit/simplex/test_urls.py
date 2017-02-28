from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestSimplexURLs(TestCase):
    """Test URL patterns for simplex app."""

    def test_init_reverse(self):
        """simplex:init should reverse to /simplex/."""
        self.assertEqual(reverse('simplex:init'), '/simplex/')

    def test_init_resolve(self):
        """/simplex/ should resolve to users:init."""
        self.assertEqual(resolve('/simplex/').view_name, 'simplex:init')
