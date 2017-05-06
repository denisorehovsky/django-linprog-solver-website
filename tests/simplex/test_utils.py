from test_plus.test import TestCase

from linprog_solver.simplex.utils import OptimizeSolution


class TestUtils(TestCase):

    def test_optimize_solution(self):
        kwargs = {
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 0,
            'pivot': (0, 1),
            'basis': [0],
            'complete': False,
        }

        solution = OptimizeSolution()
        solution.save_step([1, 1, 1], **kwargs)
        solution.save_step([5, 5, 5], **kwargs)

        expected = {
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 0,
            'pivrow': 0,
            'pivcol': 1,
            'basis': [0],
            'complete': False,
        }

        self.assertEqual(
            solution.solution_steps,
            [{'xk': [1, 1, 1], **expected}, {'xk': [5, 5, 5], **expected}]
        )
