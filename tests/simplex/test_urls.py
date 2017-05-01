from django.core.urlresolvers import reverse, resolve

from test_plus.test import TestCase


class TestSimplexURLs(TestCase):
    """Test URL patterns for simplex app."""

    def test_init_reverse(self):
        """simplex:init should reverse to /simplex/."""
        self.assertEqual(reverse('simplex:init'), '/simplex/')

    def test_init_resolve(self):
        """/simplex/ should resolve to simplex:init."""
        self.assertEqual(resolve('/simplex/').view_name, 'simplex:init')

    def test_solve_reverse(self):
        """simplex:solve should reverse to /simplex/solve/."""
        self.assertEqual(reverse('simplex:solve'), '/simplex/solve/')

    def test_solve_resolve(self):
        """/simplex/solve/ should resolve to simplex:solve."""
        self.assertEqual(resolve('/simplex/solve/').view_name, 'simplex:solve')

    def test_pdf_reverse(self):
        """simplex:pdf should reverse to /simplex/pdf/."""
        self.assertEqual(reverse('simplex:pdf'), '/simplex/pdf/')

    def test_pdf_resolve(self):
        """/simplex/pdf/ should resolve to simplex:pdf."""
        self.assertEqual(resolve('/simplex/pdf/').view_name, 'simplex:pdf')
