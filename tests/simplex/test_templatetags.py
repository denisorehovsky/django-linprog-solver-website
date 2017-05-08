from unittest.mock import MagicMock

from django.template import Context, Template, TemplateSyntaxError

from test_plus.test import TestCase


class TestShowSolutionSteps(TestCase):

    def test_show_solution_steps(self):
        out = Template(
            "{% load simplex_extras %}"
            "{% show_solution_steps solution_steps %}"
        ).render(Context({
            'solution_steps': MagicMock()
        }))
        self.assertTrue(out)

    def test_parsing_errors(self):
        def render(t):
            return Template(t).render(Context())

        with self.assertRaises(TemplateSyntaxError):
            render("{% load simplex_extras %}{% show_solution_steps %}")
