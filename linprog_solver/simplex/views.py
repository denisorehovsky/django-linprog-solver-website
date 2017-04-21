from django.views.generic import FormView

from .mixins import SimplexInitMixin, SimplexSolveActionMixin
from .forms import SimplexInitForm, SimplexSolveForm


class SimplexInitView(SimplexInitMixin, FormView):
    template_name = 'simplex/simplex_init.html'
    form_class = SimplexInitForm


class SimplexSolveView(SimplexSolveActionMixin, SimplexInitMixin, FormView):
    template_name = 'simplex/simplex_solve.html'
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
