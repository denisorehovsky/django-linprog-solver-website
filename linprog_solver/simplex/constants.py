from django.utils.translation import ugettext_lazy as _


STATUS = {
    0: _('Optimization terminated successfully'),
    1: _('Iteration limit reached'),
    2: _('Problem appears to be infeasible'),
    3: _('Problem appears to be unbounded')
}
