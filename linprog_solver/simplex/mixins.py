from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render_to_response, redirect

from .exceptions import SimplexInitException


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
        result = form.solve()
        if result['success']:
            return render_to_response(self.template_name_success, {'result': result})
        else:
            messages.add_message(self.request, messages.ERROR,
                                 _("The algorithm can't find an optimal solution."))
            return self.render_to_response(self.get_context_data(form=form))
