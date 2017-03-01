from test_plus.test import TestCase

from linprog_solver.simplex.forms import SimplexInitForm


class TestSimplexInitView(TestCase):

    def test_returns_correct_status_code(self):
        self.get_check_200('simplex:init')

    def test_uses_correct_template(self):
        resp = self.get_check_200('simplex:init')
        self.assertTemplateUsed(resp, 'simplex/simplex_init.html')

    def test_context_data(self):
        resp = self.get_check_200('simplex:init')
        self.assertIsInstance(resp.context['form'], SimplexInitForm)


class TestSimplexSolveView(TestCase):

    def test_returns_correct_status_code(self):
        self.get_check_200('simplex:solve')

    def test_uses_correct_template(self):
        resp = self.get_check_200('simplex:solve')
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
