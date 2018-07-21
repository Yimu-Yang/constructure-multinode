from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^prefix', views.prefix, name='prefix'),
    url(r'^cooperators', views.cooperators, name='cooperators'),
    url(r'^cooperation', views.cooperation, name='cooperation')
]