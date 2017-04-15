from django.contrib import messages
from django.views.generic import FormView

from .exceptions import SimplexInitException
from .forms import SimplexInitForm, SimplexSolveForm


class SimplexInitView(FormView):
    template_name = 'simplex/simplex_init.html'
    form_class = SimplexInitForm


class SimplexSolveView(FormView):
    template_name = 'simplex/simplex_solve.html'
    form_class = SimplexSolveForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'variables': self.request.GET.get('variables', None)})
        kwargs.update({'conditions': self.request.GET.get('conditions', None)})
        return kwargs

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except SimplexInitException as error:
            messages.add_message(request, messages.ERROR, str(error))
            kwargs.update({'form': None})
            return self.render_to_response(self.get_context_data(**kwargs))
