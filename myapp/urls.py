from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls import *
import views

urlpatterns = [
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^user/get_info$', views.info),
    url(r'^user/change_info$', views.change_info),
    url(r'^user/change_password$', views.change_password),
]