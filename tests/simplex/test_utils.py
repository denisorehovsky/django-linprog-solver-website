from test_plus.test import TestCase

from linprog_solver.simplex.utils import OptimizeSolution


class TestOptimizeSolution(TestCase):

    def test_optimize_solution(self):
        kwargs = {
            'tableau': [[5, 5], [6, 6]],
            'phase': 0,
            'nit': 2,
            'pivot': (0, 1),
            'basis': [0],
            'complete': False
        }
        solution = OptimizeSolution()
        solution.save_step(xk=[1, 1, 1], **kwargs)

        expected = {
            'xk': [1, 1, 1],
            'tableau': [[5, 5], [6, 6]],
            'phase': 0,
            'nit': 2,
            'pivrow': 0,
            'pivcol': 1,
            'basis': [0],
            'complete': False,
            'status': 'Iteration 2 - Phase 0'
        }

        self.assertEqual(solution.solution_steps, [expected])

    def test_optimize_solution_if_optimization_is_complete(self):
        kwargs = {
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 2,
            'pivot': (0, 1),
            'basis': [0],
            'complete': True
        }
        solution = OptimizeSolution()
        solution.save_step(xk=[1, 1, 1], **kwargs)

        expected = {
            'xk': [1, 1, 1],
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 2,
            'pivrow': 0,
            'pivcol': 1,
            'basis': [0],
            'complete': True,
            'status': 'Iteration Complete - Phase 1'
        }

        self.assertEqual(solution.solution_steps, [expected])

    def test_optimize_solution_if_current_iteration_number_equals_to_zero(self):
        kwargs = {
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 0,
            'pivot': (0, 1),
            'basis': [0],
            'complete': False
        }
        solution = OptimizeSolution()
        solution.save_step(xk=[1, 1, 1], **kwargs)

        expected = {
            'xk': [1, 1, 1],
            'tableau': [[5, 5], [6, 6]],
            'phase': 1,
            'nit': 0,
            'pivrow': 0,
            'pivcol': 1,
            'basis': [0],
            'complete': False,
            'status': 'Initial Tableau - Phase 1'
        }

        self.assertEqual(solution.solution_steps, [expected])
