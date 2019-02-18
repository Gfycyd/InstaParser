import django.views.generic
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^favicon\.ico$', django.views.generic.RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)),
    url(r'^home$',views.get_req, name='home'),
    url(r'^answer$',views.main, name='answer')
]