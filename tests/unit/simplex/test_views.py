from test_plus.test import TestCase

from linprog_solver.simplex.forms import SimplexInitForm, SimplexSolveForm


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

    def test_get(self):
        resp = self.get('simplex:solve', data={'variables': 2,
                                               'conditions': 4,
                                               'is_non_negative': 'on'})
        self.response_200(resp)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertIsInstance(resp.context['form'], SimplexSolveForm)

    def test_get_with_bad_data(self):
        resp = self.get('simplex:solve', data={'variables': 'should_be_num',
                                               'conditions': 4,
                                               'is_non_negative': 'on'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertEqual(str(list(resp.context['messages'])[0]),
                         'Please define the number of variables and conditions')

        resp = self.get('simplex:solve', data={'variables': 15,
                                               'conditions': 4,
                                               'is_non_negative': 'on'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'simplex/simplex_solve.html')
        self.assertEqual(str(list(resp.context['messages'])[0]),
                         'The number of variables and conditions should be between 1 and 10')
