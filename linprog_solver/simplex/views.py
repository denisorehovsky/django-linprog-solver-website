from django.contrib import messages
from django.views.generic import FormView
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, redirect

from .exceptions import SimplexInitException
from .forms import SimplexInitForm, SimplexSolveForm


class SimplexInitView(FormView):
    template_name = 'simplex/simplex_init.html'
    form_class = SimplexInitForm


class SimplexSolveView(FormView):
    template_name = 'simplex/simplex_solve.html'
    template_name_success = 'simplex/simplex_result.html'
    form_class = SimplexSolveForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        variables = self.request.GET.get('variables',
                                         self.request.POST.get('variables'))
        constraints = self.request.GET.get('constraints',
                                          self.request.POST.get('constraints'))
        kwargs.update({'variables': variables})
        kwargs.update({'constraints': constraints})
        return kwargs

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except SimplexInitException as error:
            messages.add_message(request, messages.ERROR, str(error))
            return redirect('simplex:init')

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
