from django.contrib import messages

from django.shortcuts import redirect, render

from .exceptions import SimplexInitException
from .utils import generate_latex_result


class SimplexInitMixin:

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except SimplexInitException as error:
            messages.add_message(request, messages.ERROR, str(error))
            return redirect('simplex:init')


class SimplexSolveActionMixin:
    template_name_success = 'simplex/simplex_result.html'

    def form_valid(self, form):
        """
        If the form is valid, solve linear programming problem.
        """
        solution, result = form.solve()
        latex_result = generate_latex_result(
            form.get_values_of_objective_function_coefficients(),
            form.cleaned_data['tendency'],
            form.get_values_of_constraints(),
            result,
        )
        return render(self.request, self.template_name_success, {
            'result': latex_result,
            'solution_steps': solution.solution_steps,
        })
