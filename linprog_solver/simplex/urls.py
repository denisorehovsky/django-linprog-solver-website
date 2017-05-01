from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.SimplexInitView.as_view(),
        name='init'
    ),
    url(
        regex=r'^solve/$',
        view=views.SimplexSolveView.as_view(),
        name='solve'
    ),
    url(
        regex=r'^pdf/$',
        view=views.SimplexPDFView.as_view(),
        name='pdf'
    ),
]
