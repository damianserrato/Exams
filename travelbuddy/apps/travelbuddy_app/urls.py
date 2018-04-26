from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^travel$', views.travel),
    url(r'^add_travel$', views.add_travel),
    url(r'^details/(?P<id>\d+)$', views.details),
    url(r'^letsgo/(?P<id>\d+)$', views.letsgo),
    url(r'^home$', views.home)
]